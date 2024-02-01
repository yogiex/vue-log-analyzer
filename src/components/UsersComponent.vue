<template>
    <v-layout class="rounded rounded-md">
        <NavbarViews/>
        <SidebarViews/>
        <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
            <UsersViews/>
        </v-main>
    </v-layout>
    

</template>


<script>
import SidebarViews from '../views/dashboard/SidebarViews.vue';
import NavbarViews from '../views/dashboard/NavbarViews.vue'
import UsersViews from '../views/dashboard/UsersViews.vue';

export default {
    name: "UsersComponent",
    components: {
        SidebarViews,
        NavbarViews,
        UsersViews
    }
}
</script>