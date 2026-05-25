export function AirLystLogo({ className = "w-8 h-8" }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#0288d1" />
          <stop offset="100%" stopColor="#00bcd4" />
        </linearGradient>
      </defs>

      {/* Background rounded square - blue gradient */}
      <rect x="4" y="4" width="56" height="56" rx="12" ry="12" fill="url(#logoGradient)" />
      
      {/* Air flow lines - curved design */}
      {/* Top curved line */}
      <path 
        d="M 16 22 Q 32 18 48 22" 
        stroke="white" 
        strokeWidth="2.5" 
        strokeLinecap="round" 
        fill="none"
      />
      
      {/* Middle curved line */}
      <path 
        d="M 14 32 Q 32 27 50 32" 
        stroke="white" 
        strokeWidth="2.5" 
        strokeLinecap="round" 
        fill="none"
      />
      
      {/* Bottom curved line */}
      <path 
        d="M 16 42 Q 32 46 48 42" 
        stroke="white" 
        strokeWidth="2.5" 
        strokeLinecap="round" 
        fill="none"
      />
      
      {/* Right arrow - indicating air direction */}
      <path 
        d="M 52 32 L 56 32 M 54 30 L 56 32 L 54 34" 
        stroke="white" 
        strokeWidth="2" 
        strokeLinecap="round" 
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}
