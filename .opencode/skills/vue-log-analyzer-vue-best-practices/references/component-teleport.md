---
title: Teleport Component Best Practices
impact: MEDIUM
impactDescription: Teleport renders content outside the component's DOM position, which is essential for overlays but affects styling and layout
type: best-practice
tags: [vue3, teleport, modal, overlay, positioning, responsive]
---

# Teleport Component Best Practices

**Impact: MEDIUM** - `<Teleport>` renders part of a component's template in a different place in the DOM while preserving the Vue component hierarchy. Use it for overlays (modals, toasts, tooltips) or any UI that must escape stacking contexts, overflow, or fixed positioning constraints.

## Task List

- Teleport overlays to `body` or a dedicated container outside the app root
- Keep a shared target for similar UI (`#modals`, `#notifications`) and control layering with order or z-index
- Use `:disabled` for responsive layouts that should render inline on small screens
- Remember props, emits, and provide/inject still work through teleport
- Avoid relying on parent stacking contexts or transforms for teleported UI

## Teleport Overlays Out of Transformed Containers

When an ancestor has `transform`, `filter`, or `perspective`, fixed-position overlays can behave like they are locally positioned. Teleport escapes that context.

**BAD:**
```vue
<div class="animated-container">
  <button @click="open = true">Open</button>
  <div v-if="open" class="modal" style="position:fixed;inset:0;z-index:9999">Modal</div>
</div>
```

**GOOD:**
```vue
<template>
  <div class="animated-container">
    <button @click="open = true">Open</button>
    <Teleport to="body">
      <div v-if="open" class="modal">Modal</div>
    </Teleport>
  </div>
</template>
```

## Responsive Layouts with `disabled`

```vue
<script setup>
import { useMediaQuery } from '@vueuse/core'
const isMobile = useMediaQuery('(max-width: 768px)')
</script>
<template>
  <Teleport to="body" :disabled="isMobile">
    <nav class="sidebar">Navigation</nav>
  </Teleport>
</template>
```

## Logical Hierarchy Is Preserved

Teleport changes DOM position, not the Vue component tree. Props, emits, slots, and provide/inject still work:

```vue
<Teleport to="body">
  <ChildPanel :message="message" @close="open = false" />
</Teleport>
```

## Multiple Teleports to the Same Target

Teleports to the same target append in declaration order. Use a shared container to keep stacking predictable.
