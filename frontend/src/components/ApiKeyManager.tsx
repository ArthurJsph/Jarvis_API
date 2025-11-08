import React, { useState } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  IconButton,
  Typography,
  Stack,
  InputAdornment,
} from '@mui/material';
import { Visibility, VisibilityOff, Save, Clear } from '@mui/icons-material';
import { setStoredApiKey, clearStoredApiKey, getStoredApiKey } from '../services/api';
import { notify } from '../services/notifications';

interface ApiKeyManagerProps {
  onKeyChange?: (key: string) => void;
}

export const ApiKeyManager: React.FC<ApiKeyManagerProps> = ({ onKeyChange }) => {
  const [apiKey, setApiKey] = useState<string>(getStoredApiKey() || '');
  const [showKey, setShowKey] = useState(false);

  const handleSave = () => {
    if (apiKey.trim()) {
      setStoredApiKey(apiKey);
      notify.success('Chave API salva com sucesso!');
      onKeyChange?.(apiKey);
    } else {
      notify.warning('Por favor, insira uma chave API válida');
    }
  };

  const handleClear = () => {
    clearStoredApiKey();
    setApiKey('');
    notify.info('Chave API removida');
    onKeyChange?.('');
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom fontWeight={600}>
          Conexão API
        </Typography>
        
        <Stack spacing={2.5}>
          <TextField
            fullWidth
            label="Chave API"
            type={showKey ? 'text' : 'password'}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Insira sua API key"
            variant="outlined"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => setShowKey(!showKey)} edge="end">
                    {showKey ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleSave}
              disabled={!apiKey.trim()}
              fullWidth
              sx={{ height: 48 }}
            >
              Salvar
            </Button>
            <Button
              variant="outlined"
              startIcon={<Clear />}
              onClick={handleClear}
              fullWidth
              sx={{ height: 48 }}
            >
              Limpar
            </Button>
          </Stack>

          <Typography variant="caption" color="text.secondary">
            A chave é armazenada localmente no navegador
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
};
