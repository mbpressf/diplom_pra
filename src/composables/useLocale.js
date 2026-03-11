import { computed } from 'vue'

import {
  convertFromRub,
  convertToRub,
  formatMoneyDisplay,
  formatMoneyFromRub,
  formatRateValue,
  formatShortDate,
  tFor,
} from '../utils/locale'
import { useUiStore } from '../store/ui'

export function useLocale() {
  const uiStore = useUiStore()

  const locale = computed(() => uiStore.locale)
  const currencyCode = computed(() => (uiStore.locale === 'en' ? 'USD' : 'RUB'))

  function t(key, params) {
    return tFor(uiStore.locale, key, params)
  }

  function money(amount) {
    return formatMoneyFromRub(amount, uiStore.locale, uiStore.usdToRubRate)
  }

  function displayMoney(amount) {
    return formatMoneyDisplay(amount, uiStore.locale)
  }

  function fromBase(amount) {
    return convertFromRub(amount, uiStore.locale, uiStore.usdToRubRate)
  }

  function toBase(amount) {
    return convertToRub(amount, uiStore.locale, uiStore.usdToRubRate)
  }

  function rateValue(rate) {
    return formatRateValue(rate, uiStore.locale)
  }

  function shortDate(dateString) {
    return formatShortDate(dateString, uiStore.locale)
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
    rateValue,
    shortDate,
  }
}
