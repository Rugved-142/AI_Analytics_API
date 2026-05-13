import { useMemo, useState } from 'react'

type Row = { page: string; count: number }

type Props = { rows: Row[] }

export function TopPagesTable({ rows }: Props) {
  const [page, setPage] = useState(1)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')
  const pageSize = 5

  const sorted = useMemo(
    () => [...rows].sort((a, b) => (sortDirection === 'asc' ? a.count - b.count : b.count - a.count)),
    [rows, sortDirection],
  )
  const paged = sorted.slice((page - 1) * pageSize, page * pageSize)
  const totalPages = Math.max(1, Math.ceil(sorted.length / pageSize))

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-lg font-semibold">Top Pages</h3>
        <button className="text-sm text-blue-600" onClick={() => setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')}>
          Sort: {sortDirection}
        </button>
      </div>
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-slate-500">
            <th className="py-2">Page</th>
            <th className="py-2">Events</th>
          </tr>
        </thead>
        <tbody>
          {paged.map((row) => (
            <tr key={row.page} className="border-b border-slate-100">
              <td className="py-2">{row.page}</td>
              <td className="py-2">{row.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-3 flex items-center justify-end gap-2">
        <button className="rounded border px-2 py-1" disabled={page <= 1} onClick={() => setPage((value) => value - 1)}>
          Prev
        </button>
        <span className="text-xs text-slate-500">
          {page}/{totalPages}
        </span>
        <button className="rounded border px-2 py-1" disabled={page >= totalPages} onClick={() => setPage((value) => value + 1)}>
          Next
        </button>
      </div>
    </div>
  )
}
