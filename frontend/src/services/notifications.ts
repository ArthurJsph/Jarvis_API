import { enqueueSnackbar } from 'notistack';

export const notify = {
  success: (message: string) => {
    enqueueSnackbar(message, { variant: 'success' });
  },
  error: (message: string) => {
    enqueueSnackbar(message, { variant: 'error' });
  },
  warning: (message: string) => {
    enqueueSnackbar(message, { variant: 'warning' });
  },
  info: (message: string) => {
    enqueueSnackbar(message, { variant: 'info' });
  },
};

export const handleApiError = (error: unknown): string => {
  if (typeof error === 'object' && error !== null) {
    const err = error as any;
    
    // Erro de autenticação
    if (err.response?.status === 401 || err.response?.status === 403) {
      const message = 'API Key inválida ou expirada. Configure uma nova chave.';
      notify.error(message);
      return message;
    }
    
    // Erro de validação
    if (err.response?.status === 422) {
      const message = err.response?.data?.detail || 'Dados inválidos enviados';
      notify.error(message);
      return message;
    }
    
    // Erro do servidor
    if (err.response?.status >= 500) {
      const message = 'Erro no servidor. Tente novamente mais tarde.';
      notify.error(message);
      return message;
    }
    
    // Erro de conexão
    if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
      const message = 'Tempo de conexão esgotado. Verifique sua conexão.';
      notify.error(message);
      return message;
    }
    
    if (err.code === 'ERR_NETWORK' || err.message?.includes('Network Error')) {
      const message = 'Erro de conexão. Verifique se o backend está rodando.';
      notify.error(message);
      return message;
    }
    
    // Erro genérico da API
    const message = err.response?.data?.detail || err.message || 'Erro desconhecido';
    notify.error(message);
    return message;
  }
  
  const message = 'Erro desconhecido';
  notify.error(message);
  return message;
};
