import { useCallback, useEffect, useState } from 'react'

import { fetchFunnels, fetchSummary, fetchTimeseries } from '../api/client'
import type { FunnelStep, SummaryResponse, TimeseriesPoint } from '../api/client'

type TimeRange = '1h' | '24h' | '7d' | '30d'

export function useAnalytics() {
  const [summary, setSummary] = useState<SummaryResponse | null>(null)
  const [timeseries, setTimeseries] = useState<TimeseriesPoint[]>([])
  const [funnels, setFunnels] = useState<FunnelStep[]>([])
  const [loading, setLoading] = useState(false)
  const [timeRange, setTimeRange] = useState<TimeRange>('24h')

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [summaryData, timeseriesData, funnelData] = await Promise.all([fetchSummary(), fetchTimeseries(), fetchFunnels()])
      setSummary(summaryData)
      setTimeseries(timeseriesData.data)
      setFunnels(funnelData.funnel)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
    const interval = setInterval(load, 30_000)
    return () => clearInterval(interval)
  }, [load, timeRange])

  return { summary, timeseries, funnels, loading, timeRange, setTimeRange, reload: load }
}
