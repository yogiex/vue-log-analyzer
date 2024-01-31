import {createWebHistory, createRouter} from 'vue-router'
import HomeComponents from './components/HomeComponents.vue'
import DashboardComponents from './components/DashboardComponent.vue'
const routes = [
    { path: '/home', component: HomeComponents },
    { path: '/dashboard', component: DashboardComponents}
    
  ]
  

  const router = createRouter({
    history: createWebHistory(),
    routes, // short for `routes: routes`
  })

  export default router