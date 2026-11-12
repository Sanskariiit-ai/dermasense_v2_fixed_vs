import { describe, expect, it } from 'vitest'
import { percent, titleCase } from '../../frontend/utils/formatter'
import { validateMessage, validatePassword, validatePhone, validateRegistration } from '../../frontend/utils/validators'

describe('validators', () => {
  it('validates phone numbers', () => {
    expect(validatePhone('9876543210')).toBeNull()
    expect(validatePhone('+919876543210')).toBeNull()
    expect(validatePhone('12ab')).not.toBeNull()
    expect(validatePhone('')).not.toBeNull()
  })
  it('requires 8 character passwords', () => {
    expect(validatePassword('1234567')).not.toBeNull()
    expect(validatePassword('12345678')).toBeNull()
  })
  it('validates registration and reports every problem', () => {
    const errors = validateRegistration({ name: ' ', age: '200', gender: undefined, phone_number: 'x', password: 'a' } as never)
    expect(Object.keys(errors).sort()).toEqual(['age', 'gender', 'name', 'password', 'phone_number'])
    expect(validateRegistration({ name: 'Asha', age: '30', gender: 'female', phone_number: '9876543210', password: 'longenough' } as never)).toEqual({})
  })
  it('limits message length', () => {
    expect(validateMessage('  ')).not.toBeNull()
    expect(validateMessage('x'.repeat(2001))).not.toBeNull()
    expect(validateMessage('itchy skin')).toBeNull()
  })
})

describe('formatter', () => {
  it('formats text and scores', () => {
    expect(titleCase('red patches')).toBe('Red Patches')
    expect(percent(0.456)).toBe('46%')
    expect(percent(5)).toBe('100%')
    expect(percent(-1)).toBe('0%')
  })
})
