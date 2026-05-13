import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

type Point = { bucket: string; count: number }

type Props = { data: Point[] }

export function TimeSeriesChart({ data }: Props) {
  return (
    <div className="h-72 rounded-lg border border-slate-200 bg-white p-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="bucket" hide />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Line dataKey="count" stroke="#2563eb" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
