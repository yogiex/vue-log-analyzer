---
title: Suspense Component Best Practices
impact: MEDIUM
impactDescription: Suspense coordinates async dependencies with fallback UI; misconfiguration leads to missing loading states or confusing UX
type: best-practice
tags: [vue3, suspense, async, async-setup, loading, fallback, router]
---

# Suspense Component Best Practices

**Impact: MEDIUM** - `<Suspense>` coordinates async dependencies (async components or async setup) and renders a fallback while they resolve.

## Task List

- Wrap default and fallback slot content in a single root node
- Use `timeout` when you need the fallback to appear on reverts
- Force root replacement with `:key` when you need Suspense to re-trigger
- Add `suspensible` to nested Suspense boundaries (Vue 3.3+)
- Use `@pending`, `@resolve`, and `@fallback` for programmatic loading state
- Keep Suspense usage centralized and documented in production

## Single Root in Default and Fallback Slots

**BAD:**
```vue
<Suspense>
  <AsyncHeader />
  <AsyncList />
  <template #fallback>
    <LoadingSpinner />
    <LoadingHint />
  </template>
</Suspense>
```

**GOOD:**
```vue
<Suspense>
  <div>
    <AsyncHeader />
    <AsyncList />
  </div>
  <template #fallback>
    <div>
      <LoadingSpinner />
      <LoadingHint />
    </div>
  </template>
</Suspense>
```

## Fallback Timing on Reverts (`timeout`)

```vue
<Suspense :timeout="200">
  <component :is="currentView" :key="viewKey" />
  <template #fallback>Loading...</template>
</Suspense>
```

## Use `suspensible` for Nested Suspense (Vue 3.3+)

**BAD:**
```vue
<Suspense>
  <LayoutShell>
    <Suspense>
      <AsyncWidget />
      <template #fallback>Loading widget...</template>
    </Suspense>
  </LayoutShell>
  <template #fallback>Loading layout...</template>
</Suspense>
```

**GOOD:**
```vue
<Suspense>
  <LayoutShell>
    <Suspense suspensible>
      <AsyncWidget />
      <template #fallback>Loading widget...</template>
    </Suspense>
  </LayoutShell>
  <template #fallback>Loading layout...</template>
</Suspense>
```

## Track Loading with Suspense Events

```vue
<script setup>
import { ref } from 'vue'
const isLoading = ref(false)
const onPending = () => { isLoading.value = true }
const onResolve = () => { isLoading.value = false }
</script>
<template>
  <LoadingBar v-if="isLoading" />
  <Suspense @pending="onPending" @resolve="onResolve">
    <AsyncPage />
    <template #fallback><PageSkeleton /></template>
  </Suspense>
</template>
```

## Recommended Nesting with RouterView, Transition, KeepAlive

**GOOD:**
```vue
<router-view v-slot="{ Component }">
  <Transition mode="out-in">
    <KeepAlive>
      <Suspense>
        <component :is="Component" />
        <template #fallback>Loading...</template>
      </Suspense>
    </KeepAlive>
  </Transition>
</router-view>
```
