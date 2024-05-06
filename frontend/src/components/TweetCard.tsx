import React, {useState} from 'react';
import {Card, Icon, Image, Popup} from 'semantic-ui-react';
import {ITweet} from '../types';
import ReactMarkdown from 'react-markdown'
import {useUser} from "../context/UserProvider";
import {findKeyByValue} from "../util";

interface TweetCardProps {
    tweet: ITweet;
}

const TweetCard: React.FC<TweetCardProps> = ({tweet}) => {
    const {usersMap} = useUser();
    const [upvotes, setUpvotes] = useState(0);
    const [hasUpvoted, setHasUpvoted] = useState(false);
    const [isBookmarked, setIsBookmarked] = useState(false); // State to track bookmark status

    const handleUpvote = () => {
        if (!hasUpvoted) {
            setUpvotes(upvotes + 1);
            setHasUpvoted(true);
        } else {
            setUpvotes(upvotes - 1);
            setHasUpvoted(false);
        }
    };

    const toggleBookmark = () => {
        setIsBookmarked(!isBookmarked); // Toggle the bookmark status
    };

    return (
        <Card className="tweet-card">
            <Card.Content>
                <Image
                    floated='left'
                    size='medium'
                    src={tweet.avatarUrl}
                    avatar
                />
                <Popup
                    content={tweet.publicKey}
                    trigger={<Card.Header>{tweet.author}</Card.Header>}>
                </Popup>
                <Card.Meta>{new Date(tweet.createdAt).toLocaleDateString()}</Card.Meta>
                <ReactMarkdown className={'markdown-content'}>
                    {tweet.content}
                </ReactMarkdown>
            </Card.Content>
            <Card.Content extra>
                <Icon
                    name='heart'
                    onClick={handleUpvote}
                    className={`upvote-icon ${hasUpvoted ? 'upvoted' : ''}`}
                    color={hasUpvoted ? 'red' : undefined}
                />
                <span style={{marginLeft: '5px'}}>{upvotes} Upvotes</span>
                <Icon
                    name='bookmark'  // Changed to filled bookmark icon
                    onClick={toggleBookmark}
                    className={`bookmark-icon ${isBookmarked ? 'bookmarked' : ''}`}
                    color={isBookmarked ? 'blue' : undefined}
                    style={{float: 'right'}}  // Move the bookmark icon to the right
                />
            </Card.Content>
        </Card>
    );
};

export default TweetCard;
