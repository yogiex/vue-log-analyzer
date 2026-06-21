---
title: Directive Best Practices
impact: MEDIUM
impactDescription: Custom directives are powerful but easy to misuse; following patterns prevents leaks, invalid usage, and unclear abstractions
type: best-practice
tags: [vue3, directives, custom-directives, composition, typescript]
---

# Directive Best Practices

**Impact: MEDIUM** - Directives are for low-level DOM access. Use them sparingly, keep them side-effect safe, and prefer components or composables when you need stateful or reusable UI behavior.

## Task List

- Use directives only when you need direct DOM access
- Do not mutate directive arguments or binding objects
- Clean up timers, listeners, and observers in `unmounted`
- Register directives in `<script setup>` with the `v-` prefix
- Prefer components or composables for complex behavior

## Treat Directive Arguments as Read-Only

```ts
const vFocus = { mounted(el, binding) { el.focus() } }
```

## Clean Up Side Effects in `unmounted`

```ts
const vResize = {
  mounted(el) {
    const observer = new ResizeObserver(() => {})
    observer.observe(el)
    el._observer = observer
  },
  unmounted(el) { el._observer?.disconnect() }
}
```

## Prefer Function Shorthand for Single-Hook Directives

```ts
const vAutofocus = (el) => el.focus()
```

## Use the `v-` Prefix and Script Setup Registration

```vue
<script setup>
const vFocus = (el) => el.focus()
</script>
<template><input v-focus /></template>
```

## Handle SSR with `getSSRProps`

```ts
const vTooltip = {
  mounted(el, binding) {
    el.setAttribute('data-tooltip', binding.value)
    el.classList.add('has-tooltip')
  },
  getSSRProps(binding) {
    return { 'data-tooltip': binding.value, class: 'has-tooltip' }
  }
}
```

## Decide Between Directives and Components

Use a directive for DOM-level behavior. Use a component when behavior affects structure, state, or rendering.
