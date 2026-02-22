<script setup>
import { computed, onMounted } from 'vue'
import { RouterView } from 'vue-router'

import AppHeader from './components/AppHeader.vue'
import { useAuthStore } from './store/auth'
import { useFinanceStore } from './store/finance'
import { useUiStore } from './store/ui'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const uiStore = useUiStore()

const isAuthed = computed(() => !!authStore.token)

onMounted(async () => {
  uiStore.initTheme()
  if (authStore.token) {
    await financeStore.bootstrap()
  }
})
</script>

<template>
  <div class="app-bg min-h-screen">
    <AppHeader v-if="isAuthed" />
    <main class="mx-auto max-w-7xl px-4 pb-10 pt-6 sm:px-6 lg:px-8">
      <RouterView v-slot="{ Component }">
        <Transition name="route-fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>
