import { createWebHistory, createRouter } from "vue-router";
import HomeComponents from "./components/HomeComponents.vue";
import DashboardComponents from "./components/DashboardComponent.vue";
import UsersComponent from "../src/components/UsersComponent.vue";
const routes = [
  { path: "/home", component: HomeComponents },
  { path: "/dashboard", component: DashboardComponents },
  { path: "/dashboard/users", component: UsersComponent },
];

const router = createRouter({
  history: createWebHistory(),
  routes, // short for `routes: routes`
});

export default router;
