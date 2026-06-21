<template>
  <v-navigation-drawer v-model="drawer" expand-on-hover rail color="surface" border="right">
    <template #prepend>
      <v-list-item lines="two" prepend-avatar="/logo-log-analyzer.png" title="Log Analyzer" subtitle="Dashboard" />
      <v-divider />
    </template>
    <v-list density="compact" nav>
      <v-list-item v-for="item in menuItems" :key="item.title" :prepend-icon="item.icon" :title="item.title"
        :value="item.title" :to="item.to" color="primary" exact />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { inject } from 'vue'

const drawer = inject('drawer')

const menuItems = [
  { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard' },
  { title: 'Users', icon: 'mdi-account-multiple', to: '/dashboard/users' },
  { title: 'Logs', icon: 'mdi-text-box-search-outline', to: '/dashboard/logs' },
  { title: 'Alerts', icon: 'mdi-bell-alert', to: '/dashboard/alerts' },
  { title: 'Findings', icon: 'mdi-magnify-expand', to: '/dashboard/findings' },
  { title: 'Monitoring', icon: 'mdi-monitor-dashboard', to: '/dashboard/monitoring' },
  { title: 'Calendar', icon: 'mdi-calendar-month', to: '/dashboard/calendar' },
  { title: 'Backups', icon: 'mdi-cloud-download', to: '/dashboard/backups' },
  { title: 'Thresholds', icon: 'mdi-speedometer', to: '/dashboard/thresholds' },
  { title: 'Systems', icon: 'mdi-cog', to: '/dashboard/systems' },
]
</script>
