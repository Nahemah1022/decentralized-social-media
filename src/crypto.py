import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

SIGNATURE_LEN = 256
RSA_KEY_SIZE = 2048

def generate_rsa_key_pair(private_key_file='private_key.pem', public_key_file='public_key.pem', key_size=RSA_KEY_SIZE):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    with open(private_key_file, "wb") as key_file:
        key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    public_key = private_key.public_key()

    with open(public_key_file, "wb") as key_file:
        key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    return private_key, public_key

def sign_data(data, private_key_file):
    with open(private_key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

def verify_signature(data, signature, public_key):
    # print(public_key)
    if isinstance(public_key, str) and os.path.exists(public_key):
        with open(public_key, 'rb') as key_file:
            public_key_bytes = key_file.read()
    elif isinstance(public_key, bytes):
        public_key_bytes = public_key
    else:
        raise ValueError("public_key must be either a file path or bytes")

    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

if __name__ == '__main__':
    generate_rsa_key_pair("private_key.pem", "public_key.pem")
    data = b"Important message"
    signature = sign_data(data, "private_key.pem")
    is_valid = verify_signature(data, signature, "public_key.pem")
    print("Is the signature valid?", is_valid)
