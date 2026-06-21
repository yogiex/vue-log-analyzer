---
title: State-driven Animations with CSS Transitions and Style Bindings
impact: LOW
impactDescription: Combining Vue's reactive style bindings with CSS transitions creates smooth, interactive animations
type: best-practice
tags: [vue3, animation, css, transition, style-binding, state, interactive]
---

# State-driven Animations with CSS Transitions and Style Bindings

**Impact: LOW** - For responsive, interactive animations that react to user input or state changes, combine Vue's dynamic style bindings with CSS transitions.

## Basic Pattern

```vue
<template>
  <div @mousemove="onMousemove" :style="{ backgroundColor: `hsl(${hue}, 80%, 50%)` }" class="interactive-area">
    <p>Move your mouse across this div...</p>
    <p>Hue: {{ hue }}</p>
  </div>
</template>
<script setup>
import { ref } from 'vue'
const hue = ref(0)
function onMousemove(e) {
  const rect = e.currentTarget.getBoundingClientRect()
  hue.value = Math.round((e.clientX - rect.left) / rect.width * 360)
}
</script>
<style>
.interactive-area { transition: background-color 0.3s ease; height: 200px; }
</style>
```

## Following Mouse Position

```vue
<template>
  <div class="container" @mousemove="onMousemove">
    <div class="follower" :style="{ transform: `translate(${x}px, ${y}px)` }" />
  </div>
</template>
<script setup>
import { ref } from 'vue'
const x = ref(0); const y = ref(0)
function onMousemove(e) {
  const rect = e.currentTarget.getBoundingClientRect()
  x.value = e.clientX - rect.left; y.value = e.clientY - rect.top
}
</script>
<style>
.container { position: relative; height: 300px; }
.follower { position: absolute; width: 20px; height: 20px; background: blue; border-radius: 50%; transition: transform 0.1s ease-out; pointer-events: none; }
</style>
```

## Progress Animation

```vue
<template>
  <div class="progress-container">
    <div class="progress-bar" :style="{ width: `${progress}%` }" />
  </div>
  <input type="range" v-model.number="progress" min="0" max="100" />
</template>
<script setup>
import { ref } from 'vue'
const progress = ref(0)
</script>
<style>
.progress-container { height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; }
.progress-bar { height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); transition: width 0.3s ease; }
</style>
```

## Performance Considerations

```css
/* GOOD: GPU-accelerated properties */
.element { transition: transform 0.3s ease, opacity 0.3s ease; }

/* AVOID: Properties that trigger layout recalculation */
.element { transition: width 0.3s ease, height 0.3s ease; }
```
