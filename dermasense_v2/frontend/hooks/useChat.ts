'use client'
import { useCallback } from 'react'
import { ApiError } from '@/services/api'
import { downloadReport, sendMessage } from '@/services/chatService'
import { useChatStore } from '@/store/chatStore'
import { uid } from '@/utils/formatter'
import { validateMessage } from '@/utils/validators'

export function useChat() {
  const store = useChatStore()

  const send = useCallback(async (text: string): Promise<string | null> => {
    const problem = validateMessage(text)
    if (problem) return problem
    const { addMessage, setSending, setSession, setInsights, sessionId } = useChatStore.getState()
    addMessage({ id: uid(), role: 'user', content: text.trim(), createdAt: Date.now() })
    setSending(true)
    try {
      const res = await sendMessage(text.trim(), sessionId)
      setSession(res.session_id)
      setInsights(res.symptoms, res.conditions, res.urgent)
      addMessage({ id: uid(), role: 'assistant', content: res.response, createdAt: Date.now(),
        urgent: res.urgent, followups: res.followups, sources: res.sources })
    } catch (e) {
      addMessage({ id: uid(), role: 'error', createdAt: Date.now(),
        content: e instanceof ApiError ? e.message : 'Something went wrong. Please try again.' })
    } finally {
      setSending(false)
    }
    return null
  }, [])

  const saveReport = useCallback(async (): Promise<string | null> => {
    const id = useChatStore.getState().sessionId
    if (!id) return 'Start a conversation first'
    try {
      const blob = await downloadReport(id)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'dermasense-report.pdf'
      a.click()
      URL.revokeObjectURL(url)
      return null
    } catch (e) {
      return e instanceof ApiError ? e.message : 'Could not create the report'
    }
  }, [])

  return { ...store, send, saveReport }
}
