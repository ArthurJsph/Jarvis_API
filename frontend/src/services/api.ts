import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { handleApiError } from './notifications';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_KEY_STORAGE = 'jarvis_api_key_v1';

export const getStoredApiKey = (): string | null => {
  return localStorage.getItem(API_KEY_STORAGE);
};

export const setStoredApiKey = (key: string): void => {
  localStorage.setItem(API_KEY_STORAGE, key);
};

export const clearStoredApiKey = (): void => {
  localStorage.removeItem(API_KEY_STORAGE);
};

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add API key
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const apiKey = getStoredApiKey();
    if (apiKey && config.headers) {
      config.headers['x-api-key'] = apiKey;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    handleApiError(error);
    return Promise.reject(error);
  }
);

export default api;

// API Service methods
export const apiService = {
  // Health & Status
  health: () => api.get('/health'),
  status: () => api.get('/status'),
  capabilities: () => api.get('/capabilities'),

  // Files
  files: {
    list: (params: { path?: string; recursive?: boolean; max_depth?: number; refresh?: boolean }) =>
      api.get('/files/list', { params }),
    read: (path: string) => api.get('/files/read', { params: { path } }),
    write: (data: { path: string; content: string; overwrite?: boolean }) =>
      api.post('/files/write', data),
    delete: (path: string) => api.post('/files/delete', { path }),
  },

  // Logs
  logs: (lines: number = 200) => api.get('/logs', { params: { lines } }),

  // Documentation
  docs: {
    search: (query: string, language?: string) =>
      api.get('/doc/search', { params: { query, language } }),
    cheatsheet: (tool: string) => api.get('/doc/cheatsheet', { params: { tool } }),
  },

  // Git
  git: {
    status: () => api.get('/git/status'),
    logs: (limit: number = 10) => api.get('/git/logs', { params: { limit } }),
    pull: (remote: string = 'origin', branch?: string) =>
      api.post('/git/pull', null, { params: { remote, branch } }),
    push: (remote: string = 'origin', branch?: string) =>
      api.post('/git/push', null, { params: { remote, branch } }),
    clone: (url: string, directory?: string) =>
      api.post('/git/clone', null, { params: { url, directory } }),
  },

  // Word
  word: {
    create: (data: { filename: string; title?: string; content?: string }) =>
      api.post('/word/create', data),
    read: (filename: string) => api.get('/word/read', { params: { filename } }),
    info: (filename: string) => api.get('/word/info', { params: { filename } }),
  },

  // PowerPoint
  ppt: {
    create: (data: { filename: string; title?: string; subtitle?: string }) =>
      api.post('/ppt/create', data),
    addSlide: (data: { filename: string; slide_title: string; content?: string }) =>
      api.post('/ppt/add_slide', data),
    info: (filename: string) => api.get('/ppt/info', { params: { filename } }),
  },

  // Execute
  execute: (command: string) => api.post('/execute', { command }),
};
