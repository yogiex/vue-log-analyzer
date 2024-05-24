<template>
    <v-layout class="rounded rounded-md" style="min-height: 100vh;">
        <NavbarLayout/>
        <SidebarLayout/>
        <v-main>
            <v-card
             flat
             title="User Filter"
            >
            <template v-slot:text>
            <v-text-field
                v-model="search"
                label="Search"
                prepend-inner-icon="mdi-magnify"
                single-line
                variant="outlined"
                hide-details
            ></v-text-field>
            </template>

            <v-data-table
            :headers="headers"
            :items="items"
            :search="search"
            >
            <template v-slot:item.status="{ item }">
                <div class="text-end">
                <v-chip
                    :color="item.stock ? 'green' : 'red'"
                    :text="item.stock ? 'Safe' : 'Warning'"
                    class="text-uppercase"
                    label
                    size="small"
                ></v-chip>
                </div>
            </template>
        </v-data-table>
        </v-card>
        </v-main>
    </v-layout>
</template>

<script>

import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios'
let jsonData = []
const consumeUser = () => {
    jsonData.push(axios.get('http://localhost:3000/users'))
    return jsonData
}
export default {
    components: {NavbarLayout, SidebarLayout},
    data() {
        return {
            search: '',
            headers: [
            {
                align: 'start',
                key: 'name',
                sortable: false,
                title: 'Username',
            },
            { key: 'first_ip', title: 'First IP' },
            { key: 'last_ip', title: 'Last IP' },
            { key: 'last_access', title: 'Last Access' },
            { key: 'user_agent', title: 'User-Agent' },
            { key: 'status', title: 'Status' },
            ],
            items: jsonData,
        }
    },
}
</script>