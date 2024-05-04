import React, { useState } from 'react';
import 'semantic-ui-css/semantic.min.css';
import AppHeader from './components/AppHeader';
import TweetForm from "./components/TweetForm";
import TweetCard from "./components/TweetCard";
import { ITweet } from './types';
import './index.css';
import AboutUs from "./components/AboutUs";
import {DEMO_TWEETS} from "./demo/tweets";

const App: React.FC = () => {
    const [tweets, setTweets] = useState<ITweet[]>(DEMO_TWEETS);
    const [currentPage, setCurrentPage] = useState('home');  // 'home' or 'about'

    const addTweet = (tweet: ITweet) => {
        setTweets([tweet, ...tweets]);
    };

    return (
        <div className="app-container">
            <AppHeader onPageChange={setCurrentPage} activePage={currentPage} />
            {currentPage === 'home' ? (
                <div className="tweet-container">
                    <TweetForm addTweet={addTweet}/>
                    {tweets.map((tweet) => (
                        <TweetCard key={tweet.id} tweet={tweet}/>
                    ))}
                </div>
            ) : (
                <AboutUs />
            )}
        </div>
    );
};

export default App;
