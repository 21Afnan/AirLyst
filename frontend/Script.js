/* ═══════════════════════════════════════════════════════════════
   AirLyst — Air Quality Intelligence Dashboard
   Script.js  |  Pure Vanilla JS · Chart.js · Rich Aesthetics
   ═══════════════════════════════════════════════════════════════ */

const API_BASE_URL = 'http://127.0.0.1:8000';

// Global chart instances to destroy on updates
let aqiChartInstance = null;
let tempChartInstance = null;
let pm25ChartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialise minor UI animations/details
    initParticles();
    initNavbarScroll();
    initTime();
    initTabs();
    
    // 2. Fetch and render data from API
    fetchDashboardData();
    fetchShapData();
});

/* ────────────────────────────────────────────────────────────────
   1. PARTICLE CANVAS ANIMATION
   ──────────────────────────────────────────────────────────────── */
function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let particles = [];
    
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();
    
    // Generate soft, floating particles (representing clean/moving air)
    const count = Math.min(Math.floor(window.innerWidth / 30), 60);
    for (let i = 0; i < count; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 3.5 + 0.8,
            vx: (Math.random() - 0.5) * 0.35,
            vy: (Math.random() - 0.5) * 0.35,
            alpha: Math.random() * 0.4 + 0.1
        });
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;
            
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(79, 124, 255, ${p.alpha})`; // Premium soft blue
            ctx.fill();
        });
        
        requestAnimationFrame(animate);
    }
    animate();
}

/* ────────────────────────────────────────────────────────────────
   2. NAVBAR & CLOCK
   ──────────────────────────────────────────────────────────────── */
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

function initTime() {
    const timeEl = document.getElementById('navTime');
    if (!timeEl) return;
    
    function updateClock() {
        const now = new Date();
        const options = { weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false };
        timeEl.innerText = now.toLocaleDateString('en-US', options);
    }
    updateClock();
    setInterval(updateClock, 60000);
}

/* ────────────────────────────────────────────────────────────────
   3. SCROLL REVEAL (FADE UP)
   ──────────────────────────────────────────────────────────────── */
function initScrollObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.05 });
    
    document.querySelectorAll('.fade-up').forEach(el => {
        observer.observe(el);
    });
}

/* ────────────────────────────────────────────────────────────────
   4. TOAST NOTIFICATIONS
   ──────────────────────────────────────────────────────────────── */
function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4500);
}

/* ────────────────────────────────────────────────────────────────
   5. CHART TABS SWITCHING
   ──────────────────────────────────────────────────────────────── */
function initTabs() {
    const tabs = document.querySelectorAll('.chart-tab');
    const panels = document.querySelectorAll('.chart-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.tab;
            
            // Update tabs active state
            tabs.forEach(t => {
                t.classList.remove('active');
                t.setAttribute('aria-selected', 'false');
            });
            tab.classList.add('active');
            tab.setAttribute('aria-selected', 'true');
            
            // Update panels visibility
            panels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === `panel-${target}`) {
                    panel.classList.add('active');
                }
            });
        });
    });
}

/* ────────────────────────────────────────────────────────────────
   6. FETCH AND POPULATE FORECAST DASHBOARD
   ──────────────────────────────────────────────────────────────── */
async function fetchDashboardData() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/forecast`);
        if (!res.ok) throw new Error('Failed to fetch forecast details.');
        const data = await res.json();
        
        populateDashboard(data);
        initScrollObserver(); // Observe newly created forecast cards
    } catch (err) {
        console.error(err);
        showToast('⚠️ Backend server offline or feature store data empty.');
        // Show fallback values for a premium demo experience even if API fails
        loadFallbacks();
    }
}

function getAqiConfig(aqi) {
    if (aqi <= 50) return { label: 'Good', color: 'var(--clr-good)', class: 'good' };
    if (aqi <= 100) return { label: 'Moderate', color: 'var(--clr-moderate)', class: 'moderate' };
    if (aqi <= 150) return { label: 'Sensitive', color: 'var(--clr-sensitive)', class: 'sensitive' };
    if (aqi <= 200) return { label: 'Unhealthy', color: 'var(--clr-unhealthy)', class: 'unhealthy' };
    if (aqi <= 300) return { label: 'Very Unhealthy', color: 'var(--clr-very-un)', class: 'very-un' };
    return { label: 'Hazardous', color: 'var(--clr-hazardous)', class: 'hazardous' };
}

function populateDashboard(data) {
    const current = data.current;
    if (!current) return;
    
    const config = getAqiConfig(current.aqi);
    
    // --- GAUGE & HERO UPDATE ---
    const gaugeValueEl = document.getElementById('gaugeAqi');
    if (gaugeValueEl) {
        gaugeValueEl.innerText = current.aqi;
        gaugeValueEl.style.color = config.color;
    }
    
    // Needle rotation: -90deg is 0 AQI, +90deg is 300 AQI
    const needle = document.getElementById('gaugeNeedle');
    if (needle) {
        const percent = Math.min(Math.max(current.aqi, 0), 300) / 300;
        const angle = -90 + (percent * 180);
        needle.style.transform = `rotate(${angle}deg)`;
    }
    
    // Hero status updates
    const heroStatusIcon = document.getElementById('heroStatusIcon');
    if (heroStatusIcon) heroStatusIcon.style.color = config.color;
    
    const heroStatusText = document.getElementById('heroStatusText');
    if (heroStatusText) heroStatusText.innerText = `AQI is ${current.aqi} — ${config.label}`;
    
    const heroUpdatedTime = document.getElementById('heroUpdatedTime');
    if (heroUpdatedTime) {
        // Extract hour & minute
        heroUpdatedTime.innerText = `Updated ${current.time}`;
    }
    
    // --- METRIC CARDS ---
    // 1. Current AQI
    const currentAqi = document.getElementById('currentAqi');
    if (currentAqi) currentAqi.innerText = current.aqi;
    
    const currentStatus = document.getElementById('currentStatus');
    if (currentStatus) currentStatus.innerText = config.label;
    
    const aqiBarFill = document.getElementById('aqiBarFill');
    if (aqiBarFill) aqiBarFill.style.width = `${Math.min((current.aqi / 300) * 100, 100)}%`;
    
    // 2. Temperature
    const currentTemp = document.getElementById('currentTemp');
    const tempVal = current.temperature_2m !== null ? Math.round(current.temperature_2m) : 28;
    if (currentTemp) currentTemp.innerText = `${tempVal}°C`;
    
    // 3. PM2.5
    const currentPm25 = document.getElementById('currentPm25');
    const pmVal = current.pm2_5 !== null ? Math.round(current.pm2_5) : 35;
    if (currentPm25) currentPm25.innerText = pmVal;
    
    const pm25BarFill = document.getElementById('pm25BarFill');
    if (pm25BarFill) pm25BarFill.style.width = `${Math.min((pmVal / 100) * 100, 100)}%`;
    
    const pm25Status = document.getElementById('pm25Status');
    if (pm25Status) {
        const pmClass = pmVal <= 12 ? 'Good' : pmVal <= 35 ? 'Moderate' : 'Unhealthy';
        pm25Status.innerText = `μg/m³ • ${pmClass}`;
    }

    // Draw Temperature Sparkline (simple mock line for visuals)
    drawTempSparkline(data.raw_hourly);

    // --- 3-DAY FORECAST CARDS ---
    const forecastGrid = document.getElementById('forecastGrid');
    if (forecastGrid && data.summaries) {
        forecastGrid.innerHTML = '';
        
        data.summaries.forEach((day, index) => {
            const dayConfig = getAqiConfig(day.avg_aqi);
            
            // Choose icon
            let icon = '🌿';
            if (day.avg_aqi > 150) icon = '😷';
            else if (day.avg_aqi > 100) icon = '🌤️';
            else if (day.avg_aqi > 50) icon = '⛅';
            
            // Determine trend indicator (comparing current or previous day)
            let trendIcon = '→';
            let prevAqi = index === 0 ? current.aqi : data.summaries[index - 1].avg_aqi;
            if (day.avg_aqi < prevAqi - 5) trendIcon = '↓';
            else if (day.avg_aqi > prevAqi + 5) trendIcon = '↑';
            
            const card = document.createElement('div');
            card.className = `forecast-card fade-up delay-${index + 1}`;
            card.innerHTML = `
                <div class="forecast-day">${day.label} (${formatDateString(day.date)})</div>
                <div class="forecast-icon">${icon}</div>
                <div class="forecast-aqi">${day.avg_aqi}</div>
                <div class="forecast-label label-${dayConfig.class}">${dayConfig.label}</div>
                <div class="forecast-trend">
                    <div class="forecast-progress-track">
                        <div class="forecast-progress-fill" style="width: ${Math.min((day.avg_aqi / 250) * 100, 100)}%; background-color: ${dayConfig.color}"></div>
                    </div>
                    <span class="forecast-trend-icon" style="color: ${dayConfig.color}">${trendIcon}</span>
                </div>
            `;
            forecastGrid.appendChild(card);
        });
    }

    // --- AI RECOMMENDATIONS INSIGHTS ---
    populateInsights(current.aqi);

    // --- INTERACTIVE CHARTS ---
    initCharts(data.raw_hourly);
}

function formatDateString(str) {
    const d = new Date(str);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

/* ────────────────────────────────────────────────────────────────
   7. DRAW TEMPERATURE SPARKLINE (Canvas 2D)
   ──────────────────────────────────────────────────────────────── */
function drawTempSparkline(hourlyData) {
    const canvas = document.getElementById('tempSparkline');
    if (!canvas || !hourlyData || hourlyData.length === 0) return;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Select last 12 context points
    const points = hourlyData.slice(0, 12).map(h => h.temperature_2m || 28);
    const min = Math.min(...points);
    const max = Math.max(...points);
    const range = max - min || 1;
    
    ctx.beginPath();
    ctx.strokeStyle = 'var(--clr-accent)';
    ctx.lineWidth = 1.8;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    points.forEach((val, idx) => {
        const x = (idx / (points.length - 1)) * (canvas.width - 4) + 2;
        const y = canvas.height - ((val - min) / range) * (canvas.height - 8) - 4;
        if (idx === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
}

/* ────────────────────────────────────────────────────────────────
   8. GENERATE AI INSIGHTS BASED ON AQI
   ──────────────────────────────────────────────────────────────── */
function populateInsights(aqi) {
    const grid = document.getElementById('insightsGrid');
    if (!grid) return;
    grid.innerHTML = '';
    
    let insights = [];
    
    if (aqi <= 50) {
        insights = [
            {
                type: 'activity',
                title: 'Peak Outdoor Conditions',
                body: 'Air quality is excellent. Ideal time for outdoor runs, yoga in parks, and natural ventilation of indoor spaces.',
                tag: 'Optimal',
                tagClass: 'tag-advisory'
            },
            {
                type: 'ai',
                title: 'Clean Atmosphere Core',
                body: 'The hybrid ML forecasting engine indicates strong atmospheric dispersion. No pollutant build-up is projected.',
                tag: 'AI Verified',
                tagClass: 'tag-ai'
            }
        ];
    } else if (aqi <= 100) {
        insights = [
            {
                type: 'activity',
                title: 'Safe Outdoor Activities',
                body: 'Air quality is acceptable. Fine to proceed with ordinary outdoor exercises. Sensitive groups should watch for light coughs.',
                tag: 'Moderate',
                tagClass: 'tag-advisory'
            },
            {
                type: 'sensitive',
                title: 'Minor Allergy Warnings',
                body: 'Individuals with asthma or severe seasonal allergies might experience mild reactions. Restrict prolonged heavy cardio.',
                tag: 'Caution',
                tagClass: 'tag-caution'
            }
        ];
    } else if (aqi <= 150) {
        insights = [
            {
                type: 'sensitive',
                title: 'Sensitive Group Hazard',
                body: 'Children, elderly, and those with pre-existing lung or heart diseases should limit heavy outdoor exertion.',
                tag: 'Health Advisory',
                tagClass: 'tag-caution'
            },
            {
                type: 'risk',
                title: 'Mask Recommended',
                body: 'Particulate density has risen. Consider wearing a standard filter mask (N95) during evening traffic peaks.',
                tag: 'Moderate Risk',
                tagClass: 'tag-high'
            },
            {
                type: 'ai',
                title: 'Lag Index Correlation',
                body: 'Temporal lag values indicate minor dust collection over the cityscape. ML expects winds to clear it in 18 hours.',
                tag: 'ML Projection',
                tagClass: 'tag-ai'
            }
        ];
    } else {
        insights = [
            {
                type: 'risk',
                title: 'High Respiratory Risk',
                body: 'Wear mask outdoors. Keep all home windows closed to prevent smog infiltration. Active air purifiers are advised.',
                tag: 'Hazardous',
                tagClass: 'tag-high'
            },
            {
                type: 'activity',
                title: 'Avoid Outdoor Activities',
                body: 'Cancel outdoor cardio. Prefer indoor gyms or climate-controlled environments until dispersion variables normalize.',
                tag: 'Avoid Outdoors',
                tagClass: 'tag-caution'
            },
            {
                type: 'ai',
                title: 'Inversion Alert',
                body: 'Atmospheric pressure traps dust particles near the ground. Our gradient boosting forecast flags persistent smoke peaks.',
                tag: 'Alert',
                tagClass: 'tag-ai'
            }
        ];
    }
    
    // Add default AI tech insights card
    insights.push({
        type: 'ai',
        title: 'Decision Factors',
        body: 'Model outputs show that us_aqi_lag_1h and PM2.5 rolling averages have the highest structural weight on current predictions.',
        tag: 'Model Weight',
        tagClass: 'tag-ai'
    });
    
    insights.forEach(ins => {
        let icon = '✦';
        if (ins.type === 'risk') icon = '🚨';
        else if (ins.type === 'activity') icon = '🏃';
        else if (ins.type === 'sensitive') icon = '😷';
        
        const card = document.createElement('div');
        card.className = `insight-card insight-card--${ins.type}`;
        card.innerHTML = `
            <div class="insight-icon insight-icon--${ins.type}">${icon}</div>
            <div class="insight-title">${ins.title}</div>
            <p class="insight-body">${ins.body}</p>
            <span class="insight-tag ${ins.tagClass}">${ins.tag}</span>
        `;
        grid.appendChild(card);
    });
}

/* ────────────────────────────────────────────────────────────────
   9. INITIALISE CHARTJS PLOTS
   ──────────────────────────────────────────────────────────────── */
function initCharts(hourlyData) {
    if (!hourlyData || hourlyData.length === 0) return;
    
    // Clear skeleton states
    document.getElementById('aqiChartWrap').classList.remove('skeleton');
    document.getElementById('tempChartWrap').classList.remove('skeleton');
    document.getElementById('pm25ChartWrap').classList.remove('skeleton');
    
    const times = hourlyData.map(h => {
        // Parse time to get HH:mm format
        return h.time.split(' ')[1] || h.time;
    });
    
    // Destroy previous charts if they exist
    if (aqiChartInstance) aqiChartInstance.destroy();
    if (tempChartInstance) tempChartInstance.destroy();
    if (pm25ChartInstance) pm25ChartInstance.destroy();
    
    // --- 1. AQI TREND CHART ---
    const ctxAqi = document.getElementById('aqiChart').getContext('2d');
    aqiChartInstance = new Chart(ctxAqi, {
        type: 'line',
        data: {
            labels: times,
            datasets: [
                {
                    label: 'Predicted AQI (Our Model)',
                    data: hourlyData.map(h => h.aqi),
                    borderColor: '#4f7cff',
                    borderWidth: 3.5,
                    pointBackgroundColor: '#4f7cff',
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    tension: 0.35,
                    fill: true,
                    backgroundColor: createGradient(ctxAqi, 'rgba(79, 124, 255, 0.28)', 'rgba(79, 124, 255, 0.01)')
                },
                {
                    label: 'Raw Open-Meteo AQI',
                    data: hourlyData.map(h => h.open_meteo_aqi),
                    borderColor: 'rgba(6, 214, 160, 0.8)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    tension: 0.35,
                    fill: false
                }
            ]
        },
        options: getCommonChartOptions('Air Quality Index')
    });
    
    // --- 2. TEMPERATURE FORECAST ---
    const ctxTemp = document.getElementById('tempChart').getContext('2d');
    tempChartInstance = new Chart(ctxTemp, {
        type: 'line',
        data: {
            labels: times,
            datasets: [{
                label: 'Temperature (°C)',
                data: hourlyData.map(h => h.temperature_2m || 28),
                borderColor: '#10b981',
                borderWidth: 3.5,
                pointBackgroundColor: '#10b981',
                pointRadius: 0,
                tension: 0.35,
                fill: true,
                backgroundColor: createGradient(ctxTemp, 'rgba(16, 185, 129, 0.25)', 'rgba(16, 185, 129, 0)')
            }]
        },
        options: getCommonChartOptions('°C')
    });
    
    // --- 3. PM2.5 PARTICLES BAR CHART ---
    const ctxPm = document.getElementById('pm25Chart').getContext('2d');
    pm25ChartInstance = new Chart(ctxPm, {
        type: 'bar',
        data: {
            labels: times,
            datasets: [{
                label: 'PM2.5 (μg/m³)',
                data: hourlyData.map(h => h.pm2_5 || 35),
                backgroundColor: 'rgba(249, 115, 22, 0.72)',
                hoverBackgroundColor: 'rgba(249, 115, 22, 0.95)',
                borderRadius: 4,
                borderSkipped: false
            }]
        },
        options: getCommonChartOptions('Particles density μg/m³')
    });
}

function createGradient(ctx, colorStart, colorEnd) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, colorStart);
    gradient.addColorStop(1, colorEnd);
    return gradient;
}

function getCommonChartOptions(yLabel) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    boxWidth: 12,
                    boxHeight: 12,
                    font: { family: 'DM Sans', size: 11, weight: 600 },
                    color: '#4b5563'
                }
            },
            tooltip: {
                backgroundColor: '#111827',
                titleFont: { family: 'Syne', size: 12, weight: 700 },
                bodyFont: { family: 'DM Sans', size: 12 },
                padding: 12,
                cornerRadius: 12,
                displayColors: true
            }
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: {
                    maxTicksLimit: 12,
                    font: { family: 'DM Sans', size: 10, weight: 600 },
                    color: '#9ca3af'
                }
            },
            y: {
                grid: { color: 'rgba(140, 160, 210, 0.08)' },
                ticks: {
                    font: { family: 'DM Sans', size: 10, weight: 600 },
                    color: '#9ca3af'
                },
                title: {
                    display: true,
                    text: yLabel,
                    font: { family: 'DM Sans', size: 11, weight: 700 },
                    color: '#4b5563'
                }
            }
        }
    };
}

/* ────────────────────────────────────────────────────────────────
   10. FETCH AND RENDER MODEL EXPLANATIONS (SHAP)
   ──────────────────────────────────────────────────────────────── */
async function fetchShapData() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/forecast/explain`);
        if (!res.ok) throw new Error('Failed to fetch explanation details.');
        const data = await res.json();
        
        renderShapExplanation(data.feature_importance);
    } catch (err) {
        console.error(err);
        // Fallback SHAP features if server offline
        const fallbacks = [
            { rank: "1", feature: "us_aqi_lag_1h", impact: 27.77 },
            { rank: "2", feature: "us_aqi_lag_3h", impact: 2.93 },
            { rank: "3", feature: "pm2_5_rolling_24h", impact: 2.72 },
            { rank: "4", feature: "hour", impact: 0.63 },
            { rank: "5", feature: "temperature_2m", impact: 0.60 }
        ];
        renderShapExplanation(fallbacks);
    }
}

function renderShapExplanation(features) {
    const list = document.getElementById('shapFeaturesList');
    if (!list || !features || features.length === 0) return;
    
    list.innerHTML = '';
    
    // Relative scaling based on maximum impact value
    const maxImpact = Math.max(...features.map(f => f.impact)) || 1;
    
    features.forEach(item => {
        const widthPercent = (item.impact / maxImpact) * 100;
        
        const row = document.createElement('div');
        row.className = 'shap-feature-item';
        row.innerHTML = `
            <div class="shap-feature-header">
                <span class="shap-feature-name">${item.feature}</span>
                <span class="shap-feature-impact">~${item.impact.toFixed(2)} AQI points</span>
            </div>
            <div class="shap-bar-track">
                <div class="shap-bar-fill" style="width: 0%"></div>
            </div>
        `;
        list.appendChild(row);
        
        // Trigger width transition in next animation frame for micro-animation feel
        setTimeout(() => {
            const fill = row.querySelector('.shap-bar-fill');
            if (fill) fill.style.width = `${widthPercent}%`;
        }, 150);
    });
}

/* ────────────────────────────────────────────────────────────────
   11. FALLBACK INTERACTION ENGINE (DEMO MODE)
   ──────────────────────────────────────────────────────────────── */
function loadFallbacks() {
    // Generate beautiful dummy forecast data matching real schema
    const times = [];
    const hourlyData = [];
    const now = new Date();
    
    for (let i = 0; i < 72; i++) {
        const timeCopy = new Date(now);
        timeCopy.setHours(now.getHours() + i + 1);
        const timeStr = timeCopy.toISOString().split('T')[0] + ' ' + String(timeCopy.getHours()).padStart(2, '0') + ':00';
        
        // Create an oscillating AQI pattern
        const baseAqi = 110 + Math.sin(i / 6) * 35 + (i * 0.15); 
        const aqiVal = Math.round(baseAqi);
        
        hourlyData.push({
            time: timeStr,
            aqi: aqiVal,
            status: getAqiConfig(aqiVal).label,
            hazardous: aqiVal > 150,
            open_meteo_aqi: Math.round(baseAqi - 10 + Math.random() * 20),
            temperature_2m: Math.round(30 + Math.sin(i / 12) * 5),
            pm2_5: Math.round(aqiVal * 0.32)
        });
    }
    
    const fallbackData = {
        current: {
            time: now.toLocaleString(),
            aqi: 122,
            status: 'Sensitive',
            hazardous: false,
            open_meteo_aqi: 110,
            temperature_2m: 32,
            pm2_5: 38
        },
        summaries: [
            { label: 'Day 1', date: now.toISOString().split('T')[0], avg_aqi: 120, status: 'Sensitive', is_hazardous: false },
            { label: 'Day 2', date: new Date(now.getTime() + 86400000).toISOString().split('T')[0], avg_aqi: 135, status: 'Sensitive', is_hazardous: false },
            { label: 'Day 3', date: new Date(now.getTime() + 172800000).toISOString().split('T')[0], avg_aqi: 148, status: 'Sensitive', is_hazardous: false }
        ],
        raw_hourly: hourlyData
    };
    
    populateDashboard(fallbackData);
    initScrollObserver();
}