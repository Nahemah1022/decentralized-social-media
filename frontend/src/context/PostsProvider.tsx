import React, {createContext, useContext, useEffect, useState} from 'react';
import {ITweet} from '../types';

interface PostsContextType {
    posts: ITweet[];
    setPosts: React.Dispatch<React.SetStateAction<ITweet[]>>;
}

const PostsContext = createContext<PostsContextType | undefined>(undefined);

export const usePosts = (): PostsContextType => {
    const context = useContext(PostsContext);
    if (!context) {
        throw new Error('usePosts must be used within a PostsProvider');
    }
    return context;
};

interface PostsProviderProps {
    children: React.ReactNode;
}

export const fetchPosts = async (): Promise<Array<ITweet>> => {
    try {
        const response = await fetch('http://127.0.0.1:5000/chain');  // FIXME
        if (!response.ok)
            throw new Error(`Failed to fetch posts: ${response.statusText}`);
        const posts: Array<ITweet> = await response.json();
        console.debug('Fetched posts:', posts);
        return posts.reverse();
    } catch (error) {
        console.error('Error fetching posts:', error);
        return [];
    }
};

export const PostsProvider = ({children}: PostsProviderProps) => {
    const [posts, setPosts] = useState<ITweet[]>([]);

    useEffect(() => {
        fetchPosts().then(posts => setPosts(posts));
    }, []);

    return (
        <PostsContext.Provider value={{posts, setPosts}}>
            {children}
        </PostsContext.Provider>
    );
};
