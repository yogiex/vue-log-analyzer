---
title: Component Fallthrough Attributes Best Practices
impact: MEDIUM
impactDescription: Incorrect $attrs access and reactivity assumptions can cause undefined values and watchers that never run
type: best-practice
tags: [vue3, attrs, fallthrough, composition-api, reactivity]
---

# Component Fallthrough Attributes Best Practices

**Impact: MEDIUM** - Fallthrough attributes are straightforward once you follow Vue's conventions: hyphenated names use bracket notation, listener keys are camelCase `onX`, and `useAttrs()` is current-but-not-reactive.

## Task List

- Access hyphenated attribute names with bracket notation (`attrs['data-testid']`)
- Access event listeners with camelCase `onX` keys (`attrs.onClick`)
- Do not `watch()` values returned from `useAttrs()`; those watchers do not trigger on attr changes
- Use `onUpdated()` for attr-driven side effects
- Promote frequently observed attrs to props when reactive observation is required

## Access Attribute and Listener Keys Correctly

Hyphenated attribute names preserve their original casing in JavaScript, so dot notation does not work for keys that include `-`.

**BAD:**
```vue
<script setup>
import { useAttrs } from 'vue'
const attrs = useAttrs()
console.log(attrs['on-click'])  // undefined
console.log(attrs['@click'])    // undefined
</script>
```

**GOOD:**
```vue
<script setup>
import { useAttrs } from 'vue'
const attrs = useAttrs()
console.log(attrs['data-testid'])
console.log(attrs['aria-label'])
console.log(attrs.onClick)
console.log(attrs.onCustomEvent)
</script>
```

## `useAttrs()` Is Not Reactive

`useAttrs()` always reflects the latest values, but it is intentionally not reactive for watcher tracking.

**BAD:**
```vue
<script setup>
import { watch, useAttrs } from 'vue'
const attrs = useAttrs()
watch(() => attrs.someAttr, (newValue) => {
  console.log('Changed:', newValue) // Never runs on attr changes
})
</script>
```

**GOOD:**
```vue
<script setup>
import { onUpdated, useAttrs } from 'vue'
const attrs = useAttrs()
onUpdated(() => { console.log('Latest attrs:', attrs) })
</script>
```

**GOOD:**
```vue
<script setup>
import { watch } from 'vue'
const props = defineProps({ someAttr: String })
watch(() => props.someAttr, (newValue) => { console.log('Changed:', newValue) })
</script>
```

## Check for optional attrs safely

```vue
<script setup>
import { computed, useAttrs } from 'vue'
const attrs = useAttrs()
const hasTestId = computed(() => 'data-testid' in attrs)
const ariaLabel = computed(() => attrs['aria-label'] ?? 'Default label')
</script>
```

## TypeScript Notes

`useAttrs()` is typed as `Record<string, unknown>`, so cast individual keys when needed.

```vue
<script setup lang="ts">
import { useAttrs } from 'vue'
const attrs = useAttrs()
const testId = attrs['data-testid'] as string | undefined
const onClick = attrs.onClick as ((event: MouseEvent) => void) | undefined
</script>
```
