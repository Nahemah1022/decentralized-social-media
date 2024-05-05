import React, {useState} from 'react';
import 'semantic-ui-css/semantic.min.css';
import AppHeader from './components/AppHeader';
import TweetForm from "./components/TweetForm";
import TweetCard from "./components/TweetCard";
import './index.css';
import '@shoelace-style/shoelace/dist/themes/light.css';
import {usePosts} from "./context/PostsProvider";

const App: React.FC = () => {
    const {posts} = usePosts();
    return (
        <div className="app-container">
            <AppHeader/>
            <div className="tweet-container">
                <TweetForm/>
                {posts.map((tweet, index) => <TweetCard key={index} tweet={tweet}/>)}
            </div>
        </div>
    );
};

export default App;
