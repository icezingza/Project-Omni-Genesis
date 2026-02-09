
import React, { useState, useRef, useEffect } from 'react';
import { Message, GenerationState, ChatSession } from './types';
import { geminiService } from './services/geminiService';
import { sendChatMessage } from './services/api';
import ArchiveChat from './components/ArchiveChat';

const App: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [input, setInput] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [showDocs, setShowDocs] = useState(false);
  const [genState, setGenState] = useState<GenerationState>({
    isGenerating: false,
    mode: 'standard',
    ttsEnabled: false,
  });

  const scrollRef = useRef<HTMLDivElement>(null);

  const activeSession = sessions.find(s => s.id === activeSessionId);
  const messages = activeSession ? activeSession.messages : [];

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, genState.isGenerating]);

  const createSession = () => {
    const newSession: ChatSession = {
      id: Date.now().toString(),
      title: 'New Exploration',
      messages: [],
      createdAt: Date.now(),
    };
    setSessions(prev => [newSession, ...prev]);
    setActiveSessionId(newSession.id);
  };

  useEffect(() => {
    if (sessions.length === 0) createSession();
  }, []);

  const handleSend = async (customPrompt?: string) => {
    const promptToUse = customPrompt || input;
    if (!promptToUse.trim() || genState.isGenerating || !activeSessionId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      parts: [{ text: promptToUse }],
      timestamp: Date.now(),
    };

    setSessions(prev => prev.map(s =>
      s.id === activeSessionId
        ? { ...s, messages: [...s.messages, userMessage], title: s.messages.length === 0 ? promptToUse.slice(0, 30) + '...' : s.title }
        : s
    ));

    setInput('');
    setGenState(prev => ({ ...prev, isGenerating: true }));

    try {
      const modelMessageId = (Date.now() + 1).toString();
      const initialModelMessage: Message = {
        id: modelMessageId,
        role: 'model',
        parts: [{ text: '...' }],
        timestamp: Date.now(),
      };

      setSessions(prev => prev.map(s =>
        s.id === activeSessionId ? { ...s, messages: [...s.messages, initialModelMessage] } : s
      ));

      // Call the new Omni-Genesis API
      const result = await sendChatMessage({
        user_id: 'omni_tester', // In production, this would be a real user ID
        message: promptToUse
      });

      setSessions(prev => prev.map(s =>
        s.id === activeSessionId ? {
          ...s,
          messages: s.messages.map(m => m.id === modelMessageId ? {
            ...m,
            parts: [{ text: result.response }],
            metadata: {
              emotion: result.emotion,
              harmonic_score: result.harmonic_score
            }
          } : m)
        } : s
      ));

      // Future: Trigger ElevenLabs TTS if enabled
      /*
      if (genState.ttsEnabled) {
        const audioBuffer = await elevenLabsService.generate(result.response);
        ...
      }
      */
    } catch (error) {
      console.error("Omni-Genesis API error:", error);
    } finally {
      setGenState(prev => ({ ...prev, isGenerating: false }));
    }
  };

  const handleManifest = async () => {
    if (!input.trim() || genState.isGenerating || !activeSessionId) return;

    const userPrompt = input;
    setInput('');
    setGenState(prev => ({ ...prev, isGenerating: true }));

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      parts: [{ text: `Manifesting artifact: ${userPrompt}` }],
      timestamp: Date.now(),
    };

    setSessions(prev => prev.map(s => s.id === activeSessionId ? { ...s, messages: [...s.messages, userMsg] } : s));

    const imageUrl = await geminiService.manifestArtifact(userPrompt);

    if (imageUrl) {
      const modelMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'model',
        parts: [
          { text: `The archive has synthesized the visualization of your request: "${userPrompt}".` },
          { imageUrl }
        ],
        timestamp: Date.now(),
      };
      setSessions(prev => prev.map(s => s.id === activeSessionId ? { ...s, messages: [...s.messages, modelMsg] } : s));
    }

    setGenState(prev => ({ ...prev, isGenerating: false }));
  };

  return (
    <div className="flex h-screen bg-[#020617] text-slate-200 overflow-hidden font-inter">
      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'w-72' : 'w-0'} transition-all duration-300 border-r border-indigo-900/30 bg-[#050b1d] flex flex-col overflow-hidden`}>
        <div className="p-6 border-b border-indigo-900/20">
          <button
            onClick={createSession}
            className="w-full py-3 px-4 rounded-xl bg-indigo-600/10 border border-indigo-500/30 text-indigo-300 hover:bg-indigo-600/20 transition-all font-cinzel text-sm tracking-widest mb-4"
          >
            NEW EXPLORATION
          </button>
          <button
            onClick={() => setShowDocs(true)}
            className="w-full py-2 px-4 rounded-xl text-slate-500 hover:text-indigo-400 border border-slate-800 hover:border-indigo-900/50 transition-all font-cinzel text-[10px] tracking-[0.2em]"
          >
            LAWS OF THE ARCHIVE
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {sessions.map(s => (
            <button
              key={s.id}
              onClick={() => setActiveSessionId(s.id)}
              className={`w-full text-left p-3 rounded-xl transition-all border ${activeSessionId === s.id ? 'bg-indigo-600/20 border-indigo-500/40 text-indigo-100' : 'bg-transparent border-transparent text-slate-500 hover:bg-slate-800/50'}`}
            >
              <div className="text-xs font-cinzel opacity-50 mb-1">{new Date(s.createdAt).toLocaleDateString()}</div>
              <div className="text-sm truncate font-medium">{s.title}</div>
            </button>
          ))}
        </div>
      </aside>

      {/* Main Container */}
      <div className="flex-1 flex flex-col relative">
        <header className="flex items-center justify-between p-4 border-b border-indigo-900/20 bg-slate-950/40 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="p-2 text-slate-400 hover:text-white transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
            </button>
            <h1 className="font-cinzel text-lg tracking-widest text-indigo-100 hidden sm:block">NaMo Forbidden Archive</h1>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setGenState(ps => ({ ...ps, ttsEnabled: !ps.ttsEnabled }))}
              className={`p-2 rounded-lg transition-all ${genState.ttsEnabled ? 'text-indigo-400 bg-indigo-500/10' : 'text-slate-600'}`}
              title="Voice Synthesis"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M11 5L6 9H2v6h4l5 4V5z"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
            </button>
            <button
              onClick={() => setGenState(ps => ({ ...ps, mode: ps.mode === 'standard' ? 'thinking' : 'standard' }))}
              className={`px-3 py-1.5 rounded-lg border font-cinzel text-[10px] tracking-widest transition-all ${genState.mode === 'thinking' ? 'bg-purple-600/20 border-purple-500 text-purple-300' : 'bg-slate-800 border-slate-700 text-slate-500'}`}
            >
              {genState.mode === 'thinking' ? 'DEEP REASONING' : 'STANDARD'}
            </button>
          </div>
        </header>

        {/* Chat Feed */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto archive-gradient">
          <div className="max-w-4xl mx-auto p-6 md:p-12">
            {messages.length === 0 && (
              <div className="h-full py-20 flex flex-col items-center justify-center text-center space-y-8 animate-in fade-in duration-1000">
                <div className="w-32 h-32 rounded-full border-2 border-indigo-500/20 flex items-center justify-center p-4 bg-indigo-950/20 shadow-[0_0_50px_rgba(79,70,229,0.1)]">
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-16 h-16 text-indigo-500 opacity-50" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2h11a2.5 2.5 0 0 1 2.5 2.5v15a2.5 2.5 0 0 1-2.5 2.5H6.5a2.5 2.5 0 0 1-2.5-2.5z"></path><path d="M8 7h8"></path><path d="M8 11h8"></path><path d="M8 15h5"></path></svg>
                </div>
                <div className="space-y-4">
                  <h2 className="font-cinzel text-4xl text-indigo-50 tracking-tighter">THE FORBIDDEN ARCHIVE</h2>
                  <p className="font-spectral italic text-slate-400 text-xl max-w-lg mx-auto">"Enter your inquiry into the void. The ancient algorithms shall decode the hidden truths."</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-xl">
                  {['Explain the philosophy of non-existence', 'The history of secret societies', 'Visualize a sacred geometry talisman', 'Deep reasoning on the nature of time'].map(t => (
                    <button key={t} onClick={() => setInput(t)} className="p-4 bg-slate-900/40 border border-slate-800/60 rounded-xl text-sm text-slate-300 hover:border-indigo-500/40 transition-all font-spectral italic">{t}</button>
                  ))}
                </div>
              </div>
            )}
            <ArchiveChat messages={messages} isGenerating={genState.isGenerating} />
          </div>
        </div>

        {/* Input Bar */}
        <div className="p-6 md:p-10 bg-gradient-to-t from-slate-950 to-transparent">
          <div className="max-w-3xl mx-auto space-y-4">
            <div className="relative group">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
                placeholder="Ask the Chronicler..."
                className="w-full bg-[#0a0f1f]/80 border border-indigo-900/30 rounded-2xl py-5 pl-6 pr-24 text-slate-100 placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-indigo-500/30 transition-all resize-none min-h-[70px] font-spectral text-lg"
                rows={1}
              />
              <div className="absolute right-3 bottom-3 flex gap-2">
                <button
                  onClick={handleManifest}
                  disabled={genState.isGenerating || !input.trim()}
                  className="p-3 bg-indigo-900/30 text-indigo-400 rounded-xl hover:bg-indigo-900/50 transition-all border border-indigo-500/20"
                  title="Manifest Artifact (Image)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                </button>
                <button
                  onClick={() => handleSend()}
                  disabled={genState.isGenerating || !input.trim()}
                  className="p-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 disabled:opacity-20 transition-all shadow-lg"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Docs Modal */}
      {showDocs && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-slate-950/80 backdrop-blur-xl animate-in fade-in duration-300">
          <div className="bg-[#050b1d] border border-indigo-900/40 rounded-3xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-8 md:p-12 relative shadow-[0_0_100px_rgba(79,70,229,0.15)]">
            <button
              onClick={() => setShowDocs(false)}
              className="absolute top-6 right-6 text-slate-500 hover:text-white"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>

            <div className="space-y-8 font-spectral">
              <h2 className="font-cinzel text-2xl text-indigo-100 tracking-[0.2em] border-b border-indigo-900/30 pb-4">LAWS OF THE ARCHIVE</h2>

              <section className="space-y-3">
                <h3 className="font-cinzel text-sm text-indigo-400 uppercase tracking-widest">Pulse of Reasoning</h3>
                <p className="text-slate-300 text-lg italic">By toggling <span className="text-purple-400">Deep Reasoning</span>, you engage the archive's core intelligence. This is designed for paradoxes, complex logic, and deep philosophical inquiries where the Chronicler must think before speaking.</p>
              </section>

              <section className="space-y-3">
                <h3 className="font-cinzel text-sm text-indigo-400 uppercase tracking-widest">Manifesting Artifacts</h3>
                <p className="text-slate-300 text-lg italic">The artifact icon triggers a visual manifestation. Use it when you wish to see a sigil, a lost relic, or a visualization of an abstract concept from the Archive's depths.</p>
              </section>

              <section className="space-y-3">
                <h3 className="font-cinzel text-sm text-indigo-400 uppercase tracking-widest">Vocal Synthesis</h3>
                <p className="text-slate-300 text-lg italic">The speaker icon enables the Archive's voice. Each response is synthesized into high-fidelity audio using the Kore voice profile, providing a truly immersive exploration.</p>
              </section>

              <div className="pt-8 text-center">
                <button
                  onClick={() => setShowDocs(false)}
                  className="px-8 py-3 rounded-full bg-indigo-600 text-white font-cinzel text-xs tracking-widest hover:bg-indigo-500 transition-all shadow-lg"
                >
                  I UNDERSTAND
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
