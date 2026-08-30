import csv
import random
import time
from decoder.constants import MRNA, PROTEIN_DICT, STOP_CODONS
from decoder.decoder import decode


def generate_valid_mrna_strand(length):
    if length <= 3:
        return "AUG"

    valid_codons = [codon for codon, protein in PROTEIN_DICT.items() if protein != "stop"]
    codons = ["AUG"]
    remaining_length = max(1, (length // 3) - 1)
    codons.extend(random.choice(valid_codons) for _ in range(remaining_length))
    codons.append(random.choice(list(STOP_CODONS)))

    strand = "".join(codons)
    if len(strand) > length:
        strand = strand[:length]
    if len(strand) % 3 != 0:
        strand = strand[: len(strand) - (len(strand) % 3)]
    if not strand.endswith(tuple(STOP_CODONS)):
        strand = strand[:-3] + random.choice(list(STOP_CODONS))
    return strand


NUM_REPEATED_SMALL_STRANDS = 100_000
NUM_REPEATED_BIG_STRANDS = 1_000
BENCHMARK_SIZES = {
    "Small": (12, NUM_REPEATED_SMALL_STRANDS),
    "Medium": (30, NUM_REPEATED_SMALL_STRANDS),
    "Large": (90, NUM_REPEATED_SMALL_STRANDS),
    "~100K": (100_000, NUM_REPEATED_BIG_STRANDS),
    "~1M": (1_000_000, NUM_REPEATED_BIG_STRANDS),
}


def measure_time_decode(strand, strand_type, five_to_three, repetitions):
    start = time.perf_counter()
    for _ in range(repetitions):
        decode(strand=strand, strand_type=strand_type, five_to_three=five_to_three)
    elapsed = time.perf_counter() - start
    bases_processed = len(strand) * repetitions
    bases_per_second = bases_processed / elapsed
    return elapsed, bases_per_second


def build_benchmark_cases():
    random.seed(12)
    cases = []
    for name, (length, repetitions) in BENCHMARK_SIZES.items():
        strand = generate_valid_mrna_strand(length)
        cases.append((name, strand, MRNA, True, repetitions))
    return cases


def main():
    tests = build_benchmark_cases()

    header = ["size", "bases", "repetitions", "time_seconds", "bases_per_second"]
    with open("tests/benchmark_run.csv", mode="w", newline="", encoding="utf-8") as file_out:
        writer_out = csv.writer(file_out)
        writer_out.writerow(header)
        for name, strand, strand_type, five_to_three, repetitions in tests:
            elapsed, bases_per_second = measure_time_decode(
                strand=strand,
                strand_type=strand_type,
                five_to_three=five_to_three,
                repetitions=repetitions,
            )
            writer_out.writerow([name, len(strand), repetitions, elapsed, bases_per_second])
            print(
                f"{name}: | "
                f"{len(strand)} bases | "
                f"{elapsed:.4f}s | "
                f"{bases_per_second:,.0f} bases/sec | "
                f"Measured over {repetitions} function calls"
            )


if __name__ == "__main__":
    main()
