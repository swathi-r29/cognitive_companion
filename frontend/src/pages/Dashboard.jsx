import React from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  AreaChart, Area, PieChart, Pie, Cell
} from 'recharts';
import { TrendingUp, Zap, Heart, Brain, AlertTriangle, Loader2 } from 'lucide-react';
import axios from 'axios';

const Dashboard = ({ user }) => {
  const [loading, setLoading] = React.useState(true);
  const [moodTrend, setMoodTrend] = React.useState([]);
  const [emotionMap, setEmotionMap] = React.useState([]);
  const [dailyTip, setDailyTip] = React.useState({ tip: '', category: '' });
  const [summary, setSummary] = React.useState({
    total_interactions: 0,
    dominant_emotion: 'N/A',
    status: 'Unknown'
  });

  const COLORS = ['#0ea5e9', '#6366f1', '#f43f5e', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'];

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const userId = user?.id || 'guest';
        
        const [distRes, trendRes, summaryRes, tipRes] = await Promise.all([
          axios.get(`http://localhost:8000/api/analytics/mood-distribution/${userId}`),
          axios.get(`http://localhost:8000/api/analytics/mood-trends/${userId}`),
          axios.get(`http://localhost:8000/api/analytics/summary/${userId}`),
          axios.get(`http://localhost:8000/api/analytics/daily-tip/${userId}`)
        ]);

        setEmotionMap(distRes.data);
        setMoodTrend(trendRes.data);
        setSummary(summaryRes.data);
        setDailyTip(tipRes.data);
      } catch (err) {
        console.error("Failed to fetch analytics:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const StatCard = ({ title, value, icon: Icon, color, trend }) => (
    <div className="glass-card p-6 flex flex-col gap-4">
      <div className="flex justify-between items-start">
        <div className={`p-3 rounded-xl ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {trend && (
          <span className={`text-xs font-bold ${trend > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
            {trend > 0 ? '+' : ''}{trend}%
          </span>
        )}
      </div>
      <div>
        <h3 className="text-slate-500 text-sm font-medium">{title}</h3>
        <p className="text-2xl font-bold text-slate-100">{value}</p>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-slate-950/50">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-12 h-12 text-primary-500 animate-spin" />
          <p className="text-slate-400 animate-pulse">Syncing your emotional data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 h-full overflow-y-auto custom-scrollbar">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Cognitive Health Dashboard</h1>
        <p className="text-slate-400 text-sm">Real-time analysis of your emotional well-being.</p>
      </header>

      {/* Daily Tip Card */}
      {dailyTip.tip && (
        <div className="mb-8 p-6 glass-card border-primary-500/30 bg-primary-500/5 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <Heart className="w-24 h-24 text-primary-500" />
          </div>
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[10px] font-bold uppercase tracking-widest text-primary-400 bg-primary-500/10 px-2 py-0.5 rounded">
                Daily Aura Reflection • {dailyTip.category}
              </span>
            </div>
            <p className="text-xl font-medium text-slate-100 leading-relaxed max-w-3xl">
              "{dailyTip.tip}"
            </p>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Dominant Emotion" value={summary.dominant_emotion} icon={Heart} color="bg-rose-500" />
        <StatCard title="Total Interactions" value={summary.total_interactions} icon={Zap} color="bg-amber-500" />
        <StatCard title="Health Status" value={summary.status} icon={Brain} color="bg-indigo-500" />
        <StatCard title="Analysis Mode" value="Real-time" icon={AlertTriangle} color="bg-emerald-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Chart */}
        <div className="lg:col-span-2 glass-card p-8 h-[400px]">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold">7-Day Interaction Trends</h2>
            <div className="flex gap-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-primary-500" />
                <span className="text-xs text-slate-400">Activity</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-rose-500" />
                <span className="text-xs text-slate-400">Sentiment Score</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={moodTrend}>
              <defs>
                <linearGradient id="colorMood" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                itemStyle={{ color: '#f1f5f9' }}
              />
              <Area type="monotone" dataKey="messages" stroke="#0ea5e9" strokeWidth={3} fillOpacity={1} fill="url(#colorMood)" />
              <Area type="monotone" dataKey="sentiment" stroke="#f43f5e" strokeWidth={2} strokeDasharray="5 5" fill="transparent" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Emotion Pie Chart */}
        <div className="glass-card p-8 h-[400px] flex flex-col">
          <h2 className="text-lg font-bold mb-6">Mood Distribution</h2>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={emotionMap}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {emotionMap.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-y-2 gap-x-4 max-h-[100px] overflow-y-auto custom-scrollbar">
            {emotionMap.map((entry, index) => (
              <div key={entry.name} className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: COLORS[index % COLORS.length] }} />
                <span className="text-[10px] text-slate-400 capitalize truncate">{entry.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
