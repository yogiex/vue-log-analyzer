# UIUX.md — Design System & Consistency Rules for Vue 3 + Vuetify Dashboard

This document defines the **UI/UX standards** and **implementation rules** for all dashboard interfaces built with Vue 3 and Vuetify. It serves as the **single source of truth** for both human developers and agentic AI tools (e.g., opencode) to ensure visual and behavioural consistency across the entire application.

---

## 1. Philosophy

- **Clarity over decoration** – every UI element must serve a functional purpose.
- **Efficiency** – minimize cognitive load; users should accomplish tasks in as few clicks as possible.
- **Responsive & accessible** – all screens work on all breakpoints and meet WCAG 2.1 AA.
- **Vuetify-first** – leverage Vuetify components and utility classes; only write custom CSS when strictly necessary.

---

## 2. Colour System

All colours are defined in the Vuetify theme. **Do not hardcode hex values** in components.

### 2.1 Theme Palette

| Role       | Vuetify Variable                   | Usage                                       |
| ---------- | ---------------------------------- | ------------------------------------------- |
| Primary    | `$vuetify.theme.colors.primary`    | Buttons, links, active states, key actions. |
| Secondary  | `$vuetify.theme.colors.secondary`  | Accents, badges, alternative CTAs.          |
| Surface    | `$vuetify.theme.colors.surface`    | Cards, dialogs, sidebars.                   |
| Background | `$vuetify.theme.colors.background` | Main page background.                       |
| Error      | `$vuetify.theme.colors.error`      | Validation messages, destructive actions.   |
| Warning    | `$vuetify.theme.colors.warning`    | Warnings, pending states.                   |
| Success    | `$vuetify.theme.colors.success`    | Confirmation, completed states.             |
| Info       | `$vuetify.theme.colors.info`       | Informational banners, tooltips.            |

### 2.2 Text Colours

- **Headings & primary text**: `color: rgba(0,0,0,0.87)` (or `$vuetify.theme.colors.text.primary` in dark mode)
- **Secondary text**: `color: rgba(0,0,0,0.60)`
- **Disabled text**: `color: rgba(0,0,0,0.38)`

### 2.3 Color Palette (Hex Values)

Source of truth for all colors. **Never hardcode hex in components** — import from `@/theme/colors.js` instead.

#### Theme Core

| Token | Hex | Usage |
|-------|-----|-------|
| `COLORS.primary` | `#1565C0` | Buttons, active states, key actions, chart primary line |
| `COLORS.secondary` | `#FF8F00` | Accents, badges, alternative CTAs, chart negative |
| `COLORS.accent` | `#82B1FF` | Complementary highlights |
| `COLORS.error` | `#FF5252` | Validation, destructive actions, dangerous states |
| `COLORS.info` | `#2196F3` | Informational banners, tooltips |
| `COLORS.success` | `#4CAF50` | Confirmation, completed states |
| `COLORS.warning` | `#FFC107` | Warnings, pending states |
| `COLORS.surface` | `#FFFFFF` | Cards, dialogs, sidebars |
| `COLORS.background` | `#F5F5F5` | Main page background |

#### Chart

| Token | Hex / RGBA | Usage |
|-------|------------|-------|
| `COLORS.chart.positive` | `#1565C0` | Positive/primary data series (blue — colorblind-safe) |
| `COLORS.chart.negative` | `#FF8F00` | Negative/secondary data series (amber — colorblind-safe) |
| `COLORS.chart.neutral` | `#82B1FF` | Neutral/tertiary data series |
| `COLORS.chart.series[]` | `['#1565C0','#FF8F00','#2196F3','#4CAF50','#FF5252']` | Multi-series data colors |
| `COLORS.chart.fillPrimary` | `rgba(21, 101, 192, 0.08)` | Area fill under line chart |
| `COLORS.chart.fillSecondary` | `rgba(255, 143, 0, 0.08)` | Area fill for secondary series |

#### Interaction

| Token | Hex | Usage |
|-------|-----|-------|
| `COLORS.hover.primary` | `#1976D2` | Button hover, card hover border |
| `COLORS.hover.secondary` | `#FFA000` | Secondary item hover |
| `COLORS.hover.info` | `#42A5F5` | Info item hover |
| `COLORS.hover.success` | `#66BB6A` | Success state hover |
| `COLORS.hover.error` | `#E53935` | Destructive action hover |

#### Chart Defaults

| Token | RGBA | Usage |
|-------|------|-------|
| `COLORS.chartGrid` | `rgba(0, 0, 0, 0.06)` | Subtle grid lines |
| `COLORS.chartTooltip` | `rgba(0, 0, 0, 0.8)` | Tooltip background |

#### Text

| Token | RGBA | Usage |
|-------|------|-------|
| `COLORS.text.primary` | `rgba(0, 0, 0, 0.87)` | Headings, body text |
| `COLORS.text.secondary` | `rgba(0, 0, 0, 0.60)` | Labels, metadata |
| `COLORS.text.disabled` | `rgba(0, 0, 0, 0.38)` | Disabled text |

### 2.4 Semantic States

- Hover: increase opacity or use `:hover` class from Vuetify.
- Focus: use Vuetify's built‑in focus ring (`v-ripple` + `outline`).
- Disabled: use `disabled` prop; opacity reduced automatically.

---

## 3. Typography

Use Vuetify’s typography classes **exclusively**. Never set `font-size`, `font-weight`, or `line-height` manually.

### 3.1 Heading Hierarchy

| Element          | Vuetify Class   | Size     | Weight | Usage                         |
| ---------------- | --------------- | -------- | ------ | ----------------------------- |
| Page Title       | `text-h4`       | 2.125rem | 500    | Top‑level page headings.      |
| Section Title    | `text-h5`       | 1.5rem   | 500    | Card headers, major sections. |
| Subsection Title | `text-h6`       | 1.25rem  | 500    | Inside cards, table titles.   |
| Body Large       | `text-body-1`   | 1rem     | 400    | Main content, paragraphs.     |
| Body Small       | `text-body-2`   | 0.875rem | 400    | Secondary info, metadata.     |
| Caption          | `text-caption`  | 0.75rem  | 400    | Helper text, footnotes.       |
| Overline         | `text-overline` | 0.75rem  | 500    | Labels, status chips.         |

### 3.2 Font Family

- **Primary font**: `Roboto` (Vuetify default).
- **Monospace**: `Roboto Mono` for code / numeric tables.

---

## 4. Spacing & Layout

Use Vuetify’s **spacing utility classes** (`pa-*`, `ma-*`, `py-*`, etc.) based on the **8px grid**.

### 4.1 Spacing Scale

| Class Suffix | Size | Usage                                  |
| ------------ | ---- | -------------------------------------- |
| `-0`         | 0    | No spacing.                            |
| `-1`         | 4px  | Tight elements (icon + text).          |
| `-2`         | 8px  | Small gaps (between list items).       |
| `-3`         | 12px | Medium gaps (between form fields).     |
| `-4`         | 16px | Standard padding for cards/containers. |
| `-5`         | 20px | Large gaps (between sections).         |
| `-6`         | 24px | Page margins / main container padding. |
| `-7`         | 28px | Spacious separation.                   |
| `-8`         | 32px | Maximum gap (header to content).       |

### 4.2 Page Structure

- Use `v-container` as the root layout wrapper with `fluid` for full‑width dashboards.
- Inside, use `v-row` and `v-col` with proper `cols`, `md`, `lg` breakpoints.
- **Content max‑width**: 1440px for large screens (apply `max-width` on `v-container` if needed).

### 4.3 Card & Panel Spacing

- Cards: `pa-4` or `pa-6` depending on density.
- Card title: `py-2` + `px-4` with `text-h6`.
- Card actions: `pa-2` with buttons aligned to the right.

### 4.4 Border Radius

Use Vuetify's rounded utility classes consistently:

| Class           | Size  | Usage                                     |
| --------------- | ----- | ----------------------------------------- |
| `rounded-xs`    | 2px   | Badges, small decorative elements.        |
| `rounded-sm`    | 4px   | Input fields, small cards.                |
| `rounded`       | 4px   | Default — buttons, cards, dialogs.        |
| `rounded-lg`    | 8px   | Cards, modals, side panels.               |
| `rounded-xl`    | 16px  | Hero sections, large containers.          |
| `rounded-pill`  | 24px  | Chips, tags, interactive elements.        |
| `rounded-0`     | 0px   | Tables, lists, edge-to-edge containers.   |

---

## 5. Grid System

- Always use Vuetify’s 12‑column grid.
- Define breakpoints explicitly:

| Breakpoint | Suffix | Min Width |
| ---------- | ------ | --------- |
| xs         | (none) | 0px       |
| sm         | `sm`   | 600px     |
| md         | `md`   | 960px     |
| lg         | `lg`   | 1264px    |
| xl         | `xl`   | 1904px    |

- **Mobile‑first**: provide `cols="12"` then override at larger breakpoints.

Example:

```vue
<v-col cols="12" sm="6" md="4" lg="3">
  <!-- content -->
</v-col>
```

---

## 6. Component Usage Rules

### 6.1 General

- Always use Vuetify components (`v-btn`, `v-card`, `v-table`, etc.) – never build custom equivalents.
- Prefer **props** over custom CSS for styling (e.g., `color`, `variant`, `density`).
- Set `density="comfortable"` as default for data‑dense areas (tables, lists); `"default"` for everything else.

### 6.2 Buttons

- **Primary action**: `v-btn color="primary" variant="flat"` (solid).
- **Secondary action**: `v-btn color="primary" variant="outlined"`.
- **Tertiary action**: `v-btn color="primary" variant="text"`.
- **Icon buttons**: `v-btn icon` with `variant="text"` and `color="default"`.
- Always add `aria-label` for icon‑only buttons.

#### Button Sizes

| Size        | Vuetify Prop | Height | Usage                              |
| ----------- | ------------ | ------ | ---------------------------------- |
| x-small     | `x-small`    | 24px   | Table actions, inline icon buttons.|
| small       | `small`      | 30px   | Chip actions, compact toolbars.    |
| default     | (omit)       | 36px   | Standard buttons, forms.           |
| large       | `large`      | 44px   | Hero CTAs, primary page actions.   |
| x-large     | `x-large`    | 52px   | Splash screens, featured CTAs.     |

### 6.3 Cards (v-card)

Card components follow Vuetify defaults with consistent spacing:

#### Card Spacing Variants

| Variant   | Classes | Usage                              |
| --------- | ------- | ---------------------------------- |
| Compact   | `pa-2`  | Data-dense lists, metrics inline.  |
| Default   | `pa-4`  | Standard cards, forms, charts.     |
| Spacious  | `pa-6`  | Hero cards, welcome sections.      |

#### Card Structure

- **Header**: `v-card-title` with `text-h6` + `d-flex` for title + actions.
- **Body**: `v-card-text` with `pa-4` (or variant above).
- **Actions**: `v-card-actions` with buttons aligned right (`class="justify-end"`).
- **Loading state**: use `v-skeleton-loader` inside `v-card`.
- **Hover effect**: apply `class="card-hover"` or Vuetify's built‑in `:hover` border.

### 6.4 Tables (v-data-table)

- Use `v-data-table` with `density="comfortable"`.
- Enable `hover` and `fixed-header` when rows > 20.
- Column headers: bold, `text-uppercase` with `text-caption`.
- Row actions: place in the last column, use icon buttons (`v-btn icon size="x-small"`).
- Loading state: use `loading` prop with a skeleton or progress bar.

### 6.5 Forms

- Use `v-form` with `v-model` validation.
- Inputs: `v-text-field`, `v-select`, `v-checkbox`, etc.
- All inputs must have `label` and `hint` where needed.
- Validation errors appear via `v-alert` or inline `error-messages`.
- Group related fields using `v-row` with spacing (`class="ga-3"`).
- Submit button: always `type="submit"` and `color="primary"`.

### 6.6 Navigation (Drawer, App Bar & Breadcrumbs)

- Left navigation drawer: `v-navigation-drawer` with `expand-on-hover` for compact mode.
- App bar: `v-app-bar` with `flat`, `elevation="0"`.
- Active route highlighting: use `exact-active-class="v-btn--active"` or `:active="true"`.

#### Breadcrumb Design

| Element        | Implementation                          | Usage                              |
| -------------- | --------------------------------------- | ---------------------------------- |
| Container      | `v-breadcrumbs density="comfortable"`   | Page title area, below app bar.    |
| Divider        | `divider-by="›"` (single right‑pointing)| Clean arrow separator.             |
| Items          | Array of `{ title, disabled, href }`    | Last item `disabled` for current.  |
| Active         | `color="primary"` + `text-body-2`       | Current page label.                |
| Inactive       | `color="text-secondary"` + `text-body-2`| Parent pages, clickable.           |

### 6.7 Feedback & Alerts

- Success/error messages: `v-alert` with `type="success"` / `"error"` and `dismissible`.
- Loading indicators: use `v-progress-circular` (indeterminate) or `v-progress-linear` for uploads.
- Empty states: show `v-card` with an icon + `text-h6` + `text-body-2`.

---

## 7. Responsiveness

- **Mobile‑first** – every page must be usable on a 320px width.
- Use `v-container fluid` and `v-row no-gutters` when full‑width is required.
- Hide elements on small screens using `v-hide-sm-and-down`, `v-show-sm-and-up` (Vuetify’s display helpers).
- For tables: use `v-data-table` with `mobile-breakpoint="sm"` to enable a card‑based mobile view.

---

## 8. Interactions & Animations

- Use Vuetify’s built‑in **ripple** effect (`v-ripple` directive) for clickable elements.
- Transitions: use `<transition-group>` or Vuetify’s `<v-fade-transition>` for consistent enter/leave.
- **Debounce** input events (search, filter) with 300ms delay.
- Tooltips: use `v-tooltip` with `open-delay="500"` to avoid clutter.
- Menus: use `v-menu` with `close-on-content-click` and `offset-y`.

---

## 9. Icons

- Use **Material Design Icons** (mdi) via Vuetify’s icon component.
- Import only required icons to reduce bundle size.
- Icon sizes:
  - `x-small` (16px) – for table actions.
  - `small` (20px) – for buttons / chips.
  - `default` (24px) – standard.
  - `large` (32px) – for empty states / hero.
- Always pair icons with text except when in an icon‑only button (then add `aria-label`).

---

## 10. Accessibility

- **Colour contrast**: all text/background combinations must pass WCAG AA (4.5:1 for normal text).
- **Focus indicators**: never disable default browser outline; Vuetify provides `.v-ripple` + focus rings.
- **ARIA attributes**:
  - Add `aria-label` to all interactive elements without visible text.
  - Use `role="status"` on live regions (e.g., alerts).
  - Use `aria-describedby` for error messages.
- **Semantic HTML**: use `v-main`, `v-header`, `v-footer` where appropriate.
- **Keyboard navigation**: all interactive elements must be reachable via Tab; use `@keydown` only for custom shortcuts.

---

## 11. Custom CSS (when unavoidable)

- **Never** use `!important`.
- Follow **BEM** naming convention: `.block__element--modifier`.
- Prefix custom classes with `dashboard-` to avoid conflicts.
- Keep custom styles in a single `scss` file and import in `App.vue` or use `<style scoped>`.
- For responsive custom CSS, use Vuetify’s breakpoint mixins:

```scss
@include breakpoint(md-and-up) {
  .dashboard-custom { ... }
}
```

---

## 12. Performance & Code Consistency

- Lazy‑load routes with `defineAsyncComponent`.
- Use `v-once` for static data.
- Prefer `computed` over `methods` for derived data.
- Use `key` on `v-for` loops with stable IDs.
- Keep template logic minimal – delegate complex logic to `setup` or composables.

---

## 13. Naming Conventions (for AI and Humans)

| Element     | Convention                | Example                 |
| ----------- | ------------------------- | ----------------------- |
| Components  | PascalCase                | `DataTable.vue`         |
| Props       | camelCase                 | `:isLoading="true"`     |
| Events      | kebab‑case                | `@update:model-value`   |
| CSS classes | BEM + `dashboard-` prefix | `dashboard-card__title` |
| Variables   | camelCase                 | `userList`              |
| Composables | `use` prefix              | `useDashboardData`      |

---

## 14. Testing UI Consistency

- Use **Storybook** (or similar) to document all Vuetify component variants with dashboard‑specific defaults.
- Every new component must be visually reviewed against this document.
- Use automated visual regression tests to detect unintended style drifts.

---

## 15. Exceptions & Overrides

- When business logic demands a deviation, **document it inline** with a comment referencing this file.
- Overrides must be approved by the design lead and added to a `_overrides.scss` file.

---

**This document is living** – update it whenever a new pattern is adopted. All team members (and AI agents) must refer to it as the ultimate rulebook for dashboard UI/UX.
