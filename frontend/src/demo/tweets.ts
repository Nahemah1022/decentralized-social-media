import {ITweet} from "../types";


export const DEMO_TWEETS: Array<ITweet> = [
    {
        id: 1,
        author: "John Doe",
        content: "# Just saw the most amazing sunrise today!\n #breathtaking\n",
        createdAt: '2023-01-01',
        avatarUrl: "/avatar/large/matthew.png"
    },
    {
        id: 2,
        author: "Jane Smith",
        content: "```\nExcited to start a new project at work tomorrow. Wish me luck!",
        createdAt: '2023-01-02',
        avatarUrl: "/avatar/large/molly.png"
    },
    {
        id: 3,
        author: "Alice Johnson",
        content: "Can anyone recommend a good book on UX design?",
        createdAt: '2023-01-03',
        avatarUrl: "/avatar/large/jenny.jpg"
    },
    {
        id: 4,
        author: "Bob Brown",
        content: "Just completed my first marathon and feeling great!",
        createdAt: '2023-01-04',
        avatarUrl: "/avatar/large/elliot.jpg"
    },
    {
        id: 5,
        author: "Charlie Green",
        content: "Exploring the city's hidden gems. #urbanexplorer",
        createdAt: '2023-01-05',
        avatarUrl: "/avatar/large/steve.jpg"
    }
];