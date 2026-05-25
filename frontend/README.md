# AirLyst - Single Page Air Quality Dashboard

Clean, minimal air quality monitoring dashboard. Real-time current conditions, 72-hour trend visualization, and 3-day average AQI forecasting in one streamlined view.

## Dashboard Features

### Current Air Quality
- Real-time AQI monitoring with animated circular progress indicator
- Main pollutants: PM2.5, PM10, O3, NO2, SO2, CO
- Atmospheric conditions: Temperature, Humidity, Pressure, Wind Speed
- Live weather information display
- Manual refresh button with loading state

### 3-Day Average AQI Cards (Redesigned)
- Attractive modern stat cards with gradient backgrounds
- Large, bold AQI numbers (48-56px) for quick scanning
- Status badges (Good/Moderate/Unhealthy/Very Poor) with dynamic colors
- Visual progress indicators showing air quality intensity
- Hover lift animations for interactive feel
- Today, Tomorrow, and Day After forecasts
- Positioned at top for quick reference before detailed trends

### 24-Hour Trend Chart
- Interactive line chart showing hourly AQI data for next 24 hours
- Color-coded severity bands for visual context
- Hover tooltips with detailed hourly information
- Smooth animations and responsive design
- Built with Recharts for accessible visualization

## Design & UX

- **Logo**: Custom AirLyst molecule icon representing air monitoring (not Wind)
- **Color Palette**: Blue-cyan gradient with semantic color coding
  - Blue (#0288d1): Primary, information
  - Cyan (#00bcd4): Accent, secondary information
  - Red: High pollution alerts
  - Green: Good air quality
- **Animations**: Slide-in, fade-in, scale effects with 100-400ms stagger
- **Typography**: Geist font family with semantic hierarchy
- **Dark Mode**: Full support with adaptive color inversions
- **Responsive**: Mobile-first design (320px - 4K)

## Tech Stack

- **Framework**: Next.js 16 with App Router & Turbopack
- **React**: 19.2 with client/server components
- **Styling**: Tailwind CSS v4 with custom animations
- **Visualization**: Recharts for trend charts
- **Icons**: Lucide React
- **Animations**: Custom CSS keyframes + Tailwind utilities
- **State**: React hooks with client-side state management

## Project Structure

```
├── app/
│   ├── page.tsx              # Single-page dashboard
│   ├── layout.tsx            # Root layout with navigation
│   └── globals.css           # Theme colors & animations
├── components/
│   ├── navigation.tsx        # Top navbar
│   ├── airlyst-logo.tsx      # Custom AirLyst logo
│   ├── theme-provider.tsx    # Dark mode provider
│   └── dashboard/
│       ├── aqi-card.tsx      # Main AQI circular indicator
│       ├── weather-widget.tsx # Weather conditions display
│       └── aqi-trend-chart.tsx # 24-hour trend chart
├── lib/api/
│   ├── client.ts           # API client & data fetching
│   ├── mock-data.ts        # Realistic mock data generator
│   └── types.ts            # TypeScript interfaces
└── hooks/
    ├── use-toast.ts
    └── use-mobile.ts
```

## Getting Started

```bash
# Install dependencies
pnpm install

# Run development server (with hot reload)
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

Open [http://localhost:3000](http://localhost:3000) to view the dashboard.

## Single-Page Dashboard

The dashboard is a single comprehensive page featuring:
- Current air quality with real-time data
- 3-day forecast cards with attractive stat design
- 24-hour trend chart for detailed trend analysis
- One-click refresh button to update all data
- Fully responsive mobile-first design

## Build Status

✅ Production build successful with all pages prerendered  
✅ Zero TypeScript or ESLint errors  
✅ Optimized with Turbopack bundler  
✅ Mobile responsive, accessible, performant  

## Color Scheme

**Light Mode**
- Background: #f0f7ff → #e8f4f8 (blue-cyan gradient)
- Text: #0d47a1 (dark blue)
- Cards: White with cyan borders

**Dark Mode**
- Background: #0d1b2a → #0f2744 (dark blue gradient)
- Text: #b3e5fc (light cyan)
- Cards: Slate with blue borders

---

Made with care for better air quality awareness worldwide.
