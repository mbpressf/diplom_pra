import axios from 'axios'

const configuredBaseURL = import.meta.env.VITE_API_URL
const baseURL = import.meta.env.PROD
  ? (configuredBaseURL && configuredBaseURL !== 'http://127.0.0.1:8000' ? configuredBaseURL : '/api')
  : (configuredBaseURL || 'http://127.0.0.1:8000')

const api = axios.create({
  baseURL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('finance_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      localStorage.removeItem('finance_token')
      localStorage.removeItem('finance_cache_v1')
      localStorage.removeItem('finance_selected_org_id')

      if (typeof window !== 'undefined' && !['/login', '/register'].includes(window.location.pathname)) {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  },
)

export default api
