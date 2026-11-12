import type { ChatApiResponse } from '@/types/message'
import type { RegisterInput, TokenResponse } from '@/types/patient'
import { request } from './api'

export const register = (input: RegisterInput) =>
  request<TokenResponse>('/auth/register', { method: 'POST', body: JSON.stringify(input) })

export const login = (phone_number: string, password: string) =>
  request<TokenResponse>('/auth/login', { method: 'POST', body: JSON.stringify({ phone_number, password }) })

export const sendMessage = (message: string, sessionId: string | null) =>
  request<ChatApiResponse>('/chat', {
    method: 'POST',
    body: JSON.stringify({ message, ...(sessionId ? { session_id: sessionId } : {}) }),
  })

export const downloadReport = (sessionId: string) =>
  request<Blob>('/reports', { method: 'POST', body: JSON.stringify({ session_id: sessionId }) })
