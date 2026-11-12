import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'
import { useChatStore } from '@/store/chatStore'
import type { Patient } from '@/types/patient'

interface PatientState {
  token: string | null
  patient: Patient | null
  setAuth: (token: string, patient: Patient) => void
  logout: () => void
}

// sessionStorage: the sign-in ends when the tab closes, which suits health data on shared devices.
export const usePatientStore = create<PatientState>()(
  persist(
    (set) => ({
      token: null,
      patient: null,
      setAuth: (token, patient) => set({ token, patient }),
      // Clear the conversation too, so the next person on a shared device never sees it.
      logout: () => { set({ token: null, patient: null }); useChatStore.getState().reset() },
    }),
    { name: 'dermasense-auth', storage: createJSONStorage(() => sessionStorage) },
  ),
)
