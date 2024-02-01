<template>
    <v-navigation-drawer color="blue">
      <v-list>
        <v-list-item prepend-icon="" title="General" value="inbox" to="/dashboard" link></v-list-item>
        <v-list-item prepend-icon="" title="Users" value="users" to="/dashboard/users" link></v-list-item>
        <v-list-item prepend-icon="" title="Courses" value="inbox"></v-list-item>
        <v-list-item prepend-icon="" title="Activity" value="inbox"></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </template>

<script>
export default {
    name: 'SidebarViews'
}
</script>

<style scoped>

</style>