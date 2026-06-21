---
title: Use Class-based Animations for Non-Enter/Leave Effects
impact: LOW
impactDescription: Class-based animations are simpler and more performant for elements that remain in the DOM
type: best-practice
tags: [vue3, animation, css, class-binding, state]
---

# Use Class-based Animations for Non-Enter/Leave Effects

**Impact: LOW** - For animations on elements that are not entering or leaving the DOM, use CSS class-based animations triggered by Vue's reactive state.

## Basic Pattern

```vue
<template>
  <div :class="{ shake: showError }">
    <button @click="submitForm">Submit</button>
    <span v-if="showError">This feature is disabled!</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const showError = ref(false)
function submitForm() {
  if (!isValid()) {
    showError.value = true
    setTimeout(() => { showError.value = false }, 820)
  }
}
</script>

<style>
.shake { animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both; }
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
</style>
```

## Using animationend Event

```vue
<template>
  <div :class="{ animate: isAnimating }" @animationend="isAnimating = false">Content</div>
</template>
<script setup>
import { ref } from 'vue'
const isAnimating = ref(false)
function triggerAnimation() { isAnimating.value = true }
</script>
```

## Composable for Reusable Animations

```javascript
// composables/useAnimation.js
import { ref } from 'vue'
export function useAnimation(duration = 500) {
  const isAnimating = ref(false)
  function trigger() {
    isAnimating.value = true
    setTimeout(() => { isAnimating.value = false }, duration)
  }
  return { isAnimating, trigger }
}
```
