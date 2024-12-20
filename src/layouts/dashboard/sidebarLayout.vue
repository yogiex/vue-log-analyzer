<template>
  <!-- <v-navigation-drawer image="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg" permanent theme="dark"> -->
  <v-navigation-drawer permanent="" theme="" color="primary">
    <v-list :lines="false" density="compact" nav>
      <v-list-item v-for="(item, i) in items" :key="i" :value="item" :to=item.url>
        <template v-slot:prepend>
          <v-icon :icon="item.icon"></v-icon>
        </template>

        <v-list-item-title v-text="item.text"></v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data: () => ({
    items: [
      { text: 'Home', icon: 'mdi-home', url: '/dashboard' },
      { text: 'Users', icon: 'mdi-account-multiple', url: '/dashboard/user' },
      { text: 'Courses', icon: 'mdi-book-account', url: '/' },
      { text: 'Activity', icon: 'mdi-timeline', url: '/' },
      { text: 'Alerts', icon: 'mdi-bell-alert', url: '/dashboard/alerts' },
      { text: 'Findings', icon: 'mdi-magnify-expand', url: '/dashboard/findings' },
      { text: 'Case', icon: 'mdi-cloud-upload', url: '/' },
      { text: 'Backup Data', icon: 'mdi-cloud-download', url: '/dashboard/backup' },
      { text: 'Threshold', icon: 'mdi-speedometer', url: '/dashboard/threshold' },
      { text: 'Calender', icon: 'mdi-calendar-month', url: '/dashboard/calendar' },
    ],
  }),
  setup() {


    return {}
  }
}
</script>
