import React, {useState} from 'react';
import 'semantic-ui-css/semantic.min.css';
import AppHeader from './components/AppHeader';
import TweetForm from "./components/TweetForm";
import TweetCard from "./components/TweetCard";
import './index.css';
import '@shoelace-style/shoelace/dist/themes/light.css';
import {usePosts} from "./context/PostsProvider";
import {useUser} from "./context/UserProvider";
import {ITweet} from "./types";

const App: React.FC = () => {
    const {posts} = usePosts();
    const {usersMap, addUser} = useUser();
    return (
        <div className="app-container">
            <AppHeader/>
            <div className="tweet-container">
                <TweetForm/>
                {posts.map((post, index) => {
                    if (!usersMap.has(post.publicKey)) {
                        addUser(post.publicKey);
                    }
                    const user = usersMap.get(post.publicKey);
                    if (!user) {
                        console.error('User should be valid here.');
                        return;
                    }
                    const tweet: ITweet = {
                        id: index,
                        author: user.username,
                        publicKey: post.publicKey,
                        content: post.content,
                        createdAt: '',
                        avatarUrl: user.avatarPath
                    };
                    return <TweetCard key={index} tweet={tweet}/>;
                })}
            </div>
        </div>
    );
};

export default App;
