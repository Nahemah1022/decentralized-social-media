// FIXME: Fix Attributes
export interface ITweet {
    id: number;
    author: string;
    publicKey: string;
    content: string;
    createdAt: string;
    avatarUrl: string;
}

export interface IPost {
    author: string;
    content: string;
}