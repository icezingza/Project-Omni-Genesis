
import React from 'react';
import { Message } from '../types';

interface ArchiveChatProps {
  messages: Message[];
  isGenerating: boolean;
}

const ArchiveChat: React.FC<ArchiveChatProps> = ({ messages, isGenerating }) => {
  return (
    <div className="flex flex-col gap-12">
      {messages.map((msg) => (
        <div 
          key={msg.id}
          className={`flex gap-6 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} animate-in slide-in-from-bottom-2 duration-500`}
        >
          {/* Minimal Avatar */}
          <div className={`flex-shrink-0 w-8 h-8 rounded-full border flex items-center justify-center mt-2 ${
            msg.role === 'user' ? 'border-indigo-500/30 text-indigo-400' : 'border-slate-700 text-slate-500'
          }`}>
            <span className="text-[10px] font-cinzel">{msg.role === 'user' ? 'S' : 'C'}</span>
          </div>

          <div className={`flex-1 max-w-[85%] md:max-w-[80%] space-y-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            {msg.isThinking && (
              <div className="flex items-center gap-2 mb-2">
                <div className="h-[1px] flex-1 bg-gradient-to-r from-transparent to-purple-500/20"></div>
                <span className="text-[9px] font-cinzel text-purple-400/80 tracking-[0.3em] uppercase">Deep Rationalization</span>
                <div className="h-[1px] flex-1 bg-gradient-to-l from-transparent to-purple-500/20"></div>
              </div>
            )}
            
            <div className={`space-y-4 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              {msg.parts.map((part, i) => (
                <div key={i} className="w-full flex flex-col items-inherit">
                  {part.text && (
                    <div className={`font-spectral text-xl leading-relaxed whitespace-pre-wrap ${
                      msg.role === 'user' ? 'text-indigo-200/90' : 'text-slate-100'
                    }`}>
                      {part.text}
                    </div>
                  )}
                  {part.imageUrl && (
                    <div className="mt-4 rounded-2xl overflow-hidden border border-indigo-500/20 shadow-2xl max-w-md mx-auto sm:mx-0">
                      <img src={part.imageUrl} alt="Artifact" className="w-full h-auto" />
                      <div className="bg-indigo-950/30 px-4 py-2 border-t border-indigo-500/10 flex justify-between items-center">
                        <span className="text-[10px] font-cinzel text-indigo-400 tracking-widest">ARTIFACT MANIFESTED</span>
                        <a href={part.imageUrl} download="artifact.png" className="text-indigo-400 hover:text-white transition-colors">
                          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                        </a>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      ))}

      {isGenerating && (
        <div className="flex gap-6 animate-pulse">
           <div className="w-8 h-8 rounded-full border border-slate-700 flex items-center justify-center mt-2">
             <div className="w-2 h-2 bg-indigo-500 rounded-full animate-ping"></div>
           </div>
           <div className="space-y-4 w-full pt-4">
             <div className="h-4 bg-slate-800/40 rounded-full w-3/4"></div>
             <div className="h-4 bg-slate-800/40 rounded-full w-1/2"></div>
           </div>
        </div>
      )}
    </div>
  );
};

export default ArchiveChat;
