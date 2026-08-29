import re

from .constants import (
    CODING,
    DNA_BASES,
    MRNA,
    MRNA_BASES,
    START_CODON,
    STOP_CODONS,
    TEMPLATE,
    PROTEIN_DICT,
)

DNA_TO_MRNA_TABLE = str.maketrans({"T": "U"})
COMPLEMENT_TABLE = str.maketrans({"T": "A", "A": "U", "G": "C", "C": "G"})

MRNA_PATTERN = re.compile(r"[^AUGC]")
CODING_PATTERN = re.compile(r"[^ATCG]")
TEMPLATE_PATTERN = re.compile(r"[^ATCG]")


def five_three(is_five_to_three, strand):
    """Return the strand in the requested orientation."""
    if is_five_to_three:
        return strand
    return strand[::-1]


def find_invalid_base(strand, pattern):
    """Return the first invalid base in the strand, if one exists."""
    match = pattern.search(strand)
    if match is None:
        return None
    return match.group(0)


def convert(strand_type, strand):
    """Convert a DNA or mRNA strand into an mRNA sequence."""
    if strand_type == MRNA:
        invalid_base = find_invalid_base(strand, MRNA_PATTERN)
        if invalid_base is not None:
            raise ValueError(f"Malformed Strand: {invalid_base} not valid")
        return strand

    if strand_type == TEMPLATE:
        invalid_base = find_invalid_base(strand, TEMPLATE_PATTERN)
        if invalid_base is not None:
            raise ValueError(f"Malformed Strand: {invalid_base} not valid")
        return strand.translate(COMPLEMENT_TABLE)[::-1]

    if strand_type == CODING:
        invalid_base = find_invalid_base(strand, CODING_PATTERN)
        if invalid_base is not None:
            raise ValueError(f"Malformed Strand: {invalid_base} not valid")
        return strand.translate(DNA_TO_MRNA_TABLE)

    raise ValueError(f"Invalid strand type: {strand_type}")


def extract_codons(strand):
    """Extract codons from the first start codon through the next stop codon."""
    codons = []
    strand_index = 0
    while strand_index + 2 < len(strand):
        if strand[strand_index:strand_index + 3] == START_CODON:
            codons.append(START_CODON)
            strand_index += 3
            while strand_index + 2 < len(strand):
                codon = strand[strand_index:strand_index + 3]
                if codon not in STOP_CODONS:
                    codons.append(codon)
                    strand_index += 3
                else:
                    codons.append(codon)
                    break
            return codons
        else:
            strand_index += 1
    return codons


def translate(strand):
    """Translate extracted mRNA codons into protein names."""
    proteins = []
    if strand:
        for codon in strand:
            protein = PROTEIN_DICT.get(codon)
            if protein is None:
                raise ValueError(f"Malformed Strand: {codon} not valid")
            proteins.append(protein)
            if protein == "stop":
                break
        if proteins and proteins[-1] != "stop":
            proteins.append("...")
        return proteins
    else:
        raise ValueError("Error: Methionine not found")


def decode(strand, strand_type, five_to_three):
    """Convert, translate, and return a strand's codons and proteins."""
    strand = strand.upper()
    oriented_strand = five_three(five_to_three, strand)
    converted = convert(strand_type, oriented_strand)
    codons = extract_codons(converted)
    proteins = translate(codons)
    return "".join(codons), proteins
