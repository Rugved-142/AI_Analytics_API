import { DashboardPage } from './pages/DashboardPage'
import { LoginPage } from './pages/LoginPage'
import { useAuth } from './hooks/useAuth'

export default function App() {
  const auth = useAuth()

  return (
    <div className="min-h-screen bg-slate-50 p-6 text-slate-900">
      {auth.isAuthenticated ? (
        <div className="mx-auto max-w-6xl">
          <div className="mb-4 flex justify-end">
            <button className="rounded border border-slate-400 px-3 py-2 text-sm" onClick={auth.logout}>
              Logout
            </button>
          </div>
          <DashboardPage />
        </div>
      ) : (
        <LoginPage onLogin={auth.login} onRegister={auth.register} />
      )}
    </div>
  )
}
