import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Chat = ({ user }) => {
  const [messages, setMessages] = useState([
    { id: 1, role: 'bot', content: `Hello ${user?.name || ''}! I'm Aura, your cognitive companion. How are you feeling today?`, timestamp: new Date() }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef(null);
  const ws = useRef(null);

  useEffect(() => {
    // Initialize WebSocket
    const userId = user?.id || "guest";
    ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${userId}`);

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'BOT_RESPONSE') {
        setIsTyping(false);
        setMessages(prev => [...prev, {
          id: Date.now(),
          role: 'bot',
          content: data.content,
          metadata: data.metadata,
          timestamp: new Date()
        }]);
      }
    };

    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    ws.current.send(JSON.stringify({ content: input }));
    setInput('');
    setIsTyping(true);
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full p-4 lg:p-8">
      {/* Header Info */}
      <div className="flex items-center justify-between mb-6 p-4 glass-card border-primary-500/10">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-sm font-medium text-slate-300">Aura AI • Emotionally Aware</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <Info className="w-4 h-4" />
          <span>Session encrypted</span>
        </div>
      </div>

      {/* Message Area */}
      <div className="flex-1 overflow-y-auto custom-scrollbar pr-4 space-y-6">
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 shadow-lg ${
                  msg.role === 'user' ? 'bg-indigo-600' : 'bg-slate-800'
                }`}>
                  {msg.role === 'user' ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-primary-400" />}
                </div>
                
                <div className="space-y-1">
                  <div className={`px-4 py-3 rounded-2xl ${
                    msg.role === 'user' 
                      ? 'bg-indigo-600 text-white rounded-tr-none' 
                      : 'bg-slate-800/80 text-slate-200 border border-slate-700/50 rounded-tl-none'
                  }`}>
                    <p className="text-sm leading-relaxed">{msg.content}</p>
                  </div>
                  
                  {msg.metadata && (
                    <div className="flex gap-2 items-center px-1">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-primary-500 bg-primary-500/10 px-2 py-0.5 rounded">
                        {msg.metadata.emotion}
                      </span>
                      {msg.metadata.is_crisis && (
                        <span className="text-[10px] font-bold uppercase tracking-wider text-rose-500 bg-rose-500/10 px-2 py-0.5 rounded">
                          Crisis Escalation
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex gap-3 max-w-[80%]">
              <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center shrink-0">
                <Bot className="w-5 h-5 text-primary-400" />
              </div>
              <div className="px-4 py-3 bg-slate-800/40 rounded-2xl rounded-tl-none flex items-center gap-2">
                <Loader2 className="w-4 h-4 text-slate-500 animate-spin" />
                <span className="text-sm text-slate-500 italic">Aura is thinking...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      {/* Input Area */}
      <div className="mt-6">
        <div className="relative group">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your thoughts here..."
            className="w-full bg-slate-800/50 border border-slate-700 rounded-2xl px-6 py-4 pr-16 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all text-slate-200 placeholder:text-slate-500"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim()}
            className="absolute right-3 top-3 p-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white disabled:opacity-50 disabled:hover:bg-primary-600 transition-all shadow-lg shadow-primary-500/20"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <p className="mt-3 text-center text-[11px] text-slate-600">
          Aura is an AI support companion and not a replacement for professional therapy.
        </p>
      </div>
    </div>
  );
};

export default Chat;
