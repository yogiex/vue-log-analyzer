<template>
  <v-container>
    <v-row>
      <v-col v-for="(item, i) in thresholds" :key="i" cols="12" md="4">
        <v-card :title="item.title" variant="tonal">
          <v-container>
            <v-text-field v-model="item.value" variant="outlined" label="Insert Threshold" />
            <v-divider />
            <v-card-actions>
              <v-btn color="primary" @click="submitThreshold(i)">Submit</v-btn>
            </v-card-actions>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

const thresholds = ref([
  { title: 'Listening Threshold', value: '' },
  { title: 'Grammar Threshold', value: '' },
  { title: 'Reading Threshold', value: '' },
  { title: 'Writing Threshold', value: '' },
  { title: 'Speaking Threshold', value: '' },
  { title: 'Overall Threshold', value: '' },
])

function submitThreshold(index) {
  console.log('Submit threshold', index, thresholds.value[index].value)
}
</script>
