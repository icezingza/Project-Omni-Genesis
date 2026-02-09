export interface ChatRequest {
    user_id: string;
    message: string;
}

export interface ChatResponse {
    response: string;
    emotion: string;
    harmonic_score: number;
    user_id: string;
}

const API_BASE_URL = '/api';

export const sendChatMessage = async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send message');
    }

    return response.json();
};
