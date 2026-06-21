---
title: Render Function Patterns and Performance
impact: MEDIUM
impactDescription: Render functions require explicit patterns for lists, events, v-model, and performance to stay correct and maintainable
type: best-practice
tags: [vue3, render-function, h, v-model, directives, performance, jsx]
---

# Render Function Patterns and Performance

**Impact: MEDIUM** - Render functions are powerful but opt out of template compiler optimizations. Use them intentionally.

## Task List

- Prefer templates; use render functions only when templates cannot express the logic
- Always add stable keys when rendering lists with `h()`/JSX
- Use `withModifiers` / `withKeys` for event modifiers
- Implement `v-model` via `modelValue` + `onUpdate:modelValue`
- Apply custom directives with `withDirectives`

## Always add keys for list rendering

**BAD:**
```javascript
import { h, ref } from 'vue'
export default { setup() {
  const items = ref([{ id: 1, name: 'Apple' }])
  return () => h('ul', items.value.map(item => h('li', item.name)))
}}
```

**GOOD:**
```javascript
import { h, ref } from 'vue'
export default { setup() {
  const items = ref([{ id: 1, name: 'Apple' }])
  return () => h('ul', items.value.map(item => h('li', { key: item.id }, item.name)))
}}
```

## Use `withModifiers` / `withKeys` for event modifiers

```javascript
import { h, withModifiers, withKeys } from 'vue'
export default { setup() {
  const handleClick = () => {}
  const handleEnter = () => {}
  return () => h('div', [
    h('button', { onClick: withModifiers(handleClick, ['stop', 'prevent']) }, 'Click'),
    h('input', { onKeyup: withKeys(handleEnter, ['enter']) })
  ])
}}
```

## Implement `v-model` explicitly

```javascript
import { h, ref } from 'vue'
import CustomInput from './CustomInput.vue'
export default { setup() {
  const text = ref('')
  return () => h(CustomInput, { modelValue: text.value, 'onUpdate:modelValue': (value) => { text.value = value } })
}}
```

## Use `withDirectives` for custom directives

```javascript
import { h, withDirectives } from 'vue'
const vFocus = { mounted: (el) => el.focus() }
export default { setup() {
  return () => withDirectives(h('input'), [[vFocus]])
}}
```
