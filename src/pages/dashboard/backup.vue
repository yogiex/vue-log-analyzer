<template>
    <v-layout class="rounded rounded-md" style="min-height: 100vh;">
      <NavbarLayout/>
      <SidebarLayout/>
      <v-main>
        <v-container>
            <h1>
                Backup Data 
            </h1>
            <v-btn variant="tonal" @click="backup()">
                    Backup!!
            </v-btn>
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
                :items="dataFiles"
                :search="search"
            >
            </v-data-table>
        </v-container>
      </v-main>
      
    </v-layout>
</template>
  
<script>
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios';
let urlEndpoint = import.meta.env.urlFlask 

export default {
    components: {NavbarLayout,SidebarLayout},
    methods: {
        async backup(){
            const response = await axios.post(`${urlEndpoint}/dump`)
            console.log(urlEndpoint)
            console.log(response)
            alert(response.data)
            window.location.reload();
        }
    },
    data() {
        
        return {
            search: '',
            headers: [
            { key: 'title', title: 'Title' },
            { key: 'url', title: 'Url' },
            ],
            dataFiles: [],  
        }
    },
    async mounted() {
        // axios.get(`${urlEndpoint}/directory`)
        //     .then(val => {
        //         val.data.map(v => this.dataFiles.push(v))
        //         this.dataFiles = val.data 
        //         console.log(this.dataFiles)
        //     })
        const response = await axios.get(`${urlEndpoint}/directory`)
        console.log(response)
            console.log(`${urlEndpoint}/directory`)
    }
}
</script>
  