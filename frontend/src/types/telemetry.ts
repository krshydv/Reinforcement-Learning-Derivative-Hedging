export type ApiLatencyPayload = {
  method: string
  path: string
  duration_ms: number
  status_code?: number
}

export type TelemetryEvent<TPayload = Record<string, unknown>> = {
  id: string
  channel: string
  event_type: string
  timestamp: string
  payload: TPayload
  source: string
  run_id?: string | null
  user_id?: string | null
}
