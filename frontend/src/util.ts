export const ALGORITHM = 'RSASSA-PKCS1-v1_5';

export function download(data: BlobPart, filename: string) {
    const blob = new Blob([data], {type: 'text/plain'});
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}

export async function readFileAsync(file: Blob): Promise<string | ArrayBuffer | null> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error);

        reader.readAsText(file);
    });
}

export async function calculatePublicKeyHash(fileInput: HTMLInputElement): Promise<{key: string, hash: string} | null> {
    try {
        if (fileInput.files == null) {
            console.error('No file was uploaded.');
            return null;
        }
        const publicKey = await readFileAsync(fileInput.files[0]);
        if (typeof publicKey !== 'string') {
            console.error(`Unexpected public key: ${publicKey}; expected type: <string>`);
            return null;
        }

        const publicKeyHash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(publicKey));
        return {
            key: publicKey,
            hash: Array.from(new Uint8Array(publicKeyHash)).map(b => b.toString(16).padStart(2, '0')).join('')
        };
    } catch (error) {
        console.error('Error calculating public key hash:', error);
        return null;
    }
}

/**
 * Generates a key pair (public and private keys) using the RSASSA-PKCS1-v1_5 algorithm.
 * The generated keys are exported in PEM format and saved as 'public_key.pem' and 'private_key.pem'.
 */
export const generateKeyPair = async () => {
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

export const findKeyByValue = <K, V>(map: Map<K, V>, searchValue: V): K | undefined => {
    const entry = Array.from(map.entries()).find(([_, value]) => value === searchValue);
    const res = entry ? entry[0] : undefined;
    console.log(res);
    return res;
};

