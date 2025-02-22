import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';

console.log('Starting the application...'); // Debug line

const rootElement = document.getElementById('root');
if (rootElement) {
  console.log('Root element found, rendering App...'); // Debug line
  createRoot(rootElement).render(<App />);
} else {
  console.error('Root element not found'); // Debug line
}
