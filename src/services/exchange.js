const FRANKFURTER_URL = 'https://api.frankfurter.dev/v1/latest?base=USD&symbols=RUB'

export async function fetchUsdRubRate() {
  const response = await fetch(FRANKFURTER_URL, {
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error(`Exchange API responded with ${response.status}`)
  }

  const data = await response.json()
  const rate = Number(data?.rates?.RUB)

  if (!Number.isFinite(rate) || rate <= 0) {
    throw new Error('Exchange API returned invalid USD/RUB rate')
  }

  return {
    usdToRubRate: rate,
    date: data?.date || '',
    fetchedAt: new Date().toISOString(),
    source: 'frankfurter',
  }
}
