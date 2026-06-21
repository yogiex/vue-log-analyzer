---
title: Virtualize Large Lists to Avoid DOM Overload
impact: HIGH
impactDescription: Rendering thousands of list items creates excessive DOM nodes, causing slow renders and high memory usage
type: efficiency
tags: [vue3, performance, virtual-list, large-data, dom, optimization]
---

# Virtualize Large Lists to Avoid DOM Overload

**Impact: HIGH** - Rendering all items in a large list (hundreds or thousands) creates massive amounts of DOM nodes. List virtualization only renders visible items.

## Recommended Libraries

| Library | Best For |
|---------|----------|
| `vue-virtual-scroller` | General use, easy setup |
| `@tanstack/vue-virtual` | Complex layouts, headless |

**BAD:**
```vue
<template>
  <div class="user-list">
    <UserCard v-for="user in users" :key="user.id" :user="user" />
  </div>
</template>
```

**GOOD (vue-virtual-scroller):**
```vue
<template>
  <RecycleScroller class="user-list" :items="users" :item-size="80" key-field="id" v-slot="{ item }">
    <UserCard :user="item" />
  </RecycleScroller>
</template>
<script setup>
import { RecycleScroller } from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'
</script>
<style scoped>
.user-list { height: 600px; }
</style>
```

**GOOD (@tanstack/vue-virtual):**
```vue
<template>
  <div ref="parentRef" class="list-container">
    <div :style="{ height: `${rowVirtualizer.getTotalSize()}px`, position: 'relative' }">
      <div v-for="virtualRow in rowVirtualizer.getVirtualItems()" :key="virtualRow.key"
        :style="{ position: 'absolute', top: 0, left: 0, width: '100%', height: `${virtualRow.size}px`, transform: `translateY(${virtualRow.start}px)` }">
        <UserCard :user="users[virtualRow.index]" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useVirtualizer } from '@tanstack/vue-virtual'
const users = ref([/* ... */])
const parentRef = ref(null)
const rowVirtualizer = useVirtualizer({ count: users.value.length, getScrollElement: () => parentRef.value, estimateSize: () => 80, overscan: 5 })
</script>
```

## When NOT to Virtualize

- Lists under 50 items with simple content
- Print layouts where all content must render
- SEO-critical content that must be in initial HTML
