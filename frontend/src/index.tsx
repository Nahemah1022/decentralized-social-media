import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import 'semantic-ui-css/semantic.min.css'; // Ensure Semantic UI CSS is loaded

const container = document.getElementById('root');
const root = createRoot(container!); // createRoot now accepts the container node, not the element.

root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
