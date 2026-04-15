from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import INFINITY


def main() -> None:
    curve = SECP256k1
    generator = curve.generator
    order = curve.order

    print("Curve:", curve.name)
    print("Generator G.x:", hex(generator.x()))
    print("Generator G.y:", hex(generator.y()))
    print("Group order n:", hex(order))
    print("Sanity check n*G == INFINITY:", order * generator == INFINITY)


if __name__ == "__main__":
    main()
