import { useEffect, useMemo, useState } from 'react'

import { loginUser, refreshToken, registerUser } from '../api/client'

export function useAuth() {
  const [accessToken, setAccessToken] = useState<string | null>(() => localStorage.getItem('access_token'))
  const [refreshTokenValue, setRefreshTokenValue] = useState<string | null>(() => localStorage.getItem('refresh_token'))

  useEffect(() => {
    if (accessToken) localStorage.setItem('access_token', accessToken)
    else localStorage.removeItem('access_token')
  }, [accessToken])

  useEffect(() => {
    if (refreshTokenValue) localStorage.setItem('refresh_token', refreshTokenValue)
    else localStorage.removeItem('refresh_token')
  }, [refreshTokenValue])

  useEffect(() => {
    if (!refreshTokenValue) return
    const interval = setInterval(async () => {
      const data = await refreshToken(refreshTokenValue)
      setAccessToken(data.access_token)
      setRefreshTokenValue(data.refresh_token)
    }, 12 * 60 * 1000)
    return () => clearInterval(interval)
  }, [refreshTokenValue])

  const auth = useMemo(
    () => ({
      isAuthenticated: Boolean(accessToken),
      async login(email: string, password: string) {
        const tokens = await loginUser(email, password)
        setAccessToken(tokens.access_token)
        setRefreshTokenValue(tokens.refresh_token)
      },
      async register(email: string, password: string) {
        await registerUser(email, password)
      },
      logout() {
        setAccessToken(null)
        setRefreshTokenValue(null)
      },
    }),
    [accessToken],
  )

  return auth
}
