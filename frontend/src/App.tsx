import React, {useState} from 'react';
import 'semantic-ui-css/semantic.min.css';
import AppHeader from './components/AppHeader';
import TweetForm from "./components/TweetForm";
import TweetCard from "./components/TweetCard";
import './index.css';
import AboutUs from "./components/AboutUs";
import '@shoelace-style/shoelace/dist/themes/light.css';
import {setBasePath} from '@shoelace-style/shoelace/dist/utilities/base-path';
import {usePosts} from "./context/PostsProvider";

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.15.0/cdn/');

const App: React.FC = () => {
    const {posts} = usePosts();
    const [currentPage, setCurrentPage] = useState('home'); // 'home' or 'about'

    return (
        <div className="app-container">
            <AppHeader onPageChange={setCurrentPage} activePage={currentPage}/>
            {currentPage === 'home'
                ?
                <div className="tweet-container">
                    <TweetForm/>
                    {posts.map((tweet) => <TweetCard key={tweet.id} tweet={tweet}/>)}
                </div>
                :
                <AboutUs/>
            }
        </div>
    );
};

export default App;
