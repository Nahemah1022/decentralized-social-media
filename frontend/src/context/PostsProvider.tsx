import React, { createContext, useContext, useEffect, useState } from 'react';
import { ITweet } from '../types';

interface PostsContextType {
    posts: ITweet[];
    setPosts: React.Dispatch<React.SetStateAction<ITweet[]>>;
    fetchPosts: () => Promise<void>;
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

export const PostsProvider = ({ children }: PostsProviderProps) => {
    const [posts, setPosts] = useState<ITweet[]>([]);

    const fetchPosts = async (): Promise<void> => {
        try {
            const response = await fetch('http://localhost:8080/chain');  // FIXME
            if (!response.ok) {
                // noinspection ExceptionCaughtLocallyJS
                throw new Error(`Failed to fetch posts: ${response.statusText}`);
            }
            const fetchedPosts = await response.json();
            setPosts(fetchedPosts);
            console.log('Fetched posts:', fetchedPosts);
        } catch (error) {
            console.error('Error fetching posts:', error);
        }
    };

    useEffect(() => {
        fetchPosts().then(_ => console.log('Finished fetching posts.'));
    }, []);

    return (
        <PostsContext.Provider value={{ posts, setPosts, fetchPosts }}>
            {children}
        </PostsContext.Provider>
    );
};
