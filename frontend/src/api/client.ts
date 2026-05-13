import axios from 'axios'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export type SummaryResponse = {
  total_events: number
  unique_users: number
  top_pages: { page: string; count: number }[]
}

export type TimeseriesPoint = { bucket: string; count: number }

export type FunnelStep = { step: string; users: number; conversion_rate: number }

export async function fetchSummary() {
  const { data } = await apiClient.get<SummaryResponse>('/api/v1/analytics/summary')
  return data
}

export async function fetchTimeseries() {
  const { data } = await apiClient.get<{ data: TimeseriesPoint[] }>('/api/v1/analytics/timeseries')
  return data
}

export async function fetchFunnels() {
  const { data } = await apiClient.get<{ funnel: FunnelStep[] }>('/api/v1/analytics/funnels')
  return data
}

export async function registerUser(email: string, password: string) {
  const { data } = await apiClient.post('/auth/register', { email, password })
  return data
}

export async function loginUser(email: string, password: string) {
  const { data } = await apiClient.post<{ access_token: string; refresh_token: string }>('/auth/login', { email, password })
  return data
}

export async function refreshToken(refreshTokenValue: string) {
  const { data } = await apiClient.post<{ access_token: string; refresh_token: string }>('/auth/refresh', {
    refresh_token: refreshTokenValue,
  })
  return data
}
