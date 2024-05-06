import React, {createContext, useContext, useState} from 'react';

interface User {
    username: string;
    avatarPath: string;
}

interface UserContextType {
    usersMap: Map<string, User>;
    addUser: (publicKey: string) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const useUser = (): UserContextType => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
};

interface UserProviderProps {
    children: React.ReactNode;
}

export const UserProvider = ({children}: UserProviderProps) => {
    const [usersMap, setUsersMap] = useState<Map<string, User>>(new Map());

    const generateRandomUsername = (): string => {
        const firstNames = ['Alan', 'Grace', 'John', 'Donald', 'Edsger', 'Linus', 'James', 'Guido', 'Bjarne', 'Ken'];
        const lastNames = ['Turing', 'Hopper', 'von Neumann', 'Knuth', 'Dijkstra', 'Torvalds', 'Gosling', 'van Rossum', 'Stroustrup', 'Thompson'];

        const randomFirstName = firstNames[Math.floor(Math.random() * firstNames.length)];
        const randomLastName = lastNames[Math.floor(Math.random() * lastNames.length)];

        return `${randomFirstName} ${randomLastName}`;
    };


    const getRandomAvatarPath = (): string => {
        const names = ['ade.jpg', 'chris.jpg', 'christian.jpg', 'daniel.jpg', 'elliot.jpg', 'helen.jpg', 'jenny.jpg', 'joe.jpg', 'justen.jpg', 'laura.jpg'];
        const randomIndex = Math.floor(Math.random() * names.length);
        const name = names[randomIndex];
        return `/avatar/small/${name}`;
    };

    const addUser = (publicKey: string): void => {
        const username = generateRandomUsername();
        const avatarPath = getRandomAvatarPath();
        setUsersMap((prevUsersMap) => new Map(prevUsersMap.set(publicKey, {username, avatarPath})));
    };

    return (
        <>
            <UserContext.Provider value={{usersMap, addUser}}>
                {children}
            </UserContext.Provider>
        </>
    );
};
