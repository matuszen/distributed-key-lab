from dkglab.crypto.schnorr import generate_keypair, sign_message, verify_signature
from dkglab.protocols.threshold_signature import SchnorrSigner


def test_schnorr_sign_and_verify_roundtrip() -> None:
    keypair = generate_keypair()
    message = b"hello schnorr"

    signature = sign_message(keypair.private_key, message)

    assert verify_signature(keypair.public_key, message, signature)


def test_schnorr_verify_rejects_tampered_message() -> None:
    keypair = generate_keypair()
    message = b"original"
    signature = sign_message(keypair.private_key, message)

    assert not verify_signature(keypair.public_key, b"tampered", signature)


def test_schnorr_verify_rejects_wrong_public_key() -> None:
    keypair = generate_keypair()
    other_keypair = generate_keypair()
    message = b"test"
    signature = sign_message(keypair.private_key, message)

    assert not verify_signature(other_keypair.public_key, message, signature)


def test_schnorr_signer_interface_roundtrip() -> None:
    signer = SchnorrSigner.generate()
    message = b"interface"

    signature = signer.sign(message)

    assert SchnorrSigner.verify(signer.public_key, message, signature)
