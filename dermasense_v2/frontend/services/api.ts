import { usePatientStore } from '@/store/patientStore'

export const API_BASE = 'http://127.0.0.1:8000'
export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

function detailToText(detail: unknown): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => (d && typeof d.msg === 'string' ? d.msg : '')).filter(Boolean).join('. ')
  return 'Something went wrong'
}

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = usePatientStore.getState().token
  const headers = new Headers(init.headers)
  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (init.body && !(init.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  let res: Response
  try {
    res = await fetch(`${API_BASE}${path}`, { ...init, headers })
  } catch {
    throw new ApiError(0, 'Cannot reach the server. Check your connection and try again.')
  }
  if (res.status === 401 && token) usePatientStore.getState().logout()
  if (!res.ok) {
    let detail: unknown = res.statusText
    try { detail = (await res.json()).detail } catch { /* non-JSON error body */ }
    throw new ApiError(res.status, detailToText(detail))
  }
  const type = res.headers.get('content-type') ?? ''
  return (type.includes('application/json') ? res.json() : res.blob()) as Promise<T>
}
