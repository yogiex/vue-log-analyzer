<template>
        <v-navigation-drawer
        image="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg"
        permanent
        theme="dark">
       <v-list
          :lines="false"
          density="compact"
          nav
        >
          <v-list-item
            v-for="(item, i) in items"
            :key="i"
            :value="item"

            :to=item.url
          >
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
        { text: 'Home', icon: 'mdi-folder' , url:'/dashboard'},
        { text: 'Users', icon: 'mdi-account-multiple',url: '/dashboard/user' },
        { text: 'Monitoring', icon: 'mdi-monitor-account',url: '/dashboard/monitoring' },
        { text: 'Courses', icon: 'mdi-book-account', url:'#' },
        { text: 'Activity', icon: 'mdi-history', url:'#' },
        { text: 'Alerts', icon: 'mdi-check-circle',url:'/dashboard/alerts' },
        { text: 'Findings', icon: 'mdi-upload' , url:'/dashboard/findings'},
        { text: 'Case', icon: 'mdi-cloud-upload', url:'#' },
        { text: 'Reporting', icon: 'mdi-file-pdf-box', url:'/dashboard/reporting' },
        { text: 'Backup Data', icon: 'mdi-cog', url:'/dashboard/backup' },
        { text: 'Threshold', icon: 'mdi-cog', url:'/dashboard/threshold' },
      ],
    }),
    setup () {


        return {}
    }
}
</script>
