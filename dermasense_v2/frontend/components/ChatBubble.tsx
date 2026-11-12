import type { ChatMessage } from '@/types/message'
import { formatTime } from '@/utils/formatter'

const urgentLabel = { crisis: 'Support is available', emergency: 'Seek emergency care', urgent_review: 'See a doctor soon' } as const

export default function ChatBubble({ message, onFollowup }: { message: ChatMessage; onFollowup: (q: string) => void }) {
  const urgent = message.urgent ? urgentLabel[message.urgent] : null
  return (
    <article className={`bubble ${message.role}`} aria-label={`${message.role === 'user' ? 'You' : 'DermaSense'} at ${formatTime(message.createdAt)}`}>
      {urgent && <p className={`urgent ${message.urgent}`} role="alert">{urgent}</p>}
      <p className="text">{message.content}</p>
      {!!message.followups?.length && (
        <div className="chips" aria-label="Questions that may help">
          {message.followups.map((q) => (
            <button key={q} type="button" className="chip" onClick={() => onFollowup(q)}>{q}</button>
          ))}
        </div>
      )}
      {!!message.sources?.length && <p className="meta">Based on: {message.sources.map((s) => s.replace('.txt', '').replace(/_/g, ' ')).join(', ')}</p>}
      <time className="meta" dateTime={new Date(message.createdAt).toISOString()}>{formatTime(message.createdAt)}</time>
    </article>
  )
}
