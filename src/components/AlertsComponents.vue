<template>
    <v-layout class="rounded rounded-md">
        <NavbarViews/>
        <SidebarViews/>
        <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
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
import NavbarViews from '../views/dashboard/NavbarViews.vue';
import SidebarViews from '../views/dashboard/SidebarViews.vue';
export default {
    name: 'AlertComponents',
    components: {
        NavbarViews,
        SidebarViews
    }
}
</script>