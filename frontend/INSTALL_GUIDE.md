# 🛠️ Installation Guide: NaMo Forbidden Archive

Follow these steps to establish your own local connection to the Forbidden Archive.

## 🗝️ Prerequisites

Before you begin, ensure you have the following:
1.  **Node.js**: Version 18.0 or higher.
2.  **Gemini API Key**: Obtainable from [Google AI Studio](https://aistudio.google.com/).
3.  **Modern Browser**: Chrome, Edge, or Brave are recommended for optimal Web Audio support.

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/icezingza/NaMo_Forbidden_Archive.git
cd NaMo_Forbidden_Archive
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your API key:
```env
API_KEY=your_gemini_api_key_here
```

### 4. Launch the Archive
Start the development server:
```bash
npm run dev
```

The archive will be accessible at `http://localhost:3000` (or the port specified by your environment).

## 🛡️ Troubleshooting

- **Audio Not Playing**: Ensure you have interacted with the page (clicked anywhere) to unlock the Browser's AudioContext.
- **Image Generation Fails**: Check if your API Key has the "Gemini 2.5 Flash" model enabled (standard for modern keys).
- **Thinking Mode Latency**: Deep Reasoning is a heavy process. It may take 10-30 seconds to generate a response depending on the complexity of the inquiry.

---
*Protocol established. The archive awaits.*
