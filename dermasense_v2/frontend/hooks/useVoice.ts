'use client'
import { useCallback, useEffect, useRef, useState } from 'react'
import { ApiError } from '@/services/api'
import { transcribe } from '@/services/voiceService'

export function useVoice(onText: (text: string) => void) {
  const [recording, setRecording] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const recorder = useRef<MediaRecorder | null>(null)
  const chunks = useRef<Blob[]>([])
  const supported = typeof window !== 'undefined' && !!navigator.mediaDevices?.getUserMedia && typeof MediaRecorder !== 'undefined'

  const start = useCallback(async () => {
    setError(null)
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const rec = new MediaRecorder(stream)
      chunks.current = []
      rec.ondataavailable = (e) => e.data.size && chunks.current.push(e.data)
      rec.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop())
        setBusy(true)
        try {
          const text = await transcribe(new Blob(chunks.current, { type: rec.mimeType }))
          if (text) onText(text)
          else setError('No speech was detected. Please try again.')
        } catch (e) {
          setError(e instanceof ApiError ? e.message : 'Could not transcribe the recording')
        } finally {
          setBusy(false)
        }
      }
      rec.start()
      recorder.current = rec
      setRecording(true)
    } catch {
      setError('Microphone access was blocked. Allow it in your browser settings to use voice.')
    }
  }, [onText])

  const stop = useCallback(() => {
    recorder.current?.state === 'recording' && recorder.current.stop()
    setRecording(false)
  }, [])

  useEffect(() => () => { recorder.current?.state === 'recording' && recorder.current.stop() }, [])
  return { recording, busy, error, supported, start, stop }
}
