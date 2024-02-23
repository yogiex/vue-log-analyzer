<template>
  <!-- <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    
    
    <div class="search-box">
      <h1>tes</h1>
    </div>
      <v-main class="d-flex align-center justify-center content-main" >
        <h1>tes heloo</h1>
      </v-main>
    </v-layout> -->
</template>

<script>
import navbarLayout from './navbarLayout.vue';
import sidebarLayout from './sidebarLayout.vue';
export default {
    components: {
      navbarLayout,
      sidebarLayout
    },
   data: () => ({
      items: [
        { text: 'My Files', icon: 'mdi-folder' },
        { text: 'Shared with me', icon: 'mdi-account-multiple' },
        { text: 'Starred', icon: 'mdi-star' },
        { text: 'Recent', icon: 'mdi-history' },
        { text: 'Offline', icon: 'mdi-check-circle' },
        { text: 'Uploads', icon: 'mdi-upload' },
        { text: 'Backups', icon: 'mdi-cloud-upload' },
      ],
    }),
    setup () {
        

        return {}
    }
}
</script>

<style lang="scss" scoped>

</style>