import { useState } from 'react'
import type { FormEvent } from 'react'

type Props = {
  onLogin: (email: string, password: string) => Promise<void>
  onRegister: (email: string, password: string) => Promise<void>
}

export function LoginPage({ onLogin, onRegister }: Props) {
  const [email, setEmail] = useState('demo@example.com')
  const [password, setPassword] = useState('password123')

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    await onLogin(email, password)
  }

  return (
    <div className="mx-auto mt-20 w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <h1 className="mb-6 text-2xl font-semibold">AI Analytics Login</h1>
      <form className="space-y-4" onSubmit={submit}>
        <input
          className="w-full rounded border border-slate-300 px-3 py-2"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="Email"
        />
        <input
          className="w-full rounded border border-slate-300 px-3 py-2"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Password"
          type="password"
        />
        <div className="flex gap-2">
          <button className="rounded bg-blue-600 px-4 py-2 text-white" type="submit">
            Login
          </button>
          <button className="rounded border border-blue-600 px-4 py-2 text-blue-600" type="button" onClick={() => onRegister(email, password)}>
            Register
          </button>
        </div>
      </form>
    </div>
  )
}
