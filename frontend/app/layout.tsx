import './globals.css'

export const metadata = {
  title: 'Aledo Train Monitor',
  description: 'Real-time train monitoring and predictions for Aledo, TX',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  )
} 