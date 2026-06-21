---
title: Avoid Expensive Operations in Updated Hook
impact: MEDIUM
impactDescription: Heavy computations in updated hook cause performance bottlenecks and potential infinite loops
type: capability
tags: [vue3, vue2, lifecycle, updated, performance, optimization, reactivity]
---

# Avoid Expensive Operations in Updated Hook

**Impact: MEDIUM** - The `updated` hook runs after every reactive state change that causes a re-render. Placing expensive operations here can cause severe performance degradation.

## Task List

- Never perform API calls in updated hook
- Never mutate reactive state inside updated (causes infinite loops)
- Use conditional checks to verify updates are relevant before acting
- Prefer `watch` or `watchEffect` for reacting to specific data changes
- Use throttling/debouncing if updated operations are expensive

**BAD:**
```javascript
export default {
  data() { return { items: [] } },
  updated() { fetch('/api/sync', { method: 'POST', body: JSON.stringify(this.items) }) }
}
```

**BAD (infinite loop):**
```javascript
export default {
  data() { return { renderCount: 0 } },
  updated() { this.renderCount++ }
}
```

**GOOD:**
```javascript
import debounce from 'lodash-es/debounce'
export default {
  data() { return { items: [] } },
  watch: {
    items: { handler(newItems) { this.syncToServer(newItems) }, deep: true }
  },
  methods: {
    syncToServer: debounce(function(items) {
      fetch('/api/sync', { method: 'POST', body: JSON.stringify(items) })
    }, 500)
  }
}
```

**GOOD (Composition API):**
```vue
<script setup>
import { ref, watch, onUpdated } from 'vue'
import { useDebounceFn } from '@vueuse/core'
const items = ref([])
watch(items, (newItems) => { syncToServer(newItems) }, { deep: true })
const syncToServer = useDebounceFn((items) => { fetch('/api/sync', { method: 'POST', body: JSON.stringify(items) }) }, 500)
onUpdated(() => { /* DOM synchronization only */ })
</script>
```

## Valid Use Cases for Updated Hook

```javascript
export default { updated() { this.thirdPartyWidget.refresh(); this.$nextTick(() => { this.maintainScrollPosition() }) } }
```

## Prefer Computed Properties for Derived Data

**BAD:**
```javascript
export default { updated() { this.sum = this.numbers.reduce((a, b) => a + b, 0) } }
```

**GOOD:**
```javascript
export default { computed: { sum() { return this.numbers.reduce((a, b) => a + b, 0) } } }
```
