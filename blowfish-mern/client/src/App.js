import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper,
  Grid,
  ThemeProvider,
  createTheme,
  CssBaseline,
  Tabs,
  Tab,
  useMediaQuery,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  AppBar,
  Toolbar,
  Menu,
  MenuItem
} from '@mui/material';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend,
  ResponsiveContainer
} from 'recharts';
import MenuIcon from '@mui/icons-material/Menu';
import SecurityIcon from '@mui/icons-material/Security';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import axios from 'axios';
import Chatbot from './components/Chatbot';
import History from './components/History';

// Update API URL to use localhost
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

// Add axios default configuration with error handling
axios.defaults.timeout = 10000; // 10 second timeout
axios.defaults.headers.common['Accept'] = 'application/json';
axios.defaults.headers.post['Content-Type'] = 'application/json';

// Add axios interceptor for debugging
axios.interceptors.request.use(request => {
  console.log('Starting Request:', request);
  return request;
});

axios.interceptors.response.use(
  response => {
    console.log('Response:', response);
    return response;
  },
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Create industrial theme
const industrialTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff6b6b',
      light: '#ff8e8e',
      dark: '#cc4a4a',
    },
    secondary: {
      main: '#4ecdc4',
      light: '#7ed9d2',
      dark: '#3da39c',
    },
    background: {
      default: '#1a1a1a',
      paper: '#2d2d2d',
    },
    error: {
      main: '#ff6b6b',
    },
    warning: {
      main: '#ffd93d',
    },
    info: {
      main: '#4ecdc4',
    },
    success: {
      main: '#95e1d3',
    },
  },
  typography: {
    fontFamily: '"Orbitron", "Roboto", "Helvetica", "Arial", sans-serif',
    h3: {
      fontWeight: 700,
      letterSpacing: '2px',
      textTransform: 'uppercase',
      fontSize: { xs: '1.5rem', sm: '2rem', md: '2.5rem' },
    },
    h5: {
      fontWeight: 600,
      letterSpacing: '1px',
      fontSize: { xs: '1.1rem', sm: '1.25rem', md: '1.5rem' },
    },
    button: {
      fontWeight: 600,
      letterSpacing: '1px',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#2d2d2d',
          borderRadius: '8px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          textTransform: 'uppercase',
          fontWeight: 600,
          padding: { xs: '8px 16px', sm: '12px 24px' },
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 6px 12px rgba(0, 0, 0, 0.2)',
          },
        },
        contained: {
          background: 'linear-gradient(45deg, #ff6b6b 30%, #ff8e8e 90%)',
          '&:hover': {
            background: 'linear-gradient(45deg, #ff8e8e 30%, #ff6b6b 90%)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: '4px',
            '&:hover .MuiOutlinedInput-notchedOutline': {
              borderColor: '#ff6b6b',
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderColor: '#ff6b6b',
            },
          },
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        root: {
          marginBottom: '20px',
          '& .MuiTabs-indicator': {
            backgroundColor: '#ff6b6b',
            height: '3px',
          },
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          color: '#ffffff',
          fontSize: { xs: '0.9rem', sm: '1.1rem' },
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: '1px',
          '&.Mui-selected': {
            color: '#ff6b6b',
          },
        },
      },
    },
  },
});

function EncryptionSection({ algorithm, title, minKeyLength, performanceData, setPerformanceData }) {
  const [text, setText] = useState('');
  const [key, setKey] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const isMobile = useMediaQuery('(max-width:600px)');

  const handleEncrypt = async () => {
    try {
      if (!text || !key) {
        setError('Please enter both text and key');
        return;
      }
      if (minKeyLength && key.length < minKeyLength) {
        setError(`Key must be at least ${minKeyLength} characters long`);
        return;
      }

      const startTime = performance.now();
      const response = await axios.post(`${API_URL}/${algorithm}/encrypt`, { text, key });
      const endTime = performance.now();
      const duration = endTime - startTime;

      setResult(response.data.encryptedText);
      setError('');
      
      // Update performance data
      const timestamp = new Date().toLocaleTimeString();
      const newData = {
        timestamp,
        time: Math.round(duration),
        operation: 'Encryption'
      };
      setPerformanceData(prevData => [...prevData, newData].slice(-10)); // Keep last 10 operations
    } catch (err) {
      console.error('Encryption error:', err);
      setError(err.response?.data?.error || 'Encryption failed');
    }
  };

  const handleDecrypt = async () => {
    try {
      if (!text || !key) {
        setError('Please enter both text and key');
        return;
      }
      if (minKeyLength && key.length < minKeyLength) {
        setError(`Key must be at least ${minKeyLength} characters long`);
        return;
      }

      const startTime = performance.now();
      const response = await axios.post(`${API_URL}/${algorithm}/decrypt`, { text, key });
      const endTime = performance.now();
      const duration = endTime - startTime;

      setResult(response.data.decryptedText);
      setError('');
      
      // Update performance data
      const timestamp = new Date().toLocaleTimeString();
      const newData = {
        timestamp,
        time: Math.round(duration),
        operation: 'Decryption'
      };
      setPerformanceData(prevData => [...prevData, newData].slice(-10)); // Keep last 10 operations
    } catch (err) {
      console.error('Decryption error:', err);
      setError(err.response?.data?.error || 'Decryption failed');
    }
  };

  return (
    <Grid container spacing={isMobile ? 2 : 3}>
      {/* Input Section */}
      <Grid item xs={12} md={6}>
        <Paper 
          elevation={3} 
          sx={{ 
            p: isMobile ? 2 : 3,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              height: '4px',
              background: 'linear-gradient(90deg, #ff6b6b, #4ecdc4)',
            },
          }}
        >
          <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
            {title} Input
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={isMobile ? 3 : 4}
            label="Text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            variant="outlined"
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Encryption Key"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            variant="outlined"
            helperText={minKeyLength ? `Minimum ${minKeyLength} characters` : ''}
            sx={{ mb: 2 }}
          />
          <Box sx={{ 
            mt: 'auto', 
            display: 'flex', 
            gap: 2,
            flexDirection: isMobile ? 'column' : 'row'
          }}>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleEncrypt}
              fullWidth
              size="large"
              startIcon={<LockIcon />}
            >
              Encrypt
            </Button>
            <Button 
              variant="contained" 
              color="secondary" 
              onClick={handleDecrypt}
              fullWidth
              size="large"
              startIcon={<LockOpenIcon />}
            >
              Decrypt
            </Button>
          </Box>
        </Paper>
      </Grid>

      {/* Result Section */}
      <Grid item xs={12} md={6}>
        <Paper 
          elevation={3} 
          sx={{ 
            p: isMobile ? 2 : 3,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              height: '4px',
              background: 'linear-gradient(90deg, #4ecdc4, #ff6b6b)',
            },
          }}
        >
          <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
            {title} Result
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={isMobile ? 3 : 4}
            value={result}
            InputProps={{ 
              readOnly: true,
              sx: { 
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '4px',
                fontFamily: 'monospace',
              }
            }}
            variant="outlined"
            sx={{ mb: 2 }}
          />
          {error && (
            <Typography color="error" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}
        </Paper>
      </Grid>
    </Grid>
  );
}

function App() {
  const [selectedTab, setSelectedTab] = useState(0);
  const [performanceData, setPerformanceData] = useState([]);
  const isMobile = useMediaQuery('(max-width:600px)');
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);

  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <ThemeProvider theme={industrialTheme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
          py: { xs: 2, sm: 4 },
          position: 'relative',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundImage: 'url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1920&q=80")',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            opacity: 0.1,
            zIndex: 0,
          },
        }}
      >
        {/* Mobile App Bar */}
        {isMobile && (
          <AppBar position="fixed" sx={{ backgroundColor: 'rgba(45, 45, 45, 0.9)', backdropFilter: 'blur(10px)' }}>
            <Toolbar>
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
                Encryption
              </Typography>
              <IconButton
                color="inherit"
                onClick={handleMenuOpen}
              >
                <SecurityIcon />
              </IconButton>
            </Toolbar>
          </AppBar>
        )}

        {/* Mobile Drawer */}
        <Drawer
          variant="temporary"
          anchor="left"
          open={drawerOpen}
          onClose={handleDrawerToggle}
          sx={{
            '& .MuiDrawer-paper': { 
              width: 240,
              backgroundColor: '#2d2d2d',
              borderRight: '1px solid rgba(255, 255, 255, 0.1)',
            },
          }}
        >
          <List>
            <ListItem button onClick={() => { setSelectedTab(0); handleDrawerToggle(); }}>
              <ListItemIcon>
                <SecurityIcon sx={{ color: '#ff6b6b' }} />
              </ListItemIcon>
              <ListItemText primary="Blowfish" />
            </ListItem>
            <ListItem button onClick={() => { setSelectedTab(1); handleDrawerToggle(); }}>
              <ListItemIcon>
                <SecurityIcon sx={{ color: '#4ecdc4' }} />
              </ListItemIcon>
              <ListItemText primary="Twofish" />
            </ListItem>
          </List>
        </Drawer>

        {/* Mobile Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          sx={{
            '& .MuiPaper-root': {
              backgroundColor: '#2d2d2d',
              border: '1px solid rgba(255, 255, 255, 0.1)',
            },
          }}
        >
          <MenuItem onClick={handleMenuClose}>About</MenuItem>
          <MenuItem onClick={handleMenuClose}>Help</MenuItem>
        </Menu>

        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1, mt: isMobile ? 8 : 0 }}>
          <Box sx={{ my: { xs: 2, sm: 4 } }}>
            <Typography 
              variant="h3" 
              component="h1" 
              gutterBottom 
              align="center"
              sx={{
                color: 'white',
                textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
                mb: { xs: 2, sm: 4 },
                position: 'relative',
                '&::after': {
                  content: '""',
                  position: 'absolute',
                  bottom: -10,
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '100px',
                  height: '4px',
                  background: 'linear-gradient(90deg, #ff6b6b, #4ecdc4)',
                  borderRadius: '2px',
                },
              }}
            >
              Encryption Algorithms
            </Typography>

            {!isMobile && (
              <Paper 
                elevation={3} 
                sx={{ 
                  mb: 4,
                  background: 'rgba(45, 45, 45, 0.9)',
                  backdropFilter: 'blur(10px)',
                }}
              >
                <Tabs
                  value={selectedTab}
                  onChange={handleTabChange}
                  centered
                  sx={{ borderBottom: 1, borderColor: 'divider' }}
                >
                  <Tab label="Blowfish" />
                  <Tab label="Twofish" />
                </Tabs>
              </Paper>
            )}

            {selectedTab === 0 && (
              <EncryptionSection 
                algorithm="blowfish"
                title="Blowfish"
                minKeyLength={8}
                performanceData={performanceData}
                setPerformanceData={setPerformanceData}
              />
            )}
            {selectedTab === 1 && (
              <EncryptionSection 
                algorithm="twofish"
                title="Twofish"
                minKeyLength={16}
                performanceData={performanceData}
                setPerformanceData={setPerformanceData}
              />
            )}

            {/* History Section */}
            <Grid item xs={12} sx={{ mt: { xs: 2, sm: 4 } }}>
              <Paper 
                elevation={3} 
                sx={{ 
                  p: { xs: 2, sm: 3 },
                  background: 'rgba(45, 45, 45, 0.9)',
                  backdropFilter: 'blur(10px)',
                }}
              >
                <History />
              </Paper>
            </Grid>

            {/* Performance Chart */}
            <Grid item xs={12} sx={{ mt: { xs: 2, sm: 4 } }}>
              <Paper 
                elevation={3} 
                sx={{ 
                  p: { xs: 2, sm: 3 },
                  background: 'rgba(45, 45, 45, 0.9)',
                  backdropFilter: 'blur(10px)',
                }}
              >
                <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
                  Performance Metrics
                </Typography>
                <Box sx={{ width: '100%', height: { xs: 300, sm: 400 } }}>
                  <ResponsiveContainer>
                    <LineChart
                      data={performanceData}
                      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                      <XAxis 
                        dataKey="timestamp" 
                        stroke="#ff6b6b"
                        tick={{ fill: '#ff6b6b' }}
                      />
                      <YAxis 
                        label={{ 
                          value: 'Time (ms)', 
                          angle: -90, 
                          position: 'insideLeft',
                          fill: '#ff6b6b'
                        }}
                        stroke="#ff6b6b"
                        tick={{ fill: '#ff6b6b' }}
                      />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#2d2d2d',
                          border: '1px solid #444',
                          borderRadius: '4px',
                        }}
                      />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="time" 
                        stroke="#ff6b6b" 
                        name="Operation Time"
                        strokeWidth={2}
                        dot={{ fill: '#ff6b6b' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Box>
              </Paper>
            </Grid>
          </Box>
        </Container>
        <Chatbot />
      </Box>
    </ThemeProvider>
  );
}

export default App;
