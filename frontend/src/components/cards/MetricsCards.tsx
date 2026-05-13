type Props = {
  eventsToday: number
  uniqueUsers: number
  p95Latency: number
  errorRate: number
}

export function MetricsCards({ eventsToday, uniqueUsers, p95Latency, errorRate }: Props) {
  const cards = [
    { label: 'Events Today', value: eventsToday },
    { label: 'Unique Users', value: uniqueUsers },
    { label: 'P95 Latency (ms)', value: p95Latency },
    { label: 'Error Rate (%)', value: errorRate.toFixed(2) },
  ]

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
      {cards.map((card) => (
        <div key={card.label} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">{card.label}</p>
          <p className="text-2xl font-semibold text-slate-900">{card.value}</p>
        </div>
      ))}
    </div>
  )
}
