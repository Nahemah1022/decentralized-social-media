import React, { useState, FormEvent } from 'react';
import { Form, TextArea, Button } from 'semantic-ui-react';
import { ITweet } from '../types';

interface TweetFormProps {
    addTweet: (tweet: ITweet) => void;
}

const TweetForm: React.FC<TweetFormProps> = ({ addTweet }) => {
    const [content, setContent] = useState('');

    const handleSubmit = (event: FormEvent) => {
        event.preventDefault();
        if (content.trim()) {
            const newTweet: ITweet = {
                id: Date.now(),
                username: 'User', // Typically this would be pulled from user context
                avatarUrl: '/avatar/small/joe.jpg',
                content: content,
                createdAt: new Date().toISOString()
            };
            addTweet(newTweet);
            setContent('');
        }
    };

    return (
        <Form className="tweet-form" onSubmit={handleSubmit}>
            <TextArea
                placeholder='What is happening?!'
                value={content}
                onChange={(e, data: any) => setContent(data.value)}
                style={{ minHeight: 100 }}
            />
            <div className="form-button">
                <Button type='submit' primary compact size='small'>
                    Post
                </Button>
            </div>
        </Form>
    );
};

export default TweetForm;
