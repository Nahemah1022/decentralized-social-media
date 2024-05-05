import React, {useState} from 'react';
import {Menu, Button, Container, Popup, Message} from 'semantic-ui-react';
import {calculatePublicKeyHash, download} from "../util";

interface AppHeaderProps {
    onPageChange: (page: string) => void;
    activePage: string; // New prop to determine the active page
}

const LogInComponent = () => {
    const [loggedIn, setLoggedIn] = useState(false);
    const [publicKeyHash, setPublicKeyHash] = useState('');
    const [waysToTrigger, setWaysToTrigger] = useState(['click']);

    const handleFileUpload = async (elem: HTMLInputElement) => {
        calculatePublicKeyHash(elem).then(hash => {
            if (hash) {
                setLoggedIn(true);
                setPublicKeyHash(hash);
            } else {
                console.error('Failed to log in.');
            }
        })
    }

    return (
        <Popup
            content={
                <>
                    <Message
                        content={loggedIn ? `Logged in as ${publicKeyHash}` : 'Upload your public key to log in.'}
                    >
                    </Message>
                    <input type='file' onChange={(e) => handleFileUpload(e.target)}/>
                </>}
            on={['click']}
            position='bottom center'
            trigger={
                <Button
                    as='a'
                    inverted
                >
                    {loggedIn ? 'Update Public Key' : 'Set Public Key'}
                </Button>
            }
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
                    <LogInComponent></LogInComponent>
                    <Popup
                        content='Generate a private-public key pair.'
                        position='bottom center'
                        trigger={
                            <Button
                                as='a'
                                inverted
                                primary
                                style={{marginLeft: '0.5em'}}
                                onClick={generateButtonClick}
                            >
                                Generate Key Pair
                            </Button>
                        }
                    />
                </Menu.Item>

            </Container>
        </Menu>
    );
};

/**
 * Generates a key pair (public and private keys) using the RSASSA-PKCS1-v1_5 algorithm.
 * The generated keys are exported in PEM format and saved as 'public_key.pem' and 'private_key.pem'.
 */
const generateButtonClick = async () => {
    try {
        // Generate Key Pair
        const keyPair = await window.crypto.subtle.generateKey(
            {
                name: "RSASSA-PKCS1-v1_5",
                modulusLength: 2048,
                publicExponent: new Uint8Array([1, 0, 1]),
                hash: {name: "SHA-256"},
            },
            true,
            ["sign", "verify"]
        );
        const privateKey = keyPair.privateKey;
        const publicKey = keyPair.publicKey;

        // Export and save the public key
        const exportedPublicKey = await window.crypto.subtle.exportKey("spki", publicKey);
        const pemExportedPublicKey =
            "-----BEGIN PUBLIC KEY-----\n" +
            btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(exportedPublicKey)))) + "\n" +
            "-----END PUBLIC KEY-----";
        download(pemExportedPublicKey, 'public_key.pem');

        // Export and save the private key
        const exportedPrivateKey = await window.crypto.subtle.exportKey("pkcs8", privateKey);
        const pemExportedPrivateKey =
            "-----BEGIN PRIVATE KEY-----\n" +
            btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(exportedPrivateKey)))) + "\n" +
            "-----END PRIVATE KEY-----";
        download(pemExportedPrivateKey, 'private_key.pem');
    } catch (error) {
        console.error("Error generating key pair:", error);
    }
};


export default AppHeader;
