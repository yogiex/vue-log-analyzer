---
title: KeepAlive Component Best Practices
impact: HIGH
impactDescription: KeepAlive caches component instances; misuse causes stale data, memory growth, or unexpected lifecycle behavior
type: best-practice
tags: [vue3, keepalive, cache, performance, router, dynamic-components]
---

# KeepAlive Component Best Practices

**Impact: HIGH** - `<KeepAlive>` caches component instances instead of destroying them. Use it to preserve state across switches, but manage cache size and freshness explicitly to avoid memory growth or stale UI.

## Task List

- Use KeepAlive only where state preservation improves UX
- Set a reasonable `max` to cap cache size
- Declare component names for include/exclude matching
- Use `onActivated`/`onDeactivated` for cache-aware logic
- Decide how and when cached views refresh their data
- Avoid caching memory-heavy or security-sensitive views

## When to Use KeepAlive

Use KeepAlive when switching between views where state should persist (tabs, multi-step forms, dashboards).

**BAD:**
```vue
<component :is="currentTab" />
```

**GOOD:**
```vue
<KeepAlive>
  <component :is="currentTab" />
</KeepAlive>
```

## When NOT to Use KeepAlive

- Search or filter pages where users expect fresh results
- Memory-heavy components (maps, large tables, media players)
- Sensitive flows where data must be cleared on exit

## Limit and Control the Cache

Always cap cache size with `max` and restrict caching to specific components when possible.

```vue
<KeepAlive :max="5" include="Dashboard,Settings">
  <component :is="currentView" />
</KeepAlive>
```

## Cache Invalidation Strategies

Use keys or dynamic include/exclude to force refreshes.

```vue
<script setup>
import { ref, reactive } from 'vue'
const currentView = ref('Dashboard')
const viewKeys = reactive({ Dashboard: 0, Settings: 0 })
function invalidateCache(view) { viewKeys[view]++ }
</script>
<template>
  <KeepAlive>
    <component :is="currentView" :key="`${currentView}-${viewKeys[currentView]}`" />
  </KeepAlive>
</template>
```

## Lifecycle Hooks for Cached Components

```vue
<script setup>
import { onActivated, onDeactivated } from 'vue'
onActivated(() => { refreshData() })
onDeactivated(() => { pauseTimers() })
</script>
```

## Router Caching

```vue
<template>
  <router-view v-slot="{ Component, route }">
    <KeepAlive>
      <component :is="Component" :key="route.fullPath" />
    </KeepAlive>
  </router-view>
</template>
```
