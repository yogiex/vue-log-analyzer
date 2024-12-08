/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { getAuth, onAuthStateChanged } from "firebase/auth";
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
})

export default router
