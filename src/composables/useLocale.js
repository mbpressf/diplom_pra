import { computed } from 'vue'

import {
  formatMoneyDisplay,
  formatShortDate,
  tFor,
} from '../utils/locale'
import { useUiStore } from '../store/ui'

export function useLocale() {
  const uiStore = useUiStore()

  const locale = computed(() => 'ru')
  const currencyCode = computed(() => 'RUB')

  function t(key, params) {
    return tFor('ru', key, params)
  }

  function money(amount) {
    return formatMoneyDisplay(amount, 'ru', 'RUB')
  }

  function displayMoney(amount) {
    return formatMoneyDisplay(amount, 'ru', 'RUB')
  }

  function fromBase(amount) {
    return Number(amount) || 0
  }

  function toBase(amount) {
    return Number(amount) || 0
  }

  function shortDate(dateString) {
    return formatShortDate(dateString, 'ru')
  }

  return {
    uiStore,
    locale,
    currencyCode,
    t,
    money,
    displayMoney,
    fromBase,
    toBase,
    shortDate,
  }
}
