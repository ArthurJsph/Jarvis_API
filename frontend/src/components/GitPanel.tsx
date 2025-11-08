import React, { useState } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Stack,
  CircularProgress,
} from '@mui/material';
import { Code, PlayArrow } from '@mui/icons-material';
import { apiService } from '../services/api';
import { notify } from '../services/notifications';

export const GitPanel: React.FC = () => {
  const [remote, setRemote] = useState('origin');
  const [branch, setBranch] = useState('');
  const [cloneUrl, setCloneUrl] = useState('');
  const [cloneDir, setCloneDir] = useState('');
  const [logLimit, setLogLimit] = useState(10);
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleAction = async (action: () => Promise<unknown>, successMsg: string) => {
    setLoading(true);
    setResult('');
    try {
      const response = await action();
      setResult(JSON.stringify((response as { data: unknown }).data, null, 2));
      notify.success(successMsg);
    } catch {
      // Error handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom fontWeight={600}>
          Git Manager
        </Typography>

        <Stack spacing={3}>
          {/* Status & Logs */}
          <Stack spacing={2}>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <Button
                variant="outlined"
                onClick={() => handleAction(() => apiService.git.status(), 'Status obtido com sucesso!')}
                disabled={loading}
                startIcon={<Code />}
                fullWidth
                sx={{ height: 48 }}
              >
                Status
              </Button>
              <Button
                variant="outlined"
                onClick={() => handleAction(() => apiService.git.logs(logLimit), 'Logs carregados com sucesso!')}
                disabled={loading}
                fullWidth
                sx={{ height: 48 }}
              >
                Logs ({logLimit})
              </Button>
            </Stack>
            <TextField
              type="number"
              label="Limite de Logs"
              value={logLimit}
              onChange={(e) => setLogLimit(parseInt(e.target.value) || 10)}
              fullWidth
              variant="outlined"
            />
          </Stack>

          {/* Pull & Push */}
          <Stack spacing={2}>
            <Typography variant="subtitle1" fontWeight={500}>
              Pull / Push
            </Typography>
            <TextField
              label="Remote"
              value={remote}
              onChange={(e) => setRemote(e.target.value)}
              variant="outlined"
              fullWidth
            />
            <TextField
              label="Branch (opcional)"
              value={branch}
              onChange={(e) => setBranch(e.target.value)}
              variant="outlined"
              fullWidth
            />
            <Stack direction="row" spacing={2}>
              <Button
                variant="contained"
                onClick={() => handleAction(() => apiService.git.pull(remote, branch), 'Pull realizado com sucesso!')}
                disabled={loading}
                fullWidth
                sx={{ height: 48 }}
              >
                ⬇️ Pull
              </Button>
              <Button
                variant="contained"
                onClick={() => handleAction(() => apiService.git.push(remote, branch), 'Push realizado com sucesso!')}
                disabled={loading}
                fullWidth
                sx={{ height: 48 }}
              >
                ⬆️ Push
              </Button>
            </Stack>
          </Stack>

          {/* Clone */}
          <Stack spacing={2}>
            <Typography variant="subtitle1" fontWeight={500}>
              Clonar Repositório
            </Typography>
            <TextField
              fullWidth
              label="URL do repositório"
              value={cloneUrl}
              onChange={(e) => setCloneUrl(e.target.value)}
              placeholder="https://github.com/user/repo.git"
              variant="outlined"
            />
            <TextField
              fullWidth
              label="Diretório (opcional)"
              value={cloneDir}
              onChange={(e) => setCloneDir(e.target.value)}
              variant="outlined"
            />
            <Button
              variant="contained"
              onClick={() => handleAction(() => apiService.git.clone(cloneUrl, cloneDir), 'Repositório clonado com sucesso!')}
              disabled={loading || !cloneUrl.trim()}
              startIcon={<PlayArrow />}
              fullWidth
              sx={{ height: 48 }}
            >
              Clonar
            </Button>
          </Stack>

          {/* Result/Error Display */}
          {loading && (
            <Stack alignItems="center" py={2}>
              <CircularProgress size={40} />
            </Stack>
          )}

          {result && !loading && (
            <TextField
              fullWidth
              multiline
              rows={12}
              value={result}
              InputProps={{ readOnly: true }}
              label="Resultado"
              variant="outlined"
              sx={{ 
                fontFamily: 'monospace',
                '& .MuiInputBase-input': {
                  fontSize: '0.85rem'
                }
              }}
            />
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};
