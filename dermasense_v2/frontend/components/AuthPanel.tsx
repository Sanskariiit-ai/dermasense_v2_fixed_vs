'use client'
import { FormEvent, useState } from 'react'
import { ApiError } from '@/services/api'
import { login, register } from '@/services/chatService'
import { usePatientStore } from '@/store/patientStore'
import type { Gender } from '@/types/patient'
import { validatePhone, validateRegistration } from '@/utils/validators'

export default function AuthPanel() {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [formError, setFormError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const setAuth = usePatientStore((s) => s.setAuth)

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const f = Object.fromEntries(new FormData(e.currentTarget)) as Record<string, string>
    const errs: Record<string, string> = mode === 'register' ? validateRegistration(f) : {}
    if (mode === 'login') {
      const phoneProblem = validatePhone(f.phone_number ?? '')
      if (phoneProblem) errs.phone_number = phoneProblem
      if (!f.password) errs.password = 'Enter your password'
    }
    setErrors(errs); setFormError(null)
    if (Object.keys(errs).length) return
    setBusy(true)
    try {
      const res = mode === 'login'
        ? await login(f.phone_number.trim(), f.password)
        : await register({ name: f.name.trim(), age: Number(f.age), gender: f.gender as Gender, phone_number: f.phone_number.trim(), password: f.password })
      setAuth(res.access_token, res.patient)
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : 'Something went wrong')
    } finally { setBusy(false) }
  }

  const field = (name: string, label: string, type = 'text', extra: object = {}) => (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <input id={name} name={name} type={type} aria-invalid={!!errors[name]} aria-describedby={errors[name] ? `${name}-e` : undefined} {...extra} />
      {errors[name] && <p id={`${name}-e`} className="field-error">{errors[name]}</p>}
    </div>
  )

  return (
    <main className="auth">
      <img src="/logo.png" alt="" width={56} height={56} />
      <h1>DermaSense</h1>
      <p className="muted">A private space to describe skin concerns and prepare for a doctor visit.</p>
      <form onSubmit={submit} noValidate aria-label={mode === 'login' ? 'Sign in' : 'Create account'}>
        {mode === 'register' && <>
          {field('name', 'Full name', 'text', { autoComplete: 'name' })}
          {field('age', 'Age', 'number', { min: 0, max: 120, inputMode: 'numeric' })}
          <div className="field"><label htmlFor="gender">Gender</label>
            <select id="gender" name="gender" defaultValue="" aria-invalid={!!errors.gender}>
              <option value="" disabled>Choose…</option><option value="female">Female</option><option value="male">Male</option>
              <option value="other">Other</option><option value="prefer_not_to_say">Prefer not to say</option></select>
            {errors.gender && <p className="field-error">{errors.gender}</p>}</div>
        </>}
        {field('phone_number', 'Phone number', 'tel', { autoComplete: 'tel', inputMode: 'tel' })}
        {field('password', 'Password', 'password', { autoComplete: mode === 'login' ? 'current-password' : 'new-password' })}
        {formError && <p className="field-error" role="alert">{formError}</p>}
        <button className="btn" disabled={busy}>{busy ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create account'}</button>
      </form>
      <button className="link" onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setErrors({}); setFormError(null) }}>
        {mode === 'login' ? 'New here? Create an account' : 'Already have an account? Sign in'}</button>
      <p className="muted small">DermaSense gives general information only and cannot diagnose. In an emergency call your local emergency number (112 in India).</p>
    </main>
  )
}
