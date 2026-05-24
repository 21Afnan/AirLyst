import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area 
} from 'recharts';
import { 
  Wind, Thermometer, CloudRain, AlertTriangle, CheckCircle, Info, RefreshCcw, MapPin 
} from 'lucide-react';

const API_BASE_URL = 'http://127.0.0.1:8000/api/forecast';

const MOCK_DATA = {
  current: {
    aqi: 72,
    status: "Moderate",
    time: "2026-05-24 14:00"
  },
  summaries: [
    { label: "Day 1", date: "2026-05-24", avg_aqi: 68, status: "Moderate" },
    { label: "Day 2", date: "2026-05-25", avg_aqi: 54, status: "Good" },
    { label: "Day 3", date: "2026-05-26", avg_aqi: 95, status: "Moderate" },
  ],
  hourly_forecast: Array.from({ length: 72 }, (_, i) => ({
    time: `2026-05-24 ${String(i % 24).padStart(2, '0')}:00`,
    aqi: 60 + Math.sin(i / 5) * 20 + Math.random() * 10,
    pm25: 15 + Math.random() * 5,
    temp: 28 + Math.random() * 5
  }))
};

const App = () => {
  const [data, setData] = useState(MOCK_DATA);
  const [loading, setLoading] = useState(false);
  const [isDemo, setIsDemo] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(API_BASE_URL);
      setData(response.data);
      setIsDemo(false);
    } catch (err) {
      console.warn("Backend not found, staying in Demo Mode");
      setData(MOCK_DATA);
      setIsDemo(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getStatusColor = (status) => {
    if (!status) return 'bg-gray-500';
    const s = status.toLowerCase();
    if (s.includes('good')) return 'emerald';
    if (s.includes('moderate')) return 'yellow';
    if (s.includes('unhealthy (sg)')) return 'orange';
    if (s.includes('unhealthy')) return 'red';
    if (s.includes('very unhealthy')) return 'purple';
    return 'rose';
  };

  const statusColor = getStatusColor(data?.current?.status);

  const statusConfig = {
    emerald: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', glow: 'from-emerald-400/20', icon: 'text-emerald-500' },
    yellow: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', glow: 'from-amber-400/20', icon: 'text-amber-500' },
    orange: { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-200', glow: 'from-orange-400/20', icon: 'text-orange-500' },
    red: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200', glow: 'from-rose-400/20', icon: 'text-rose-500' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200', glow: 'from-purple-400/20', icon: 'text-purple-500' },
    rose: { bg: 'bg-slate-50', text: 'text-slate-700', border: 'border-slate-200', glow: 'from-slate-400/10', icon: 'text-slate-500' }
  };

  const activeStatus = statusConfig[statusColor] || statusConfig.rose;

  return (
    <div className="min-h-screen bg-[#fcfdfe] text-slate-900 font-sans selection:bg-blue-100 selection:text-blue-900 overflow-x-hidden flex flex-col">
      {/* Immersive Weather Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className={`absolute -top-[20%] -right-[10%] w-[70%] h-[70%] rounded-full blur-[150px] opacity-30 transition-all duration-1000 bg-gradient-to-br ${activeStatus.glow} to-blue-50`}></div>
        <div className="absolute top-[30%] -left-[10%] w-[50%] h-[50%] rounded-full blur-[130px] opacity-20 bg-cyan-100 animate-pulse"></div>
        <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-white to-transparent opacity-80"></div>
      </div>

      <div className="relative z-10 flex-grow flex flex-col items-stretch">
        {/* Full-width Top Navbar */}
        <nav className="w-full backdrop-blur-2xl bg-white/60 border-b border-slate-100 px-6 md:px-12 py-4 flex justify-between items-center sticky top-0 z-50 shadow-sm">
          <div className="flex items-center gap-4 group cursor-pointer">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-500 rounded-2xl flex items-center justify-center shadow-2xl shadow-blue-200 group-hover:scale-110 transition-all duration-500 ease-out">
              <Wind className="text-white w-7 h-7 animate-bounce" />
            </div>
            <div>
              <h1 className="text-2xl font-[1000] tracking-tighter text-slate-900 leading-none">
                AIR<span className="text-blue-600">LYST</span>
              </h1>
              <p className="text-[9px] text-blue-500 font-black uppercase tracking-[0.3em] mt-1">Global Aero Intelligence</p>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden lg:flex items-center gap-3 bg-white/80 px-5 py-2.5 rounded-2xl border border-slate-100 shadow-sm">
              <div className="flex flex-col items-end">
                <span className="text-[10px] text-slate-400 font-black uppercase tracking-tighter leading-none">Station</span>
                <span className="text-sm font-black text-slate-800">Islamabad HQ</span>
              </div>
              <div className="w-8 h-8 rounded-full bg-rose-50 flex items-center justify-center">
                <MapPin className="w-4 h-4 text-rose-500" />
              </div>
            </div>
            
            <button 
              onClick={fetchData}
              className="group flex items-center gap-2 px-5 py-3 bg-slate-900 hover:bg-blue-600 text-white rounded-2xl transition-all duration-500 shadow-xl shadow-slate-200 hover:shadow-blue-200 active:scale-95"
            >
              <RefreshCcw className={`w-4 h-4 ${loading ? 'animate-spin' : 'group-hover:rotate-180 transition-transform duration-700'}`} />
            </button>
          </div>
        </nav>

        {/* Full Page Content */}
        <main className="flex-grow p-6 md:p-12 max-w-[1800px] mx-auto w-full grid grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
          
          {/* Main Display: Massive Hero Unit */}
          <div className="col-span-12 xl:col-span-7 flex flex-col gap-8">
            <div className="relative bg-white rounded-[3.5rem] p-12 md:p-16 border border-white shadow-[0_40px_100px_-20px_rgba(0,0,0,0.06)] overflow-hidden transition-all hover:shadow-[0_50px_120px_-20px_rgba(0,0,0,0.08)] group hover:-translate-y-1 duration-500">
              <div className="absolute top-0 left-0 w-full h-full opacity-[0.03] pointer-events-none bg-[radial-gradient(#3b82f6_1px,transparent_1px)] [background-size:20px_20px]"></div>
              
              <div className="relative z-10 flex flex-col h-full">
                <div className="flex justify-between items-start mb-16">
                  <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-3">
                       <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.5)] animate-pulse"></span>
                       <span className="text-xs font-black text-slate-400 uppercase tracking-widest italic">Streaming Live Intelligence</span>
                    </div>
                    <p className="text-sm text-slate-500 font-medium ml-6 italic">Validated at {data?.current?.time}</p>
                  </div>
                  <div className={`px-6 py-2.5 rounded-2xl text-[10px] font-black tracking-[0.2em] border shadow-sm transition-all duration-700 ${activeStatus.bg} ${activeStatus.text} ${activeStatus.border}`}>
                    {data?.current?.status?.toUpperCase()}
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-12 mb-16">
                  <div className="relative flex items-end translate-x-[-10px]">
                    <h2 className="text-[13rem] leading-none font-[1000] tracking-tighter text-slate-900 drop-shadow-2xl select-none">
                      {data?.current?.aqi}
                    </h2>
                    <div className="flex flex-col mb-10 translate-x-[-10px]">
                       <span className="text-5xl font-black text-slate-200 tracking-tighter">AQI</span>
                       <span className="text-xs font-bold text-blue-500 leading-none mt-2">Predicted Value</span>
                    </div>
                  </div>

                  <div className="flex flex-col gap-8 flex-grow">
                    <div className="bg-slate-50/50 backdrop-blur-md p-6 rounded-[2.5rem] border border-slate-100/50">
                      <p className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4">Precision Metrics</p>
                      <div className="grid grid-cols-2 gap-6">
                        {[
                          { val: '28°', label: 'Ambient Temp', icon: Thermometer, color: 'text-orange-500' },
                          { val: '12km', label: 'Drift Speed', icon: Wind, color: 'text-blue-500' },
                        ].map((s, i) => (
                          <div key={i} className="flex flex-col">
                            <span className="text-2xl font-black text-slate-800">{s.val}</span>
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">{s.label}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-auto grid grid-cols-1 md:grid-cols-2 gap-6">
                   <div className={`flex gap-5 p-6 rounded-[2.5rem] border transition-all duration-500 ${activeStatus.bg} ${activeStatus.border}`}>
                      <div className={`w-12 h-12 rounded-2xl ${activeStatus.bg} border-2 ${activeStatus.border} flex items-center justify-center shadow-sm`}>
                         <Info className={`w-6 h-6 ${activeStatus.icon}`} />
                      </div>
                      <div className="flex flex-col justify-center">
                         <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Health Advisory</span>
                         <p className={`text-sm font-black leading-tight ${activeStatus.text}`}>
                           {statusColor === 'emerald' ? 'Ideal conditions for peak performance.' : 'Sensitivity detected. Take pre-emptive measures.'}
                         </p>
                      </div>
                   </div>
                   <div className="bg-slate-900 rounded-[2.5rem] p-6 flex flex-col justify-center hover:bg-slate-800 transition-colors shadow-2xl shadow-slate-200">
                      <p className="text-slate-400 text-[10px] font-black uppercase tracking-[0.2em] mb-2">Network Status</p>
                      <div className="flex items-center justify-between">
                         <span className="text-white font-black text-sm tracking-tight italic">Hybrid ML Model 4.7.2</span>
                         <div className="flex gap-1">
                           {[1, 2, 3].map(i => <div key={i} className="w-1.5 h-4 rounded-full bg-blue-500 opacity-50 first:opacity-100 last:bg-emerald-500"></div>)}
                         </div>
                      </div>
                   </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Section: Aggregated Insights */}
          <div className="col-span-12 xl:col-span-5 flex flex-col gap-8">
            <div className="grid grid-cols-3 gap-4">
              {data?.summaries?.map((day, idx) => {
                const dayColor = getStatusColor(day.status);
                const config = statusConfig[dayColor] || statusConfig.rose;
                return (
                  <div key={idx} className="group relative bg-white rounded-[2.5rem] p-6 border border-white shadow-xl shadow-slate-200/50 transition-all duration-500 hover:-translate-y-2 overflow-hidden flex flex-col items-center text-center">
                    <p className="text-[9px] font-black text-blue-500 uppercase tracking-widest mb-1 italic">{day.label}</p>
                    <span className="text-4xl font-[1000] text-slate-900 tracking-tighter mb-4">{day.avg_aqi}</span>
                    <div className={`text-[8px] font-black px-3 py-1.5 rounded-xl uppercase tracking-widest border transition-colors ${config.bg} ${config.text} ${config.border}`}>
                      {day.status}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="bg-white rounded-[3.5rem] p-10 border border-white shadow-[0_40px_100px_-20px_rgba(0,0,0,0.06)] flex flex-col flex-grow min-h-[500px]">
                <div className="flex justify-between items-center mb-12">
                  <div className="flex flex-col">
                    <h3 className="text-xl font-black text-slate-900 leading-none">Aero Momentum</h3>
                    <p className="text-[10px] text-slate-400 font-black uppercase tracking-[0.2em] mt-2">72H AI Prediction Engine</p>
                  </div>
                </div>
                
                <div className="flex-grow w-full relative">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data?.hourly_forecast}>
                      <defs>
                        <linearGradient id="colorAqiHuge" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="12 12" stroke="#f1f5f9" vertical={false} />
                      <XAxis 
                        dataKey="time" 
                        stroke="#e2e8f0" 
                        fontSize={9} 
                        fontWeight="900"
                        tickFormatter={(t) => t.split(' ')[1]}
                        interval={12}
                        axisLine={false}
                        tickLine={false}
                      />
                      <YAxis stroke="#e2e8f0" fontSize={9} fontWeight="900" axisLine={false} tickLine={false} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '24px', padding: '20px' }}
                        itemStyle={{ color: '#fff', fontWeight: '900', fontSize: '16px' }}
                        labelStyle={{ color: '#64748b', fontSize: '10px', marginBottom: '8px', textTransform: 'uppercase' }}
                      />
                      <Area type="monotone" dataKey="aqi" stroke="#2563eb" strokeWidth={5} fillOpacity={1} fill="url(#colorAqiHuge)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default App;
