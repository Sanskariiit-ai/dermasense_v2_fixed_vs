export type Gender = 'female' | 'male' | 'other' | 'prefer_not_to_say'

export interface Patient {
  id: string
  name: string
  age: number
  gender: Gender
  phone_number: string
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  patient: Patient
}

export interface RegisterInput {
  name: string
  age: number
  gender: Gender
  phone_number: string
  password: string
}
