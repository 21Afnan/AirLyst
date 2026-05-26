export function AirLystLogo({ className = "w-8 h-8" }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="logoGradMain" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#3b82f6" />
          <stop offset="50%" stopColor="#06b6d4" />
          <stop offset="100%" stopColor="#10b981" />
        </linearGradient>
        <filter id="logoGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      {/* Outer Glowing Ring representing AQI forecast range */}
      <circle 
        cx="32" 
        cy="32" 
        r="25" 
        stroke="url(#logoGradMain)" 
        strokeWidth="3.5" 
        strokeDasharray="110 30" 
        strokeLinecap="round" 
        filter="url(#logoGlow)" 
        className="animate-spin-slow"
        transform="rotate(-45 32 32)"
      />
      
      {/* Sleek wind trace 1 */}
      <path 
        d="M 18 25 C 28 20, 36 34, 46 27" 
        stroke="white" 
        strokeWidth="3" 
        strokeLinecap="round" 
        fill="none"
        filter="url(#logoGlow)"
      />
      {/* Sleek wind trace 2 */}
      <path 
        d="M 15 33 C 24 30, 34 38, 48 33" 
        stroke="url(#logoGradMain)" 
        strokeWidth="3" 
        strokeLinecap="round" 
        fill="none"
      />
      {/* Sleek wind trace 3 */}
      <path 
        d="M 18 41 C 28 41, 38 34, 46 39" 
        stroke="white" 
        strokeWidth="2" 
        strokeLinecap="round" 
        fill="none"
        opacity="0.8"
      />
      
      {/* Spark/Star of Prediction */}
      <path 
        d="M 44 19 L 46 22 L 49 24 L 46 26 L 44 29 L 42 26 L 39 24 L 42 22 Z" 
        fill="url(#logoGradMain)"
        filter="url(#logoGlow)"
        className="animate-pulse"
      />
    </svg>
  );
}
