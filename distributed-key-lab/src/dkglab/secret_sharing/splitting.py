import secrets
from typing import List
from dkglab.crypto.curves import GROUP_ORDER
from dkglab.utils.types import Share

def create_shares(secret: int, threshold: int, num_participants: int, modulus: int = GROUP_ORDER) -> List[Share]:
    if threshold > num_participants:
        raise ValueError("Threshold cannot be greater than number of participants.")

    # 1. Generujemy losowe wspó³czynniki wielomianu: a_1, a_2, ..., a_{t-1}
    # Wyraz wolny a_0 to nasz sekret.
    coefficients = [secret] + [secrets.randbelow(modulus) for _ in range(threshold - 1)]

    shares = []
    for x in range(1, num_participants + 1):
        # 2. Obliczamy y = P(x) u¿ywaj¹c schematu Hornera (najszybszy sposób)
        y = 0
        for coeff in reversed(coefficients):
            y = (y * x + coeff) % modulus
        shares.append(Share(x=x, y=y))
    
    return shares