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

export async function calculatePublicKeyHash(fileInput: HTMLInputElement): Promise<string | null> {
    try {
        if (fileInput.files == null) {
            console.error('No file was uploaded.');
            return null;
        }
        const publicKey = await readFileAsync(fileInput.files[0]);
        if (typeof publicKey !== 'string') {
            console.error(`Unexpected public key: ${publicKey}; expected: <string>`);
            return null;
        }

        const encoder = new TextEncoder();
        const publicKeyHash = await crypto.subtle.digest('SHA-256', encoder.encode(publicKey));
        return Array.from(new Uint8Array(publicKeyHash)).map(b => b.toString(16).padStart(2, '0')).join('');
    } catch (error) {
        console.error('Error calculating public key hash:', error);
        return null;
    }
}
