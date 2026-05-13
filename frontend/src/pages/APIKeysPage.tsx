import { useState } from 'react'

type ApiKey = { id: number; name: string; revoked: boolean }

export function APIKeysPage() {
  const [keys, setKeys] = useState<ApiKey[]>([{ id: 1, name: 'default-key', revoked: false }])
  const [name, setName] = useState('')

  const createKey = () => {
    if (!name) return
    setKeys((current) => [...current, { id: current.length + 1, name, revoked: false }])
    setName('')
  }

  const revokeKey = (id: number) => setKeys((current) => current.map((item) => (item.id === id ? { ...item, revoked: true } : item)))

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <h3 className="mb-3 text-lg font-semibold">API Keys</h3>
      <div className="mb-3 flex gap-2">
        <input className="rounded border border-slate-300 px-3 py-2" value={name} onChange={(event) => setName(event.target.value)} placeholder="Key name" />
        <button className="rounded bg-emerald-600 px-3 py-2 text-white" onClick={createKey}>
          Create
        </button>
      </div>
      <ul className="space-y-2">
        {keys.map((key) => (
          <li key={key.id} className="flex items-center justify-between rounded border border-slate-200 px-3 py-2">
            <span>
              {key.name} {key.revoked ? '(revoked)' : ''}
            </span>
            <button className="text-sm text-red-600" onClick={() => revokeKey(key.id)} disabled={key.revoked}>
              Revoke
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
