import React from 'react';
import {createRoot} from 'react-dom/client';
import App from './App';
import 'semantic-ui-css/semantic.min.css';
import {PublicKeyProvider} from "./context/PublicKeyProvider";
import {PostsProvider} from "./context/PostsProvider"; // Ensure Semantic UI CSS is loaded

const container = document.getElementById('root');
const root = createRoot(container!); // createRoot now accepts the container node, not the element.

root.render(
    <React.StrictMode>
        <PublicKeyProvider>
            <PostsProvider>
                <App/>
            </PostsProvider>
        </PublicKeyProvider>
    </React.StrictMode>
);
