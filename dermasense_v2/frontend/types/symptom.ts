export interface Symptom {
  symptom: string
  category: string
  confidence: number
}

export interface ConditionMatch {
  condition: string
  score: number
  matched_symptoms: string[]
  confidence_note: string
}
