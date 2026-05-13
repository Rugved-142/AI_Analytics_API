import { FunnelChart } from '../components/charts/FunnelChart'
import { TimeSeriesChart } from '../components/charts/TimeSeriesChart'
import { MetricsCards } from '../components/cards/MetricsCards'
import { TopPagesTable } from '../components/tables/TopPagesTable'
import { useAnalytics } from '../hooks/useAnalytics'
import { APIKeysPage } from './APIKeysPage'

export function DashboardPage() {
  const { summary, timeseries, funnels, loading, timeRange, setTimeRange } = useAnalytics()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">Analytics Dashboard</h1>
        <select
          className="rounded border border-slate-300 px-3 py-2"
          value={timeRange}
          onChange={(event) => setTimeRange(event.target.value as '1h' | '24h' | '7d' | '30d')}
        >
          <option value="1h">1h</option>
          <option value="24h">24h</option>
          <option value="7d">7d</option>
          <option value="30d">30d</option>
        </select>
      </div>

      {loading ? <div className="rounded bg-slate-100 p-4 text-sm">Loading analytics…</div> : null}

      <MetricsCards
        eventsToday={summary?.total_events ?? 0}
        uniqueUsers={summary?.unique_users ?? 0}
        p95Latency={187}
        errorRate={0.08}
      />

      <TimeSeriesChart data={timeseries} />
      <div className="grid gap-4 lg:grid-cols-2">
        <TopPagesTable rows={summary?.top_pages ?? []} />
        <FunnelChart data={funnels} />
      </div>

      <APIKeysPage />
    </div>
  )
}
