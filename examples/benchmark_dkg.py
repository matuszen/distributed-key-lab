"""Small academic benchmark for local distributed key generation simulations."""

from time import perf_counter

from dkglab.protocols.dkg import run_dkg


def main() -> None:
    configs = [(3, 2), (5, 3), (7, 4), (10, 6)]

    print("Distributed key generation benchmark")
    print("n,t,time_ms")
    for num_participants, threshold in configs:
        start = perf_counter()
        run_dkg(num_participants=num_participants, threshold=threshold)
        elapsed_ms = (perf_counter() - start) * 1000
        print(f"{num_participants},{threshold},{elapsed_ms:.3f}")


if __name__ == "__main__":
    main()
