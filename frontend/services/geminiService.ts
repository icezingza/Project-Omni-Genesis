
import { GoogleGenAI, Modality, GenerateContentResponse, Type } from "@google/genai";
import { decode, decodeAudioData } from "../utils/audio";

const API_KEY = process.env.API_KEY || "";

export class GeminiService {
  private ai: GoogleGenAI;

  constructor() {
    this.ai = new GoogleGenAI({ apiKey: API_KEY });
  }

  async *generateResponseStream(
    prompt: string,
    history: { role: string; parts: { text: string }[] }[],
    useThinking: boolean = false
  ) {
    const model = useThinking ? 'gemini-3-pro-preview' : 'gemini-3-flash-preview';
    
    const config: any = {
      systemInstruction: `You are the Chronicler of the NaMo Forbidden Archive. 
      The archive contains lost knowledge, mystical secrets, and profound insights. 
      Your tone is cryptic yet helpful, ancient, and deeply intellectual. 
      When users ask for "artifacts" or "visualizations", use your descriptive power.
      If the user wants to see something, describe it vividly first.`,
    };

    if (useThinking) {
      config.thinkingConfig = { thinkingBudget: 32768 };
    }

    const stream = await this.ai.models.generateContentStream({
      model,
      contents: [...history, { role: 'user', parts: [{ text: prompt }] }],
      config,
    });

    for await (const chunk of stream) {
      yield chunk.text || "";
    }
  }

  async manifestArtifact(prompt: string): Promise<string | null> {
    try {
      const response = await this.ai.models.generateContent({
        model: 'gemini-2.5-flash-image',
        contents: {
          parts: [{ text: `A mystical, ancient, forbidden artifact or scroll from an ethereal archive representing: ${prompt}. Cinematic lighting, highly detailed, occult aesthetic, gold and obsidian textures, 4k.` }]
        },
        config: {
          imageConfig: { aspectRatio: "1:1" }
        }
      });

      for (const part of response.candidates[0].content.parts) {
        if (part.inlineData) {
          return `data:image/png;base64,${part.inlineData.data}`;
        }
      }
      return null;
    } catch (error) {
      console.error("Manifestation Error:", error);
      return null;
    }
  }

  async generateTTS(text: string): Promise<AudioBuffer | null> {
    try {
      const response = await this.ai.models.generateContent({
        model: "gemini-2.5-flash-preview-tts",
        contents: [{ parts: [{ text: `Read this with mystical, calm authority: ${text}` }] }],
        config: {
          responseModalities: [Modality.AUDIO],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: { voiceName: 'Kore' },
            },
          },
        },
      });

      const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
      if (!base64Audio) return null;

      const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
      const decodedData = decode(base64Audio);
      return await decodeAudioData(decodedData, audioCtx, 24000, 1);
    } catch (error) {
      console.error("TTS Generation Error:", error);
      return null;
    }
  }

  async playAudioBuffer(buffer: AudioBuffer) {
    const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
    const source = audioCtx.createBufferSource();
    source.buffer = buffer;
    source.connect(audioCtx.destination);
    source.start();
  }
}

export const geminiService = new GeminiService();
