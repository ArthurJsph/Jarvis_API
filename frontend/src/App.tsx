import { Box, Stack } from '@mui/material';
import { SnackbarProvider } from 'notistack';
import { ThemeProvider } from './contexts/ThemeContext';
import { TopBar } from './components/TopBar';
import { ApiKeyManager } from './components/ApiKeyManager';
import { FileExplorer } from './components/FileExplorer';
import { GitPanel } from './components/GitPanel';

function App() {
  return (
    <ThemeProvider>
      <SnackbarProvider 
        maxSnack={3}
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        autoHideDuration={4000}
      >
        <Box 
          sx={{ 
            display: 'flex',
            flexDirection: 'column',
            height: '100vh',
            width: '100vw',
            bgcolor: 'background.default',
            overflow: 'hidden'
          }}
        >
        <TopBar />
        
        <Box
          component="main"
          sx={{ 
            flexGrow: 1,
            width: '100%',
            p: { xs: 2, sm: 3, md: 4 },
            overflow: 'auto'
          }}
        >
          <Stack 
            direction={{ xs: 'column', lg: 'row' }} 
            spacing={3}
            sx={{ 
              width: '100%',
              maxWidth: '1800px',
              margin: '0 auto'
            }}
          >
            {/* Left Sidebar */}
            <Box 
              sx={{ 
                width: { xs: '100%', lg: '400px' },
                flexShrink: 0 
              }}
            >
              <Stack spacing={3}>
                <ApiKeyManager />
                <GitPanel />
              </Stack>
            </Box>

            {/* Main Content */}
            <Box 
              sx={{ 
                flexGrow: 1,
                minWidth: 0,
                width: '100%'
              }}
            >
              <FileExplorer />
            </Box>
          </Stack>
        </Box>
      </Box>
      </SnackbarProvider>
    </ThemeProvider>
  );
}

export default App;
