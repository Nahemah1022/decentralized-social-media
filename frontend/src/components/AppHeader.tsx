import React, {useState} from 'react';
import {Menu, Button, Container, Popup, Message} from 'semantic-ui-react';
import {calculatePublicKeyHash, generateKeyPair} from "../util";
import '@shoelace-style/shoelace/dist/components/input/input';
import {usePublicKey} from "../context/PublicKeyProvider";

interface AppHeaderProps {
    onPageChange: (page: string) => void;
    activePage: string; // New prop to determine the active page
}


const LogInComponent: React.FC = () => {
    const { publicKeyHash, setPublicKeyHash } = usePublicKey();
    const [loggedIn, setLoggedIn] = useState<boolean>(false);

    const handleFileUpload = async (elem: HTMLInputElement) => {
        calculatePublicKeyHash(elem).then(hash => {
            if (hash) {
                setLoggedIn(true);
                setPublicKeyHash(hash);
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
                        content={loggedIn ? `Logged in as ${publicKeyHash}` : 'Upload your public key to sign in.'}>
                    </Message>
                    <input type='file' onChange={(e) => handleFileUpload(e.target)}></input>
                </>
            }
            on={['click']}
            position='bottom center'
            trigger={
                <Button
                    as='a'
                    inverted
                >
                    {loggedIn ? 'Update Public Key' : 'Sign In'}
                </Button>
            }
        />
    );
};

const RegisterComponent = () => {
    return (
        <Popup
            content={<Button onClick={generateKeyPair}>Generate Key Pair</Button>}
            on={'click'}
            position='bottom center'
            wide
            trigger={<Button as='a' inverted primary style={{marginLeft: '0.5em'}}>New User</Button>}
        />
    );
};


const AppHeader: React.FC<AppHeaderProps> = ({onPageChange, activePage}) => {
    return (
        <Menu inverted>
            <Container>
                <Menu.Item
                    as='a'
                    active={activePage === 'home'} // Only active if the current page is 'home'
                    onClick={() => onPageChange('home')}
                >
                    Home
                </Menu.Item>
                <Menu.Item
                    as='a'
                    active={activePage === 'about'} // Only active if the current page is 'about'
                    onClick={() => onPageChange('about')}
                >
                    About
                </Menu.Item>
                <Menu.Item position='right'>
                    <LogInComponent/>
                    <RegisterComponent/>
                </Menu.Item>
            </Container>
        </Menu>
    );
};

export default AppHeader;
