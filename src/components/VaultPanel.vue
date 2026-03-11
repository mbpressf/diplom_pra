<script setup>
import { computed, reactive, watch } from 'vue'

import { useLocale } from '../composables/useLocale'
import { useFinanceStore } from '../store/finance'

const props = defineProps({
  vault: {
    type: Object,
    required: true,
  },
})

const financeStore = useFinanceStore()
const { t, money, displayMoney, fromBase, toBase, uiStore } = useLocale()

const transferForm = reactive({
  amount: '',
  mode: 'deposit',
})

const settingsForm = reactive({
  name: '',
  target_amount: '',
})

const status = reactive({
  type: '',
  text: '',
})

const quickAmounts = [500, 1000, 2500, 5000]

const displayName = computed(() => props.vault.name || t('vaultFallbackName'))

watch(
  [() => props.vault, () => uiStore.locale],
  ([value]) => {
    settingsForm.name = value?.name || t('vaultFallbackName')
    settingsForm.target_amount = value?.target_amount ? String(fromBase(value.target_amount)) : ''
  },
  { immediate: true, deep: true },
)

const progressWidth = computed(() => `${Math.min(props.vault.progress_percent || 0, 100)}%`)
const isDepositMode = computed(() => transferForm.mode === 'deposit')
const availabilityClass = computed(() =>
  props.vault.available_to_spend >= 0
    ? 'text-cyan-700 dark:text-cyan-300'
    : 'text-expense',
)
const equationText = computed(() =>
  `${money(props.vault.balance)} + ${money(props.vault.available_to_spend)} = ${money(props.vault.net_balance)}`,
)
const modeTitle = computed(() => (isDepositMode.value ? t('vaultModeDepositTitle') : t('vaultModeWithdrawTitle')))
const modeHint = computed(() =>
  isDepositMode.value
    ? t('vaultModeDepositHint')
    : t('vaultModeWithdrawHint'),
)

function setQuickAmount(amount) {
  transferForm.amount = String(amount)
}

function normalizeVaultError(error, fallback) {
  if (error?.response?.status === 401) {
    return t('vaultSessionExpired')
  }
  return error?.response?.data?.detail || fallback
}

async function submitTransfer() {
  const amount = toBase(Number(transferForm.amount))
  if (!amount) return

  status.type = ''
  status.text = ''

  try {
    if (isDepositMode.value) {
      await financeStore.depositToVault(amount)
      status.type = 'success'
      status.text = t('vaultSuccessDeposit')
    } else {
      await financeStore.withdrawFromVault(amount)
      status.type = 'success'
      status.text = t('vaultSuccessWithdraw')
    }
    transferForm.amount = ''
  } catch (error) {
    status.type = 'error'
    status.text = normalizeVaultError(error, t('vaultErrorAction'))
  }
}

async function saveSettings() {
  status.type = ''
  status.text = ''

  try {
    await financeStore.updateVault({
      name: settingsForm.name.trim() || t('vaultFallbackName'),
      target_amount: toBase(Number(settingsForm.target_amount || 0)),
    })
    status.type = 'success'
    status.text = t('vaultSuccessSave')
  } catch (error) {
    status.type = 'error'
    status.text = normalizeVaultError(error, t('vaultErrorSave'))
  }
}
</script>

<template>
  <article class="vault-shell relative overflow-hidden rounded-[30px] border border-white/15 p-4 shadow-[0_26px_70px_rgba(2,6,23,0.14)] sm:p-5 lg:p-6">
    <div class="vault-glow vault-glow-a"></div>
    <div class="vault-glow vault-glow-b"></div>

    <div class="relative z-[1] grid gap-5 xl:grid-cols-[1.05fr_0.95fr] xl:items-start">
      <div class="space-y-4">
        <div class="inline-flex items-center rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.28em] text-slate-600 dark:text-slate-300">
          {{ t('vaultBadge') }}
        </div>

        <div class="space-y-2.5">
          <h2 class="display-type text-2xl font-semibold tracking-tight text-slate-950 dark:text-slate-50 sm:text-3xl">
            {{ displayName }}
          </h2>
          <p class="max-w-2xl text-sm leading-6 text-slate-600 dark:text-slate-300">
            {{ t('vaultDescription') }}
          </p>
        </div>

        <div class="rounded-[26px] border border-white/15 bg-[linear-gradient(135deg,rgba(255,255,255,0.78),rgba(255,255,255,0.46))] p-3.5 dark:bg-[linear-gradient(135deg,rgba(6,15,29,0.78),rgba(10,20,36,0.52))] sm:p-4">
          <p class="text-xs uppercase tracking-[0.24em] text-slate-500 dark:text-slate-400">{{ t('vaultHowToCount') }}</p>
          <div class="mt-3 grid grid-cols-3 gap-2.5 lg:flex lg:flex-row lg:items-center">
            <div class="vault-metric vault-metric-total">
              <span class="vault-metric-label">
                <span class="sm:hidden">{{ t('vaultTotalShort') }}</span>
                <span class="hidden sm:inline">{{ t('vaultTotal') }}</span>
              </span>
              <strong>{{ money(props.vault.net_balance) }}</strong>
            </div>
            <div class="hidden text-2xl font-light text-slate-400 lg:block">=</div>
            <div class="vault-metric vault-metric-safe">
              <span class="vault-metric-label">
                <span class="sm:hidden">{{ t('vaultInSafeShort') }}</span>
                <span class="hidden sm:inline">{{ t('vaultInSafe') }}</span>
              </span>
              <strong>{{ money(props.vault.balance) }}</strong>
            </div>
            <div class="hidden text-2xl font-light text-slate-400 lg:block">+</div>
            <div class="vault-metric vault-metric-free">
              <span class="vault-metric-label">
                <span class="sm:hidden">{{ t('vaultFreeShort') }}</span>
                <span class="hidden sm:inline">{{ t('vaultFree') }}</span>
              </span>
              <strong :class="availabilityClass">{{ money(props.vault.available_to_spend) }}</strong>
            </div>
          </div>
          <p class="mt-3 text-sm text-slate-500 dark:text-slate-400">{{ equationText }}</p>
        </div>

        <div class="rounded-[26px] border border-white/15 bg-slate-950/5 p-4 dark:bg-white/5">
          <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p class="text-sm font-semibold text-slate-800 dark:text-slate-100">{{ t('vaultGoalTitle') }}</p>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
                {{ props.vault.target_amount > 0 ? money(props.vault.target_amount) : t('vaultGoalEmpty') }}
              </p>
            </div>
            <p class="text-lg font-semibold text-slate-700 dark:text-slate-200">{{ props.vault.progress_percent }}%</p>
          </div>
          <div class="mt-4 h-3 overflow-hidden rounded-full bg-slate-200/80 dark:bg-slate-800/80">
            <div class="h-full rounded-full bg-[linear-gradient(90deg,#2563eb,#06b6d4,#10b981)] transition-all duration-500" :style="{ width: progressWidth }"></div>
          </div>
        </div>
      </div>

      <div class="space-y-3">
        <section class="vault-action-panel">
          <div class="grid grid-cols-2 gap-2 rounded-[22px] bg-slate-950/5 p-1 dark:bg-white/5">
            <button
              type="button"
              class="rounded-[18px] px-4 py-3 text-sm font-semibold transition"
              :class="isDepositMode ? 'bg-[linear-gradient(90deg,#1d4ed8,#10b981)] text-white shadow-[0_12px_30px_rgba(29,78,216,0.28)]' : 'text-slate-500 dark:text-slate-300'"
              @click="transferForm.mode = 'deposit'"
            >
              {{ t('vaultToSafe') }}
            </button>
            <button
              type="button"
              class="rounded-[18px] px-4 py-3 text-sm font-semibold transition"
              :class="!isDepositMode ? 'bg-slate-950 text-white shadow-[0_12px_30px_rgba(15,23,42,0.18)] dark:bg-white dark:text-slate-950' : 'text-slate-500 dark:text-slate-300'"
              @click="transferForm.mode = 'withdraw'"
            >
              {{ t('vaultFromSafe') }}
            </button>
          </div>

          <div class="mt-4">
            <h3 class="text-xl font-semibold text-slate-900 dark:text-slate-50">{{ modeTitle }}</h3>
            <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{{ modeHint }}</p>
          </div>

          <div class="mt-4 flex flex-wrap gap-2">
            <button
              v-for="amount in quickAmounts"
              :key="amount"
              type="button"
              class="rounded-full border border-white/15 bg-white/65 px-3 py-2 text-sm font-medium text-slate-700 transition hover:-translate-y-0.5 hover:bg-white dark:bg-slate-950/45 dark:text-slate-200 dark:hover:bg-slate-900"
              @click="setQuickAmount(amount)"
            >
              {{ displayMoney(amount) }}
            </button>
          </div>

          <div class="mt-4 grid gap-3 sm:grid-cols-[1fr_auto]">
            <input
              v-model="transferForm.amount"
              type="number"
              min="0"
              step="0.01"
              :placeholder="t('vaultTransferPlaceholder')"
              class="rounded-[20px] border border-white/15 bg-white/80 px-4 py-3.5 text-base dark:bg-slate-950/45"
            />
            <button
              type="button"
              class="rounded-[20px] bg-[linear-gradient(90deg,#1d4ed8,#10b981)] px-6 py-3.5 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:shadow-[0_16px_30px_rgba(14,165,233,0.2)]"
              @click="submitTransfer"
            >
              {{ isDepositMode ? t('vaultDepositButton') : t('vaultWithdrawButton') }}
            </button>
          </div>
        </section>

        <section class="vault-action-panel">
          <div>
            <h3 class="text-xl font-semibold text-slate-900 dark:text-slate-50">{{ t('vaultSettingsTitle') }}</h3>
            <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
              {{ t('vaultSettingsText') }}
            </p>
          </div>

          <div class="mt-4 grid gap-3">
            <input
              v-model="settingsForm.name"
              type="text"
              maxlength="64"
              :placeholder="t('vaultNamePlaceholder')"
              class="rounded-[20px] border border-white/15 bg-white/80 px-4 py-3.5 dark:bg-slate-950/45"
            />
            <div class="grid gap-3 sm:grid-cols-[1fr_auto]">
              <input
                v-model="settingsForm.target_amount"
                type="number"
                min="0"
                step="0.01"
                :placeholder="t('vaultTargetPlaceholder')"
                class="rounded-[20px] border border-white/15 bg-white/80 px-4 py-3.5 dark:bg-slate-950/45"
              />
              <button
                type="button"
                class="rounded-[20px] border border-white/15 px-6 py-3.5 text-sm font-semibold text-slate-700 transition hover:bg-white dark:text-slate-100 dark:hover:bg-slate-800"
                @click="saveSettings"
              >
                {{ t('save') }}
              </button>
            </div>
          </div>

          <p
            v-if="status.text"
            class="mt-4 text-sm"
            :class="status.type === 'error' ? 'text-expense' : 'text-income'"
          >
            {{ status.text }}
          </p>
        </section>
      </div>
    </div>
  </article>
</template>
