<template>
  <div>
    <h1>{{ datas }}</h1>
    <h1>{{ $route.params.id }}</h1>
  </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router'
const route = useRoute();
// let param = route.params.id
// console.log(route.params.id)
export default {
  data() {
    return {
      datas: [],
    }
  },
  setup() {


    return {}
  }, mounted() {
    axios.get(`http://localhost:3000/example-kasus.json`)
      .then(val => {
        val.data.map(v => {
          this.datas.push(v)
        })
      })
  }
}
</script>

<style lang="scss" scoped></style>
