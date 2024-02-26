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
            color="primary"
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
        { text: 'My Files', icon: 'mdi-folder' , url:'dashboard'},
        { text: 'Users', icon: 'mdi-account-multiple',url: 'users' },
        { text: 'Courses', icon: 'mdi-star', url:'dashboard' },
        { text: 'Activity', icon: 'mdi-history', url:'dashboard' },
        { text: 'Alerts', icon: 'mdi-check-circle',url:'alerts' },
        { text: 'Findings', icon: 'mdi-upload' , url:'dashboard'},
        { text: 'Case', icon: 'mdi-cloud-upload', url:'dashboard' },
        { text: 'Timelines', icon: 'mdi-cloud-upload', url:'dashboard' },
        { text: 'Explore', icon: 'mdi-cloud-upload', url:'dashboard' },
      ],
    }),
    setup () {
        

        return {}
    }
}
</script>