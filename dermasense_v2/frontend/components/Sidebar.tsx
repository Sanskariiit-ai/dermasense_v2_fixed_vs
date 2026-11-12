'use client'
import { useState } from 'react'
import { useChat } from '@/hooks/useChat'
import { usePatientStore } from '@/store/patientStore'
import { percent, titleCase } from '@/utils/formatter'

export default function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { symptoms, conditions, sessionId, reset, saveReport } = useChat()
  const { patient, logout } = usePatientStore()
  const [note, setNote] = useState<string | null>(null)
  return (
    <aside className={`sidebar ${open ? 'open' : ''}`} aria-label="Conversation summary">
      <div className="brand"><img src="/logo.png" alt="" width={36} height={36} /><strong>DermaSense</strong>
        <button className="link close-only" onClick={onClose}>Close</button></div>
      <p className="hello">Signed in as <strong>{patient?.name}</strong></p>
      <button className="btn secondary" onClick={() => { reset(); onClose() }}>New conversation</button>

      <section aria-labelledby="sym-h"><h2 id="sym-h">Symptoms noticed</h2>
        {symptoms.length ? <ul className="tags">{symptoms.map((s) => <li key={s.symptom}>{titleCase(s.symptom)}</li>)}</ul>
          : <p className="muted">None yet. Describe what you see or feel.</p>}</section>

      <section aria-labelledby="cond-h"><h2 id="cond-h">Worth discussing with a doctor</h2>
        {conditions.length ? <ul className="conds">{conditions.map((c) => (
          <li key={c.condition}><strong>{titleCase(c.condition)}</strong>
            <span className="muted">Match {percent(c.score)} ({c.confidence_note})</span></li>))}</ul>
          : <p className="muted">Suggestions appear as you share symptoms.</p>}
        <p className="muted small">These are possibilities, not a diagnosis.</p></section>

      <button className="btn" disabled={!sessionId} onClick={async () => setNote(await saveReport() ?? 'Report downloaded')}>Download report (PDF)</button>
      {note && <p className="muted small" role="status">{note}</p>}
      <button className="link" onClick={logout}>Sign out</button>
    </aside>
  )
}
