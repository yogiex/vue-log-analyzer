<template>
    <v-layout class="rounded rounded-md" style="min-height: 100vh;">
        <NavbarLayout/>
        <SidebarLayout/>
        <v-main>
            <h1>tes sistem setting</h1>
        </v-main>
    </v-layout>
</template>

<script>

import dashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';

export default {
    components: { dashboardLayout, SidebarLayout, NavbarLayout },
}
</script>