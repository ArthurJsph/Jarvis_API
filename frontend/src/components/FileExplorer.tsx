import React, { useState } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Stack,
  FormControlLabel,
  Checkbox,
  CircularProgress,
} from '@mui/material';
import { Folder, Description, Delete, Save } from '@mui/icons-material';
import { apiService } from '../services/api';
import { notify } from '../services/notifications';

export const FileExplorer: React.FC = () => {
  const [listPath, setListPath] = useState('');
  const [readPath, setReadPath] = useState('');
  const [deletePath, setDeletePath] = useState('');
  const [writePath, setWritePath] = useState('');
  const [writeContent, setWriteContent] = useState('');
  const [recursive, setRecursive] = useState(false);
  const [maxDepth, setMaxDepth] = useState(3);
  const [overwrite, setOverwrite] = useState(true);
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleList = async () => {
    setLoading(true);
    setResult('');
    try {
      const response = await apiService.files.list({
        path: listPath,
        recursive,
        max_depth: maxDepth,
      });
      setResult(JSON.stringify(response.data, null, 2));
      notify.success('Arquivos listados com sucesso!');
    } catch {
      // Error handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  const handleRead = async () => {
    if (!readPath.trim()) return;
    setLoading(true);
    setResult('');
    try {
      const response = await apiService.files.read(readPath);
      setResult(JSON.stringify(response.data, null, 2));
      notify.success(`Arquivo ${readPath} lido com sucesso!`);
    } catch {
      // Error handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!deletePath.trim()) return;
    if (!confirm(`Tem certeza que deseja excluir: ${deletePath}?`)) return;
    setLoading(true);
    setResult('');
    try {
      const response = await apiService.files.delete(deletePath);
      setResult(JSON.stringify(response.data, null, 2));
      notify.success(`Arquivo ${deletePath} excluído com sucesso!`);
      setDeletePath('');
    } catch {
      // Error handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  const handleWrite = async () => {
    if (!writePath.trim()) return;
    setLoading(true);
    setResult('');
    try {
      const response = await apiService.files.write({
        path: writePath,
        content: writeContent,
        overwrite,
      });
      setResult(JSON.stringify(response.data, null, 2));
      notify.success(`Arquivo ${writePath} salvo com sucesso!`);
    } catch {
      // Error handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h5" gutterBottom fontWeight={600}>
          Gerenciador de Arquivos
        </Typography>

        <Stack spacing={4}>
          {/* List Files */}
          <Stack spacing={2}>
            <Typography variant="h6" color="primary" fontWeight={500}>
              Listar Arquivos
            </Typography>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <TextField
                fullWidth
                label="Caminho"
                value={listPath}
                onChange={(e) => setListPath(e.target.value)}
                placeholder="Deixe vazio para raiz"
                variant="outlined"
              />
              <Button
                variant="contained"
                onClick={handleList}
                disabled={loading}
                startIcon={<Folder />}
                sx={{ minWidth: 120, height: 56 }}
              >
                Listar
              </Button>
            </Stack>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center">
              <FormControlLabel
                control={<Checkbox checked={recursive} onChange={(e) => setRecursive(e.target.checked)} />}
                label="Recursivo"
              />
              <TextField
                type="number"
                label="Profundidade"
                value={maxDepth}
                onChange={(e) => setMaxDepth(parseInt(e.target.value) || 3)}
                sx={{ width: { xs: '100%', sm: 150 } }}
              />
            </Stack>
          </Stack>

          {/* Read File */}
          <Stack spacing={2}>
            <Typography variant="h6" color="primary" fontWeight={500}>
              Ler Arquivo
            </Typography>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <TextField
                fullWidth
                label="Caminho do arquivo"
                value={readPath}
                onChange={(e) => setReadPath(e.target.value)}
                placeholder="ex: README.md"
                variant="outlined"
              />
              <Button
                variant="contained"
                onClick={handleRead}
                disabled={loading}
                startIcon={<Description />}
                sx={{ minWidth: 120, height: 56 }}
              >
                Ler
              </Button>
            </Stack>
          </Stack>

          {/* Write File */}
          <Stack spacing={2}>
            <Typography variant="h6" color="primary" fontWeight={500}>
              Escrever Arquivo
            </Typography>
            <TextField
              fullWidth
              label="Caminho"
              value={writePath}
              onChange={(e) => setWritePath(e.target.value)}
              placeholder="ex: novo_arquivo.txt"
              variant="outlined"
            />
            <TextField
              fullWidth
              multiline
              rows={8}
              label="Conteúdo"
              value={writeContent}
              onChange={(e) => setWriteContent(e.target.value)}
              variant="outlined"
            />
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center">
              <FormControlLabel
                control={<Checkbox checked={overwrite} onChange={(e) => setOverwrite(e.target.checked)} />}
                label="Sobrescrever se existir"
                sx={{ flexGrow: 1 }}
              />
              <Button
                variant="contained"
                onClick={handleWrite}
                disabled={loading}
                startIcon={<Save />}
                sx={{ minWidth: 120, height: 56 }}
              >
                Salvar
              </Button>
            </Stack>
          </Stack>

          {/* Delete File */}
          <Stack spacing={2}>
            <Typography variant="h6" color="error" fontWeight={500}>
              Excluir Arquivo
            </Typography>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <TextField
                fullWidth
                label="Caminho do arquivo"
                value={deletePath}
                onChange={(e) => setDeletePath(e.target.value)}
                variant="outlined"
              />
              <Button
                variant="contained"
                color="error"
                onClick={handleDelete}
                disabled={loading}
                startIcon={<Delete />}
                sx={{ minWidth: 120, height: 56 }}
              >
                Excluir
              </Button>
            </Stack>
          </Stack>

          {/* Result/Error Display */}
          {loading && (
            <Stack alignItems="center" py={4}>
              <CircularProgress size={50} />
            </Stack>
          )}

          {result && !loading && (
            <TextField
              fullWidth
              multiline
              rows={15}
              value={result}
              InputProps={{ readOnly: true }}
              label="Resultado"
              variant="outlined"
              sx={{ 
                fontFamily: 'monospace',
                '& .MuiInputBase-input': {
                  fontSize: '0.9rem'
                }
              }}
            />
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};
