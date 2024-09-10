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

            
            <!-- <v-data-table
                    :headers="headers"
                    :items="dataPeserta"
                    :search="search"
            >
            </v-data-table> -->
            
            <v-data-table
            :headers="headers"
            :items="dataPeserta"
            :search="search"
            >
            <template v-slot:item.status="{ item }">
                <div class="">
                    <v-chip
                    :text="dataPeserta.status == 'aman' ? 'Warning' : 'Safe'"
                    :color="dataPeserta.status == 'aman' ? 'red' : 'green'" 
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
import axios from 'axios';
let url = `${import.meta.env.VITE_APP_URL_ENDPOINT}`

export default {
    components: {NavbarLayout, SidebarLayout},
    data() {
        
            return {
                search: '',
                headers: [
                { key: 'userid', title: 'User ID' },
                {
                    align: 'start',
                    key: 'firstname',
                    sortable: false,
                    title: 'Username',
                },
                { key: 'lastname', title: 'Full Name' },
                { key: 'timedate', title: 'Timedate' },
                { key: 'timestart', title: 'Time Start' },
                { key: 'timefinish', title: 'Time Finished' },
                { key: 'time_taken', title: 'Durasi Pengerjaan' },
                { key: 'session', title: 'Sesi Pengerjaan'},
                { key: 'score', title: 'Nilai' },
                { key: 'status', title: 'Status' },
                ],
                dataPeserta: [],  
        } 
    },
    mounted(){
        axios.get(`${url}/api/daftar_peserta`)
             .then(val =>{
                val.data.map(v => this.dataPeserta.push(v))
                this.dataPeserta = val.data
                console.log(this.dataPeserta)
             })
        console.log(`${url}/api/daftar_peserta`)
    }
}
</script>