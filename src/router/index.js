import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '@/layouts/dashboard/DashboardLayout.vue'
import { useAuth } from '@/composables/useAuth'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/login.vue'),
  },
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'dashboard', component: () => import('@/pages/dashboard/index.vue') },
      { path: 'users', name: 'users', component: () => import('@/pages/dashboard/user.vue') },
      { path: 'logs', name: 'logs', component: () => import('@/pages/dashboard/logs.vue') },
      { path: 'alerts', name: 'alerts', component: () => import('@/pages/dashboard/alerts.vue') },
      { path: 'findings', name: 'findings', component: () => import('@/pages/dashboard/findings/index.vue') },
      { path: 'findings/:id', name: 'findings-detail', component: () => import('@/pages/dashboard/findings/[id].vue') },
      { path: 'calendar', name: 'calendar', component: () => import('@/pages/dashboard/calendar.vue') },
      { path: 'monitoring', name: 'monitoring', component: () => import('@/pages/dashboard/monitoring.vue') },
      { path: 'backups', name: 'backups', component: () => import('@/pages/dashboard/backup.vue') },
      { path: 'backups/:id', name: 'backups-detail', component: () => import('@/pages/dashboard/downloads/[id].vue') },
      { path: 'thresholds', name: 'thresholds', component: () => import('@/pages/dashboard/threshold.vue') },
      { path: 'systems', name: 'systems', component: () => import('@/pages/dashboard/systems.vue') },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return '/login'
  }
})

export default router
