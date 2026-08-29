import time
import csv
from pathlib import Path
from decoder.decoder import decode
from decoder.constants import MRNA, TEMPLATE, CODING

def read_strand(filename):
    with open(filename) as file_in:
        strand = file_in.readline().strip()
    return strand


file_path_100k = Path(__file__).with_name("dna_template_100k.txt")
file_path_1m = Path(__file__).with_name("dna_template_1m.txt")

SMALL_STRAND = ["AUGGCACUGGUC", MRNA, True]
MEDIUM_STRAND = ["CCGAUGGCUCCUGAACGUAUCGGAAAUUAA", MRNA, True]
LARGE_STRAND = ["CCGAUGGCUCCUGAACGUAUCGGAAAUACCGUUGCUAAGGCUACGAUCGGCUAUCGAACCGGUUAACGCUAAGCUCGGAUCCGAUCGAAUAA", MRNA, True]
STRAND_100K = [read_strand(file_path_100k), CODING, True]
STRAND_1M = [read_strand(file_path_1m), TEMPLATE, False]
TESTS = [SMALL_STRAND, MEDIUM_STRAND, LARGE_STRAND, STRAND_100K, STRAND_1M]
NUM_REPEATED_SMALL_STRANDS = 10000
NUM_REPEATED_BIG_STRANDS = 100


def measure_time_decode(strand, repetitions):
    sequence = strand[0]
    start = time.perf_counter()
    for _ in range(repetitions):
        decode(strand=strand[0], strand_type=strand[1], five_to_three=strand[2])
    elapsed = time.perf_counter() - start
    bases_processed = len(sequence) * repetitions
    bases_per_second = bases_processed / elapsed
    return elapsed, bases_per_second


def main():
    print("Running decoder benchmark...")
    tests = [
        ("Small", SMALL_STRAND, NUM_REPEATED_SMALL_STRANDS),
        ("Medium", MEDIUM_STRAND, NUM_REPEATED_SMALL_STRANDS),
        ("Large", LARGE_STRAND, NUM_REPEATED_SMALL_STRANDS),
        ("~100K", STRAND_100K, NUM_REPEATED_BIG_STRANDS),
        ("~1M", STRAND_1M, NUM_REPEATED_BIG_STRANDS),
    ]
    header = ["size", "bases", "repetitions", "time_seconds", "bases_per_second"]
    with open("tests/benchmark_run.csv", mode="w", newline="", encoding="utf-8") as file_out:
        writer_out = csv.writer(file_out)
        writer_out.writerow(header)
        for name, strand, repetitions in tests:
            elapsed, bases_per_second = measure_time_decode(strand, repetitions)
            writer_out.writerow([name, len(strand[0]), repetitions, elapsed, bases_per_second])
            print(
                    f"{name}: | "
                    f"{len(strand[0])} bases | "
                    f"{elapsed:.4f}s | "
                    f"{bases_per_second:,.0f} bases/sec | "
                    f"Measured over {repetitions} function calls"
                )

if __name__ == "__main__":
    main()
