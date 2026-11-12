'use client'
import { useCallback, useEffect, useRef, useState } from 'react'
import AuthPanel from '@/components/AuthPanel'
import ChatBubble from '@/components/ChatBubble'
import Sidebar from '@/components/Sidebar'
import TypingIndicator from '@/components/TypingIndicator'
import VoiceRecorder from '@/components/VoiceRecorder'
import { useChat } from '@/hooks/useChat'
import { usePatientStore } from '@/store/patientStore'

export default function Home() {
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  const token = usePatientStore((s) => s.token)
  if (!mounted) return null
  return token ? <ChatScreen /> : <AuthPanel />
}

function ChatScreen() {
  const { messages, sending, send, urgent } = useChat()
  const [text, setText] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [menu, setMenu] = useState(false)
  const end = useRef<HTMLDivElement>(null)
  useEffect(() => end.current?.scrollIntoView({ behavior: 'smooth' }), [messages, sending])

  const submit = useCallback(async () => {
    if (sending) return
    const msg = text
    const problem = await send(msg)
    if (problem) return setError(problem)
    setError(null); setText('')
  }, [text, sending, send])
  const addText = useCallback((t: string) => setText((p) => (p ? `${p} ${t}` : t)), [])

  return (
    <div className="shell">
      <Sidebar open={menu} onClose={() => setMenu(false)} />
      <main className="chat">
        <header className="topbar"><button className="link" onClick={() => setMenu(true)}>Menu</button><strong>DermaSense</strong></header>
        {urgent && <p className={`banner ${urgent}`} role="alert">If you feel unwell or unsafe, call your local emergency number now (112 in India).</p>}
        <div className="messages" role="log" aria-live="polite" aria-label="Conversation">
          {!messages.length && (
            <div className="empty"><h2>How is your skin today?</h2>
              <p className="muted">Tell me what you are noticing: where, how long, and whether it itches or hurts. I will ask a few follow-up questions.</p></div>)}
          {messages.map((m) => <ChatBubble key={m.id} message={m} onFollowup={(q) => setText(`${q} `)} />)}
          {sending && <TypingIndicator />}
          <div ref={end} />
        </div>
        <form className="composer" onSubmit={(e) => { e.preventDefault(); void submit() }}>
          <label htmlFor="msg" className="sr-only">Message</label>
          <textarea id="msg" rows={2} value={text} maxLength={2000} placeholder="Describe your symptoms…" aria-invalid={!!error}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void submit() } }} />
          <VoiceRecorder onText={addText} disabled={sending} />
          <button className="btn" disabled={sending}>Send</button>
          {error && <p className="field-error" role="alert">{error}</p>}
        </form>
        <p className="disclaimer">General information only, not a diagnosis. See a doctor for medical advice.</p>
      </main>
    </div>
  )
}
