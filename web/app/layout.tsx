import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "RAG Video Assistant",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="w-full py-4 px-6 bg-black flex items-center gap-10 border-b border-cyan-400 
shadow-[0_0_12px_rgba(0,255,255,0.4)] relative">

  {/* Glow overlay */}
  <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_top_left,rgba(0,255,255,0.25),transparent_60%)]"></div>

  <Link 
    href="/" 
    className="text-cyan-300 font-semibold tracking-wider hover:text-cyan-100 
    transition-all duration-200 cursor-pointer
    hover:shadow-[0_0_10px_rgba(0,255,255,0.6)]"
  >
    HOME
  </Link>

  <Link 
    href="/upload" 
    className="text-cyan-300 font-semibold tracking-wider hover:text-cyan-100 
    transition-all duration-200 cursor-pointer
    hover:shadow-[0_0_10px_rgba(0,255,255,0.6)]"
  >
    UPLOAD
  </Link>

  <Link 
    href="/chat" 
    className="text-cyan-300 font-semibold tracking-wider hover:text-cyan-100 
    transition-all duration-200 cursor-pointer
    hover:shadow-[0_0_10px_rgba(0,255,255,0.6)]"
  >
    CHAT
  </Link>
</div>


        {children}
      </body>
    </html>
  );
}
