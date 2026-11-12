import type { RegisterInput } from '@/types/patient'

export const PHONE_RE = /^\+?[0-9]{10,15}$/

export const validatePhone = (v: string): string | null =>
  PHONE_RE.test(v.trim()) ? null : 'Enter 10 to 15 digits, optionally starting with +'

export const validatePassword = (v: string): string | null =>
  v.length >= 8 ? null : 'Use at least 8 characters'

export function validateRegistration(input: Partial<Record<keyof RegisterInput, string>>): Record<string, string> {
  const errors: Record<string, string> = {}
  if (!input.name?.trim()) errors.name = 'Enter your name'
  const age = Number(input.age)
  if (!Number.isInteger(age) || age < 0 || age > 120) errors.age = 'Enter an age between 0 and 120'
  if (!input.gender) errors.gender = 'Choose an option'
  const phone = validatePhone(input.phone_number ?? '')
  if (phone) errors.phone_number = phone
  const pw = validatePassword(input.password ?? '')
  if (pw) errors.password = pw
  return errors
}

export const validateMessage = (v: string): string | null => {
  const t = v.trim()
  if (!t) return 'Type a message first'
  return t.length > 2000 ? 'Messages can be up to 2000 characters' : null
}
