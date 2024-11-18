<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout />
    <SidebarLayout />
    <v-main>
      <!-- <v-card class="mx-auto" max-width="344" title="User Threshold">
        <v-container>
      <v-row>
        <v-col>
            <v-text-field
        v-model="listeningTimetaken"
        color="primary"
        label="Listening Time taken"
        variant="underlined"
      ></v-text-field>
        </v-col>
        <v-col>
            <v-text-field
        v-model="listeningScore"
        color="primary"
        label="Listening Score"
        variant="underlined"
      ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
            <v-text-field
        v-model="grammarTimetaken"
        color="primary"
        label="Grammar Time taken"
        variant="underlined"
      ></v-text-field>
        </v-col>
        <v-col>
            <v-text-field
        v-model="grammarScore"
        color="primary"
        label="Grammar score"
        placeholder=""
        variant="underlined"
      ></v-text-field>
        </v-col>
      </v-row>



      <v-row>
        <v-col>
            <v-text-field
        v-model="readingTimetaken"
        color="primary"
        label="Reading Time taken"
        variant="underlined"
      ></v-text-field>
        </v-col>
        <v-col>
            <v-text-field
        v-model="readingScore"
        color="primary"
        label="Reading Score"
        variant="underlined"
      ></v-text-field>
        </v-col>
      </v-row>

    </v-container>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="success">
            Complete Threshold

            <v-icon icon="mdi-chevron-right" end></v-icon>
          </v-btn>
        </v-card-actions>
      </v-card> -->
      <v-container>
        <v-row>
          <v-col>
            <v-card title="Treshold" variant="tonal">
              <v-container>
                <v-text-field variant="outlined" label="Insert Treshold">

                </v-text-field>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-btn color="blue-accent-3">
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-container>
            </v-card>
          </v-col>
          <v-col>
            <v-card title="Treshold" variant="tonal">
              <v-container>
                <v-text-field variant="outlined" label="Insert Treshold">

                </v-text-field>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-btn color="blue-accent-3">
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-container>
            </v-card>
          </v-col>
          <v-col>
            <v-card title="Treshold" variant="tonal">
              <v-container>
                <v-text-field variant="outlined" label="Insert Treshold">

                </v-text-field>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-btn color="blue-accent-3">
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-container>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-card title="Treshold" variant="tonal">
              <v-container>
                <v-text-field variant="outlined" label="Insert Treshold">

                </v-text-field>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-btn color="blue-accent-3">
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-container>
            </v-card>
          </v-col>
          <v-col>
            <v-card title="Treshold" variant="tonal">
              <v-container>
                <v-text-field variant="outlined" label="Insert Treshold">

                </v-text-field>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-btn color="blue-accent-3">
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-container>
            </v-card>
          </v-col>
          <v-col>
            <v-card title="Treshold" variant="tonal">
              <v-container>
                <v-text-field variant="outlined" label="Insert Treshold">

                </v-text-field>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-btn color="blue-accent-3">
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-container>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-layout>
</template>

<script>

import dashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios';
export default {
  components: { dashboardLayout, SidebarLayout, NavbarLayout },
  methods: {
    async pushThreshold() {

    }
  }
}
</script>
