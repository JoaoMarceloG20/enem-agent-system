import './globals.css'

export const metadata = {
  title: 'ENEM Agent System',
  description: 'Sistema inteligente de preparação para o ENEM',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}