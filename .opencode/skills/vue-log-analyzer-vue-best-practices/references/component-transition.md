---
title: Transition Component Best Practices
impact: MEDIUM
impactDescription: Transition animates a single element or component; incorrect structure or keys prevent animations
type: best-practice
tags: [vue3, transition, animation, performance, keys]
---

# Transition Component Best Practices

**Impact: MEDIUM** - `<Transition>` animates entering/leaving of a single element or component.

## Task List

- Wrap a single element or component inside `<Transition>`
- Provide a `key` when switching between same element types
- Use `mode="out-in"` when you need sequential swaps
- Prefer `transform` and `opacity` for smooth animations

## Single Root Element

**BAD:**
```vue
<Transition name="fade">
  <h3>Title</h3>
  <p>Description</p>
</Transition>
```

**GOOD:**
```vue
<Transition name="fade">
  <div>
    <h3>Title</h3>
    <p>Description</p>
  </div>
</Transition>
```

## Force Transitions Between Same Element Types

Add `key` so Vue treats it as a new element and triggers enter/leave.

**BAD:**
```vue
<Transition name="fade">
  <p v-if="isActive">Active</p>
  <p v-else>Inactive</p>
</Transition>
```

**GOOD:**
```vue
<Transition name="fade" mode="out-in">
  <p v-if="isActive" key="active">Active</p>
  <p v-else key="inactive">Inactive</p>
</Transition>
```

## Use `mode` to Avoid Overlap

**BAD:**
```vue
<Transition name="fade">
  <component :is="currentView" />
</Transition>
```

**GOOD:**
```vue
<Transition name="fade" mode="out-in">
  <component :is="currentView" :key="currentView" />
</Transition>
```

## Animate `transform` and `opacity` for Performance

**BAD:**
```css
.slide-enter-active, .slide-leave-active { transition: height 0.3s ease; }
.slide-enter-from, .slide-leave-to { height: 0; }
```

**GOOD:**
```css
.slide-enter-active, .slide-leave-active { transition: transform 0.3s ease, opacity 0.3s ease; }
.slide-enter-from { transform: translateX(-12px); opacity: 0; }
.slide-leave-to { transform: translateX(12px); opacity: 0; }
```
