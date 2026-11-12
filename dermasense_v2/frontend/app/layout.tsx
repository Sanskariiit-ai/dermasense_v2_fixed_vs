import type { Metadata, Viewport } from 'next'
import '@/styles/globals.css'

export const metadata: Metadata = { title: 'DermaSense', description: 'Describe skin concerns and prepare for a doctor visit' }
export const viewport: Viewport = { width: 'device-width', initialScale: 1 }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
