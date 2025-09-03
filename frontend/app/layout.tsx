import './globals.css'
import type { Metadata } from 'next'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

export const metadata: Metadata = {
  title: 'Your Project',
  description: 'A full-stack application built with Next.js and FastAPI',
}

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      retry: 1,
    },
  },
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <QueryClientProvider client={queryClient}>
          {children}
          <ReactQueryDevtools initialIsOpen={false} />
        </QueryClientProvider>
      </body>
    </html>
  )
}
