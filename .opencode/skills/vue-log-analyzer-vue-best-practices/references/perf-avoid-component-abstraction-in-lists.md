---
title: Avoid Excessive Component Abstraction in Large Lists
impact: MEDIUM
impactDescription: Each component instance has memory and render overhead - abstractions multiply this in lists
type: efficiency
tags: [vue3, performance, components, abstraction, lists, optimization]
---

# Avoid Excessive Component Abstraction in Large Lists

**Impact: MEDIUM** - Component instances are more expensive than plain DOM nodes. In large lists, this overhead multiplies.

**BAD:**
```vue
<!-- UserCard.vue - 4 wrapper components per item -->
<template>
  <Card>
    <CardHeader><UserAvatar :src="user.avatar" /></CardHeader>
    <CardBody><Text>{{ user.name }}</Text></CardBody>
  </Card>
</template>
<!-- 100 users = 500+ component instances -->
```

**GOOD:**
```vue
<!-- UserCard.vue - Flattened, uses native elements -->
<template>
  <div class="card">
    <div class="card-header"><img :src="user.avatar" :alt="user.name" class="avatar" /></div>
    <div class="card-body"><span class="user-name">{{ user.name }}</span></div>
  </div>
</template>
<script setup>
defineProps({ user: Object })
</script>
<style scoped>
.card { /* ... */ }
.card-header { /* ... */ }
.card-body { /* ... */ }
</style>
```

## When Abstraction Is Still Worth It

- Complex behavior is encapsulated (tooltips, logic)
- The list itself is small (< 20 items)
- Virtualization is used (only ~20 items rendered at once)

## Impact Calculation

| List Size | Components per Item | Total Instances |
|-----------|---------------------|-----------------|
| 100 items | 1 (flat) | 100 |
| 100 items | 5 (deeply nested) | 500 |
| 1000 items | 1 (flat) | 1000 |
| 1000 items | 5 (deeply nested) | 5000 |
