import React, {useState} from 'react';
import {Button, Form, Message, Popup, TextArea} from 'semantic-ui-react';
import {ALGORITHM, readFileAsync} from "../util";
import {usePublicKey} from "../context/PublicKeyProvider";
import {usePosts} from "../context/PostsProvider";


const TweetForm = () => {
    const [content, setContent] = useState('');
    const {publicKey} = usePublicKey();
    const {fetchPosts} = usePosts();

    /**
     * Process a private key file.
     * @param file The private key file to process.
     * @returns A Promise that resolves to the imported private key or null if processing fails.
     */
    const processPrivateKey = async (file: File): Promise<CryptoKey | null> => {
        const pemPrivate = await readFileAsync(file);
        if (typeof pemPrivate !== 'string')
            return null;

        const privateKeyData = pemPrivate.split('\n').slice(1, -1).join('');
        const binaryDerPrivate = atob(privateKeyData);
        const arrayPrivate = new Uint8Array(binaryDerPrivate.length);
        for (let i = 0; i < binaryDerPrivate.length; i++)
            arrayPrivate[i] = binaryDerPrivate.charCodeAt(i);

        try {
            return await window.crypto.subtle.importKey(
                'pkcs8', arrayPrivate.buffer, {name: ALGORITHM, hash: {name: 'SHA-256'}}, true, ['sign']);
        } catch (error) {
            console.error('Error importing private key:', error);
            return null;
        }
    };

    const submitPost = async (fileInput: HTMLInputElement) => {
        try {
            if (fileInput.files == null) {
                console.error('No file was uploaded.');
                return null;
            }

            const privateKey = await processPrivateKey(fileInput.files[0]);
            if (privateKey == null) {
                console.error(`Private key should not be null: ${privateKey}`);
                return null;
            }

            const signature = await window.crypto.subtle.sign(
                ALGORITHM, privateKey, new TextEncoder().encode(content));

            // FIXME: Hardcoded link
            fetch('http://127.0.0.1:5000/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    post_content: content,
                    public_key: publicKey,
                    signature: btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(signature))))
                }),
                // credentials: 'include'  // Include credentials for cookies, authorization headers or TLS client certificates
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Response:', data);
                    fetchPosts();
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } catch (error) {
            console.error('Error calculating public key hash:', error);
            return null;
        }
    }

    return (
        <Form className="tweet-form">
            <TextArea
                placeholder='What is happening?!'
                value={content}
                onChange={(_, data: any) => setContent(data.value)}
                style={{minHeight: 100}}
            />
            <div className="form-button">
                <Popup
                    wide
                    on={'click'}
                    trigger={
                        <Button type='submit' primary compact size='small'>
                            Sign & Post
                        </Button>
                    }
                    content={
                        <>
                            <Message content={'Upload your private key to sign the post.'}/>
                            <input type='file' onChange={(e) => submitPost(e.target)}></input>
                        </>
                    }
                >
                </Popup>
            </div>
        </Form>
    );
};

export default TweetForm;
