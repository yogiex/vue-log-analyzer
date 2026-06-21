---
title: Use v-once and v-memo to Skip Unnecessary Updates
impact: MEDIUM
impactDescription: v-once skips all future updates for static content; v-memo conditionally memoizes subtrees
type: efficiency
tags: [vue3, performance, v-once, v-memo, optimization, directives]
---

# Use v-once and v-memo to Skip Unnecessary Updates

**Impact: MEDIUM** - Vue re-evaluates templates on every reactive change. For content that never changes or changes infrequently, `v-once` and `v-memo` tell Vue to skip updates.

## v-once: Render Once, Never Update

**BAD:**
```vue
<footer>
  <p>Copyright {{ copyrightYear }} {{ companyName }}</p>
</footer>
```

**GOOD:**
```vue
<footer v-once>
  <p>Copyright {{ copyrightYear }} {{ companyName }}</p>
</footer>
```

## v-memo: Conditional Memoization for Lists

**BAD:**
```vue
<div v-for="item in list" :key="item.id">
  <div :class="{ selected: item.id === selectedId }">
    <ExpensiveComponent :data="item" />
  </div>
</div>
```

**GOOD:**
```vue
<div v-for="item in list" :key="item.id" v-memo="[item.id === selectedId]">
  <div :class="{ selected: item.id === selectedId }">
    <ExpensiveComponent :data="item" />
  </div>
</div>
```

## v-memo with Multiple Dependencies

```vue
<div v-for="item in items" :key="item.id" v-memo="[item.id === selectedId, item.id === editingId]">
  <ItemCard :item="item" :selected="item.id === selectedId" :editing="item.id === editingId" />
</div>
```

## When NOT to Use These Directives

```vue
<!-- DON'T: Content that DOES need to update -->
<div v-once><span>Count: {{ count }}</span></div>

<!-- DON'T: When child components have their own reactive state -->
<div v-memo="[selected]"><InputField v-model="item.name" /></div>
```
