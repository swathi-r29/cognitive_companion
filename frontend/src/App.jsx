import React, { useState, useEffect } from 'react';
import { LayoutDashboard, MessageSquare, Shield, Settings as SettingsIcon, LogOut } from 'lucide-react';
import { auth } from './firebase';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Auth from './pages/Auth';

const App = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser({
          name: currentUser.displayName || 'User',
          id: currentUser.uid,
          email: currentUser.email
        });
      } else {
        setUser(null);
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  const handleLogout = async () => {
    try {
      await signOut(auth);
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  const navItems = [
    { id: 'chat', label: 'Companion', icon: MessageSquare },
    { id: 'dashboard', label: 'Analytics', icon: LayoutDashboard },
    { id: 'safety', label: 'Safety', icon: Shield },
  ];

  if (loading) {
    return (
      <div className="h-screen w-screen bg-[#020617] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-primary-500/20 border-t-primary-500 rounded-full animate-spin" />
          <p className="text-slate-500 font-medium animate-pulse">Initializing Aura...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Auth onAuthSuccess={(u) => setUser({ name: u.displayName || 'User', id: u.uid })} />;
  }

  return (
    <div className="flex h-screen w-screen bg-[#0f172a] text-slate-100 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 flex flex-col p-4">
        <div className="flex items-center gap-3 mb-10 px-2">
          <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/20">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <span className="font-bold text-xl tracking-tight">CognitiveMood</span>
        </div>

        <nav className="flex-1 space-y-2">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                activeTab === item.id 
                  ? 'bg-primary-600/10 text-primary-400 border border-primary-500/20 shadow-lg shadow-primary-500/5' 
                  : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-slate-800">
          <div className="flex items-center gap-3 px-2 mb-6">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary-500 to-indigo-500 flex items-center justify-center font-bold">
              {user.name[0]}
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-semibold">{user.name}</span>
              <span className="text-xs text-slate-500">Premium Member</span>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-rose-400 transition-colors"
          >
            <LogOut className="w-5 h-5" />
            <span className="font-medium">Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 relative flex flex-col overflow-hidden bg-slate-950/50">
        {activeTab === 'chat' && <Chat user={user} />}
        {activeTab === 'dashboard' && <Dashboard user={user} />}
        {activeTab === 'safety' && (
          <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">Safety & Privacy</h1>
            <p className="text-slate-400">Your data is encrypted and used only for personalized insights.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
