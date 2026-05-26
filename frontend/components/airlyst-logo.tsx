export function AirLystLogo({ className = "w-8 h-8" }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        {/* Main Blue to Green Gradient */}
        <linearGradient id="logoGrad" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#0072db" />
          <stop offset="50%" stopColor="#00b4d8" />
          <stop offset="100%" stopColor="#00c9a7" />
        </linearGradient>
        {/* Soft Shadow for Glowing effect */}
        <filter id="softGlow" x="-10%" y="-10%" width="120%" height="120%">
          <feGaussianBlur stdDeviation="1.5" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      {/* Main Outer Open Circle Ring (Blue to Green Gradient) */}
      <path
        d="M 46 18 A 20 20 0 1 1 48 32"
        stroke="url(#logoGrad)"
        strokeWidth="4"
        strokeLinecap="round"
        filter="url(#softGlow)"
      />

      {/* Inner Wave Shape */}
      <path
        d="M 22 36 C 28 32, 34 40, 42 36"
        stroke="url(#logoGrad)"
        strokeWidth="3.5"
        strokeLinecap="round"
        fill="none"
        filter="url(#softGlow)"
      />

      {/* Spark/Plus at Top Right */}
      <path
        d="M 45 13 L 49 13 M 47 11 L 47 15"
        stroke="#00c9a7"
        strokeWidth="2.5"
        strokeLinecap="round"
        filter="url(#softGlow)"
        className="animate-pulse"
      />
    </svg>
  );
}
