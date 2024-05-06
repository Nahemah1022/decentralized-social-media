import React, {useState} from 'react';
import {Menu, Button, Container, Popup, Message} from 'semantic-ui-react';
import {calculatePublicKeyHash, generateKeyPair} from "../util";
import '@shoelace-style/shoelace/dist/components/input/input';
import {usePublicKey} from "../context/PublicKeyProvider";
import {fetchPosts, usePosts} from "../context/PostsProvider";

const LogInComponent: React.FC = () => {
    const {setPublicKey, publicKeyHash, setPublicKeyHash} = usePublicKey();
    const [loggedIn, setLoggedIn] = useState<boolean>(false);

    const handlePublicKeyUpload = async (elem: HTMLInputElement) => {
        calculatePublicKeyHash(elem).then(res => {
            if (res) {
                setLoggedIn(true);
                setPublicKey(res.key);
                setPublicKeyHash(res.hash);
            } else {
                console.error('Failed to log in.');
            }
        });
    }

    return (
        <Popup
            content={
                <>
                    <Message
                        content={loggedIn
                            ? `Logged in as\n${publicKeyHash}`
                            : 'Upload your public key to sign in.'}>
                    </Message>
                    <input type='file' onChange={(e) => handlePublicKeyUpload(e.target)}></input>
                </>
            }
            on={['click']}
            position='bottom center'
            trigger={
                <Button as='a' inverted style={{marginLeft: '0.5em'}}>
                    {loggedIn ? 'Update Public Key' : 'Sign In'}
                </Button>
            }
        />
    );
};

const RegisterComponent = () => {
    return (
        <Popup
            content={<Button onClick={generateKeyPair}>Generate New Key Pair</Button>}
            on={'click'}
            position='bottom center'
            wide
            trigger={<Button as='a' inverted primary>New User</Button>}
        />
    );
};


const AppHeader = () => {
    const {setPosts} = usePosts();
    return (
        <Menu inverted borderless className={'fixed'}>
            <Container style={{justifyContent: 'space-around'}}>
                <Menu.Item>
                    <RegisterComponent/>
                    <LogInComponent/>
                </Menu.Item>
                <Menu.Item as='a' onClick={() => fetchPosts().then(setPosts)}>
                    Refresh Posts
                </Menu.Item>
            </Container>
        </Menu>
    );
};

export default AppHeader;
