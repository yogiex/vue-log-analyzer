<script>
import navbarLayout from '@/layouts/dashboard/navbarLayout.vue'
import sidebarLayout from '@/layouts/dashboard/sidebarLayout.vue'
import ex1 from './ex1.vue'
import ex2 from './ex2.vue'
export default {
    components: {navbarLayout,sidebarLayout},
    methods: {
        showSesi1(){
            this.currentComponent = ex1
        },
        showSesi2(){
            this.currentComponent = ex2
        },
        showSesi3(){},
        showSesi4(){}
    },
    data: () => ({
        currentComponent: null,
        users:  [
        {
            "nama": "Cameron",
            "ip_address": "126.246.120.31",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Buck",
            "ip_address": "255.162.171.92",
            "img": "/public/user_456141.png",
            "status" : "bad"
        },
        {
            "nama": "Geovanni",
            "ip_address": "210.97.101.185",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Carmel",
            "ip_address": "219.218.21.209",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Buddy",
            "ip_address": "106.113.177.207",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Marge",
            "ip_address": "48.44.158.104",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Max",
            "ip_address": "219.44.100.177",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Anderson",
            "ip_address": "90.222.115.117",
            "img": "/public/user_456141.png",
            "status" : "bad"
        },
        {
            "nama": "Bartholome",
            "ip_address": "226.35.252.40",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Katherine",
            "ip_address": "4.24.53.4",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Sonny",
            "ip_address": "178.234.93.28",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Erica",
            "ip_address": "168.33.31.211",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Dolores",
            "ip_address": "108.200.65.186",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Nestor",
            "ip_address": "15.183.109.37",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Kaleb",
            "ip_address": "234.130.24.201",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "John",
            "ip_address": "153.5.43.225",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Libby",
            "ip_address": "196.148.18.80",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Deion",
            "ip_address": "136.237.97.201",
            "img": "/public/user_456141.png",
            "status" : "good"
        },
        {
            "nama": "Tyler",
            "ip_address": "172.66.112.226",
            "img": "/public/user_456141.png",
            "status" : "bad"
        },
        {
            "nama": "Mac",
            "ip_address": "43.23.229.99",
            "img": "/public/user_456141.png",
            "status" : "good"

        }
    ]
    })
}
</script>

<template>
    <navbarLayout/>
    <sidebarLayout/>
    <v-main>
        <v-container>
            <v-row>
                <v-col>
                    <v-btn variant="outlined" @click="showSesi1" class="ma-4">sesi 1</v-btn>
                    <!-- <button @click="showSesi1">sesi 1</button> -->
                    <v-btn variant="outlined" @click="showSesi2" class="ma-4">sesi 2</v-btn>
                    <v-btn variant="outlined" class="ma-4">sesi 3</v-btn>
                </v-col>
            </v-row>
        </v-container>
        <v-container class="d-flex align-content-start flex-wrap" fluid>
            <v-card v-for="(user, i) in users" class="ma-3 ma-3" :elevation="5">
                <v-card-title> {{ user.nama }}</v-card-title>
                <v-img
                :src="user.img"
                width="150px"
                height="150px"
                >
                </v-img>
                <v-card-actions>
                   <p>Status : </p> <v-btn class="ml-2" :color="user.status == 'bad' ? 'red': 'green'">{{ user.status }}</v-btn>
                   <v-btn prepend-icon="mdi-open-in-new">Details</v-btn>
                </v-card-actions>
            </v-card>
        </v-container>

        <!-- <div :is="currentComponent">

        </div> -->
        <!-- <v-container v-if="!showSession">
            <h1>sesi 3</h1>
        </v-container>
        <v-container v-if="!showSession">
            <h1>sesi 4</h1>
        </v-container> -->
    </v-main>
</template>
