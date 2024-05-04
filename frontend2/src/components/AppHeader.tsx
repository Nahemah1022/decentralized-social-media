import React from 'react';
import { Menu, Button, Container } from 'semantic-ui-react';

interface AppHeaderProps {
    onPageChange: (page: string) => void;
    activePage: string; // New prop to determine the active page
}

const AppHeader: React.FC<AppHeaderProps> = ({ onPageChange, activePage }) => {
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
                    <Button as='a' inverted>Log in</Button>
                    <Button as='a' inverted primary style={{ marginLeft: '0.5em' }}>
                        Sign up
                    </Button>
                </Menu.Item>
            </Container>
        </Menu>
    );
};

export default AppHeader;
