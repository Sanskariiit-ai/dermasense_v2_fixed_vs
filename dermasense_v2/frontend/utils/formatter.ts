export const titleCase = (s: string): string => s.replace(/\b\w/g, (c) => c.toUpperCase())

export const formatTime = (ms: number): string =>
  new Date(ms).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })

export const percent = (score: number): string => `${Math.round(Math.max(0, Math.min(1, score)) * 100)}%`

export const uid = (): string =>
  typeof crypto !== 'undefined' && 'randomUUID' in crypto ? crypto.randomUUID() : String(Date.now() + Math.random())
