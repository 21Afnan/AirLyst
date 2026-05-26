export function AirLystLogo({ className = "w-8 h-8" }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        {/* Left Leg Gradient (Blue to Cyan) */}
        <linearGradient id="leftLegGrad" x1="0%" y1="100%" x2="50%" y2="0%">
          <stop offset="0%" stopColor="#1e3a8a" />
          <stop offset="100%" stopColor="#00d2ff" />
        </linearGradient>
        
        {/* Right Leg Gradient (Teal to Green) */}
        <linearGradient id="rightLegGrad" x1="50%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#00d2ff" />
          <stop offset="100%" stopColor="#10b981" />
        </linearGradient>

        {/* Wind Bridge Gradient */}
        <linearGradient id="windBridgeGrad" x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stopColor="#00d2ff" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0.8" />
        </linearGradient>

        {/* Premium Neon Glow */}
        <filter id="premiumGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="2.5" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      {/* Left loop/ribbon representing the ascending wind current */}
      <path
        d="M 16 52 C 16 38, 22 20, 32 16 C 36 14, 40 18, 40 24 C 40 32, 28 44, 20 48"
        stroke="url(#leftLegGrad)"
        strokeWidth="4.5"
        strokeLinecap="round"
        fill="none"
        filter="url(#premiumGlow)"
      />

      {/* Right loop/ribbon representing clean returning air flow */}
      <path
        d="M 48 52 C 48 38, 42 20, 32 16 C 28 14, 24 18, 24 24 C 24 32, 36 44, 44 48"
        stroke="url(#rightLegGrad)"
        strokeWidth="4.5"
        strokeLinecap="round"
        fill="none"
        filter="url(#premiumGlow)"
      />

      {/* The cross-bar of the 'A', styled as a dynamic horizontal wind wave */}
      <path
        d="M 22 36 C 28 32, 36 40, 42 36"
        stroke="url(#windBridgeGrad)"
        strokeWidth="3.5"
        strokeLinecap="round"
        fill="none"
        filter="url(#premiumGlow)"
      />

      {/* High-tech predictor spark star at the apex of the 'A' */}
      <path
        d="M 32 8 L 34 12 L 38 14 L 34 16 L 32 20 L 30 16 L 26 14 L 30 12 Z"
        fill="#00d2ff"
        filter="url(#premiumGlow)"
        className="animate-pulse"
      />
    </svg>
  );
}
