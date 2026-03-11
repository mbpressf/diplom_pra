import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../store/auth'
import AnalyticsView from '../views/AnalyticsView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import LoginView from '../views/LoginView.vue'
import OverviewView from '../views/OverviewView.vue'
import RegisterView from '../views/RegisterView.vue'
import TransactionsView from '../views/TransactionsView.vue'
import VaultView from '../views/VaultView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/', name: 'overview', component: OverviewView, meta: { requiresAuth: true } },
  { path: '/analytics', name: 'analytics', component: AnalyticsView, meta: { requiresAuth: true } },
  { path: '/vault', name: 'vault', component: VaultView, meta: { requiresAuth: true } },
  { path: '/transactions', name: 'transactions', component: TransactionsView, meta: { requiresAuth: true } },
  { path: '/categories', name: 'categories', component: CategoriesView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    return { name: 'login' }
  }
  if (to.meta.guestOnly && authStore.token) {
    return { name: 'overview' }
  }
  return true
})

export default router
