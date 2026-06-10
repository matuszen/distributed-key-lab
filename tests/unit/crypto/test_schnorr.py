from dkglab.crypto.curves import GENERATOR, GROUP_ORDER
from dkglab.crypto.schnorr import (
    compute_challenge,
    generate_keypair,
    point_to_hex,
    scalar_to_hex,
    sign_message,
    verify_signature,
)
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


def test_compute_challenge_is_stable_and_message_bound() -> None:
    keypair = generate_keypair()
    R = 7 * GENERATOR
    message = b"challenge"

    first = compute_challenge(R, keypair.public_key, message)
    second = compute_challenge(R, keypair.public_key, message)
    changed = compute_challenge(R, keypair.public_key, b"other")

    assert first == second
    assert first != changed
    assert 0 <= first < GROUP_ORDER


def test_point_and_scalar_hex_are_fixed_width() -> None:
    keypair = generate_keypair()

    public_key_hex = point_to_hex(keypair.public_key)
    scalar_hex = scalar_to_hex(keypair.private_key)

    assert public_key_hex.startswith("04")
    assert len(public_key_hex) == 130
    assert len(scalar_hex) == 64
