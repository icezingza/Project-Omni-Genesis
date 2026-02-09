
export type Role = 'user' | 'model';

export interface MessagePart {
  text?: string;
  imageUrl?: string;
}

export interface Message {
  id: string;
  role: Role;
  parts: MessagePart[];
  timestamp: number;
  isThinking?: boolean;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
}

export interface GenerationState {
  isGenerating: boolean;
  mode: 'standard' | 'thinking';
  ttsEnabled: boolean;
}
