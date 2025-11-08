import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Chip,
  Stack,
} from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { useThemeMode } from '../contexts/ThemeContext';

export const TopBar: React.FC = () => {
  const { mode, toggleTheme } = useThemeMode();

  return (
    <AppBar 
      position="static" 
      elevation={2}
      sx={{ 
        zIndex: (theme) => theme.zIndex.appBar,
      }}
    >
      <Toolbar sx={{ minHeight: { xs: 56, sm: 64 } }}>
        <Stack direction="row" spacing={1} alignItems="center" sx={{ flexGrow: 1 }}>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              fontWeight: 700,
              display: { xs: 'none', sm: 'block' }
            }}
          >
            Jarvis
          </Typography>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              fontWeight: 700,
              display: { xs: 'block', sm: 'none' }
            }}
          >
            J
          </Typography>
          <Chip 
            label="Assistente Remoto" 
            size="small" 
            variant="outlined"
            sx={{ 
              display: { xs: 'none', md: 'flex' },
              borderColor: 'rgba(255, 255, 255, 0.3)'
            }}
          />
        </Stack>

        <Stack direction="row" spacing={1} alignItems="center">
          <Chip 
            label="v1.0" 
            size="small" 
            color="primary" 
            variant="filled"
            sx={{ fontWeight: 600 }}
          />
          <IconButton 
            onClick={toggleTheme} 
            color="inherit"
            size="large"
            aria-label="Toggle theme"
          >
            {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
          </IconButton>
        </Stack>
      </Toolbar>
    </AppBar>
  );
};
