'use client'
import { useVoice } from '@/hooks/useVoice'

export default function VoiceRecorder({ onText, disabled }: { onText: (t: string) => void; disabled?: boolean }) {
  const { recording, busy, error, supported, start, stop } = useVoice(onText)
  if (!supported) return null
  return (
    <>
      <button type="button" className={`icon-btn ${recording ? 'rec' : ''}`} disabled={disabled || busy}
        aria-pressed={recording} onClick={recording ? stop : start}
        aria-label={recording ? 'Stop recording' : busy ? 'Transcribing' : 'Record a voice message'}>
        {recording ? 'Stop' : busy ? '…' : 'Voice'}
      </button>
      {error && <p className="field-error" role="alert">{error}</p>}
    </>
  )
}
