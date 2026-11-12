import { request } from './api'

export async function transcribe(blob: Blob): Promise<string> {
  const ext = blob.type.includes('ogg') ? 'ogg' : blob.type.includes('mp4') ? 'm4a' : 'webm'
  const form = new FormData()
  form.append('file', blob, `recording.${ext}`)
  const out = await request<{ transcript: string }>('/voice/transcribe', { method: 'POST', body: form })
  return out.transcript
}
