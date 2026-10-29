import './globals.css';

export const metadata = {
  title: 'Holographic Clinical Command Deck • Next.js & Tailwind Suite',
  description: 'Enterprise 60FPS Glassmorphic Healthcare Analytics Dashboard built with Next.js 14, Tailwind CSS, Framer Motion, and Recharts.',
  openGraph: {
    title: 'Holographic Clinical Command Deck • Next.js & Tailwind Suite',
    description: 'Enterprise 60FPS Glassmorphic Healthcare Analytics Dashboard with Framer Motion, Recharts, and authentic Egyptian healthcare economics.',
    images: ['cairo_tech_founders_hologram.jpg'],
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased selection:bg-holo-cyan selection:text-black">
        {children}
      </body>
    </html>
  );
}
