<template>
    <v-layout class="rounded rounded-md" style="min-height: 100vh;">
        <NavbarLayout/>
        <SidebarLayout/>
        <v-main class="align-center justify-center" style="min-height: 500px;">
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field
                        label="Label"
                        prepend-icon="$vuetify"
                        variant="outlined"
                        ></v-text-field>
                    </v-col>
                </v-row>
            </v-container>
            <v-container>
                <v-row>
                    <!-- <v-col v-for="n in 4" :key="n" cols="12" sm="3">
                        <v-sheet class="ma-2 pa-2">tes input</v-sheet>
                    </v-col> -->
                    <v-col>
                        <v-select
                            label="Status"
                            :items="['Open','Closed','On Progress']"
                            variant="outlined"
                        ></v-select>
                    </v-col>
                </v-row>
            </v-container>
            <v-data-table
                :headers="headers"
                :items="dataPeserta"
                :search="search"
            >
            <template v-slot:item.status="{ item }">
                <div class="text-center" >
                <v-chip
                    :color="dataPeserta.status == 'terindikasi' ? 'green' : 'red'"
                    :text="dataPeserta.status == 'terindikasi' ? 'Aman' : 'Terindikasi'"
                    class="text-uppercase"
                    label
                    size="small"
                ></v-chip>
                </div>
            </template>
            <template v-slot:item.track_progress="{item}">
                <!-- <div class="text-end" >
                    <v-select
                    :label="Select"
                    :items="dataPeserta.track_progress == 'open' ? ['OPEN']: ['CLOSED']"
                    variant="outlined"
                    ></v-select>
                </div> -->
                <div class="text-end" >
                    <v-select
                    :label="Select"
                    :items="dataPeserta.track_progress == 'open' ? ['OPEN'] : ['CLOSED']"
                    variant="outlined"
                    ></v-select>
                </div>
            </template>
            </v-data-table>
        </v-main>
    </v-layout>
</template>

<script>

import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios';
let url = 'http://180.250.135.11:5000'
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
        { key: 'timestart', title: 'Time Start' },
        { key: 'timefinish', title: 'Time Finished' },
        { key: 'timedate', title: 'Time Date' },
        { key: 'time_taken', title: 'Durasi Pengerjaan' },
        { key: 'score', title: 'Nilai' },
        { key: 'status', title: 'Status' },
        { key: 'track_progress', title: 'Progress'}
        ],
        dataPeserta: [],
    }
},
mounted(){
    axios.get(`${url}/api/get_cases`)
         .then(val =>{
            val.data.map(v => this.dataPeserta.push(v))
            this.dataPeserta = val.data
            console.log(this.dataPeserta)
         })
}

}
</script>
