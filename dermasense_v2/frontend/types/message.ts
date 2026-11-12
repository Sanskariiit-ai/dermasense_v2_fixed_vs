import type { ConditionMatch, Symptom } from './symptom'

export type UrgencyLevel = 'crisis' | 'emergency' | 'urgent_review' | null

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'error'
  content: string
  createdAt: number
  urgent?: UrgencyLevel
  followups?: string[]
  sources?: string[]
}

export interface ChatApiResponse {
  session_id: string
  response: string
  urgent: UrgencyLevel
  symptoms: Symptom[]
  followups: string[]
  conditions: ConditionMatch[]
  sources: string[]
  disclaimer: string
}
