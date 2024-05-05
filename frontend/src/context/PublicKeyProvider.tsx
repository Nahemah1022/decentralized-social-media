import React, { createContext, useContext, useState, ReactNode } from 'react';

interface PublicKeyContextType {
    publicKeyHash: string;
    setPublicKeyHash: React.Dispatch<React.SetStateAction<string>>;
}

const PublicKeyContext = createContext<PublicKeyContextType | undefined>(undefined);

export const usePublicKey = (): PublicKeyContextType => {
    const context = useContext(PublicKeyContext);
    if (!context) {
        throw new Error('usePublicKey must be used within a PublicKeyProvider');
    }
    return context;
};

interface PublicKeyProviderProps {
    children: ReactNode;
}

export const PublicKeyProvider = ({ children }: PublicKeyProviderProps) => {
    const [publicKeyHash, setPublicKeyHash] = useState<string>('');

    return (
        <PublicKeyContext.Provider value={{ publicKeyHash, setPublicKeyHash }}>
            {children}
        </PublicKeyContext.Provider>
    );
};
