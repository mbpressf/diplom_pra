import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../store/auth'
import AnalyticsView from '../views/AnalyticsView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import LoginView from '../views/LoginView.vue'
import OrgExportsView from '../views/OrgExportsView.vue'
import OrganizationView from '../views/OrganizationView.vue'
import OrgReportsView from '../views/OrgReportsView.vue'
import OverviewView from '../views/OverviewView.vue'
import PricingView from '../views/PricingView.vue'
import RegisterView from '../views/RegisterView.vue'
import TransactionsView from '../views/TransactionsView.vue'
import VaultView from '../views/VaultView.vue'

function homeByAccountType(accountType) {
  return accountType === 'organization' ? { name: 'organization' } : { name: 'overview' }
}

const routes = [
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/', name: 'overview', component: OverviewView, meta: { requiresAuth: true, accountTypes: ['individual'] } },
  { path: '/analytics', name: 'analytics', component: AnalyticsView, meta: { requiresAuth: true, accountTypes: ['individual'] } },
  { path: '/vault', name: 'vault', component: VaultView, meta: { requiresAuth: true, accountTypes: ['individual'] } },
  { path: '/transactions', name: 'transactions', component: TransactionsView, meta: { requiresAuth: true, accountTypes: ['individual'] } },
  { path: '/categories', name: 'categories', component: CategoriesView, meta: { requiresAuth: true, accountTypes: ['individual'] } },
  { path: '/org', name: 'organization', component: OrganizationView, meta: { requiresAuth: true, accountTypes: ['organization'] } },
  { path: '/org/reports', name: 'org-reports', component: OrgReportsView, meta: { requiresAuth: true, accountTypes: ['organization'] } },
  { path: '/org/exports', name: 'org-exports', component: OrgExportsView, meta: { requiresAuth: true, accountTypes: ['organization'] } },
  { path: '/pricing', name: 'pricing', component: PricingView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    return { name: 'login' }
  }

  if (authStore.token && !authStore.profileLoaded) {
    try {
      await authStore.loadProfile()
    } catch {
      return { name: 'login' }
    }
  }

  if (to.meta.guestOnly && authStore.token) {
    return homeByAccountType(authStore.accountType)
  }

  const allowedAccountTypes = to.meta.accountTypes
  if (to.meta.requiresAuth && Array.isArray(allowedAccountTypes) && !allowedAccountTypes.includes(authStore.accountType)) {
    return homeByAccountType(authStore.accountType)
  }

  return true
})

export default router
