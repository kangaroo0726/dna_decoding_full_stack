from .constants import (
    CODING,
    DNA_BASES,
    MRNA,
    MRNA_BASES,
    START_CODON,
    STOP_CODONS,
    TEMPLATE,
    COMPLEMENT_DICT,
    PROTEIN_DICT,
)

def five_three(is_five_to_three, strand):
    """Return the strand in the requested orientation."""
    if is_five_to_three:
        return strand
    return strand[::-1]


def convert(strand_type, strand):
    """Convert a DNA or mRNA strand into an mRNA sequence."""
    if strand_type == MRNA:
        for char in strand:
            if char not in MRNA_BASES:
                raise ValueError(f"Malformed Strand: {char} not valid")
        return strand
    elif strand_type == TEMPLATE:
        converted_strand = list(strand[::-1])
        for index, base in enumerate(converted_strand):
            try:
                converted_strand[index] = COMPLEMENT_DICT[base]
            except KeyError:
                raise ValueError(f"Malformed Strand: {base} not valid")
        return "".join(converted_strand)
    elif strand_type == CODING:
        for char in strand:
            if char not in DNA_BASES:
                raise ValueError(f"Malformed Strand: {char} not valid")
        return strand.replace("T", "U")
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
