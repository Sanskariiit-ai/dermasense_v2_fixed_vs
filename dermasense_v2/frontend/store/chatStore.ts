import { create } from 'zustand'
import type { ChatMessage, UrgencyLevel } from '@/types/message'
import type { ConditionMatch, Symptom } from '@/types/symptom'

interface ChatState {
  sessionId: string | null
  messages: ChatMessage[]
  symptoms: Symptom[]
  conditions: ConditionMatch[]
  sending: boolean
  urgent: UrgencyLevel
  addMessage: (m: ChatMessage) => void
  setSession: (id: string) => void
  setInsights: (symptoms: Symptom[], conditions: ConditionMatch[], urgent: UrgencyLevel) => void
  setSending: (v: boolean) => void
  reset: () => void
}

const empty = { sessionId: null, messages: [], symptoms: [], conditions: [], sending: false, urgent: null as UrgencyLevel }

export const useChatStore = create<ChatState>((set) => ({
  ...empty,
  addMessage: (m) => set((s) => ({ messages: [...s.messages, m] })),
  setSession: (id) => set({ sessionId: id }),
  setInsights: (symptoms, conditions, urgent) => set({ symptoms, conditions, urgent }),
  setSending: (sending) => set({ sending }),
  reset: () => set({ ...empty }),
}))
