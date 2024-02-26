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
                    <v-col>
                        <v-select
                            label="Status"
                            :items="['Open','Closed','On Progress']"
                            variant="outlined"
                        ></v-select>
                    </v-col>
                    <v-col>
                        <v-select
                            label="Status"
                            :items="['Open','Closed','On Progress']"
                            variant="outlined"
                        ></v-select>
                    </v-col>
                    <v-col>
                        <v-select
                            label="Status"
                            :items="['Open','Closed','On Progress']"
                            variant="outlined"
                        ></v-select>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-layout>
</template>

<script>

import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';

export default {
    components: {NavbarLayout, SidebarLayout}
}
</script>