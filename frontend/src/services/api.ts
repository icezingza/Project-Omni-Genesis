/**
 * Project Omni-Genesis: Frontend API Client
 * Handles JWT authentication and API calls to the backend.
 */

// --- Types ---
export interface ChatRequest {
    message: string;
    voice_features?: Record<string, unknown>;
    facial_features?: Record<string, unknown>;
}

export interface ChatResponse {
    response: string;
    emotion: string;
    harmonic_score: number;
    user_id: string;
    namo_mood?: string;
    balance_index?: number;
}

export interface LoginRequest {
    user_id: string;
    password: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export interface HealthResponse {
    status: string;
    version: string;
    services: Record<string, string>;
    namo_state: Record<string, unknown>;
}

export interface DashboardResponse {
    user_id: string;
    total_interactions: number;
    top_emotions: { emotion: string; count: number }[];
    avg_harmonic_score: number;
}

// --- Configuration ---
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';
const TOKEN_KEY = 'omni_genesis_token';
const USER_KEY = 'omni_genesis_user';

// --- Token Management ---
export const getToken = (): string | null => {
    return localStorage.getItem(TOKEN_KEY);
};

export const setToken = (token: string): void => {
    localStorage.setItem(TOKEN_KEY, token);
};

export const clearToken = (): void => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
};

export const getStoredUser = (): string | null => {
    return localStorage.getItem(USER_KEY);
};

export const isAuthenticated = (): boolean => {
    return getToken() !== null;
};

// --- HTTP Helpers ---
async function apiRequest<T>(
    endpoint: string,
    options: RequestInit = {},
): Promise<T> {
    const token = getToken();
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(options.headers as Record<string, string> || {}),
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    // Handle auth errors
    if (response.status === 401) {
        clearToken();
        throw new Error('Authentication expired. Please log in again.');
    }

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `API error: ${response.status}`);
    }

    return response.json();
}

// --- Auth API ---
export const login = async (userId: string, password: string): Promise<TokenResponse> => {
    const response = await apiRequest<TokenResponse>('/auth/token', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId, password }),
    });

    setToken(response.access_token);
    localStorage.setItem(USER_KEY, userId);

    return response;
};

export const logout = (): void => {
    clearToken();
};

// --- Chat API ---
export const sendChatMessage = async (request: ChatRequest): Promise<ChatResponse> => {
    return apiRequest<ChatResponse>('/chat', {
        method: 'POST',
        body: JSON.stringify(request),
    });
};

// --- Health API ---
export const getHealth = async (): Promise<HealthResponse> => {
    return apiRequest<HealthResponse>('/health');
};

// --- NaMo API ---
export const getNamoGreeting = async (): Promise<{ greeting: string; mood: string }> => {
    return apiRequest<{ greeting: string; mood: string }>('/namo/greeting');
};

// --- Analytics API ---
export const getDashboard = async (): Promise<DashboardResponse> => {
    return apiRequest<DashboardResponse>('/analytics/dashboard');
};

export const getEmotionTrends = async (days: number = 7) => {
    return apiRequest(`/analytics/emotions?days=${days}`);
};
