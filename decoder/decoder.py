from .constants import PROTEIN_DICT as protein_dict, MRNA, CODING, TEMPLATE, COMPLEMENT_DICT as complement_dict, STOP_CODONS, MRNA_BASES, DNA_BASES, START_CODON

def five_three(answer, strand):
    if answer:
        return strand
    return strand[::-1]


def convert(type_strand, strand):
    if type_strand == MRNA:
        for char in strand:
            if char not in MRNA_BASES:
                raise ValueError(f"Malformed Strand: {char} not valid")
        return strand
    elif type_strand == TEMPLATE:
        new_strand = strand[::-1]
        new_strand = list(new_strand)
        for i in range(len(new_strand)):
            try:
                new_strand[i] = complement_dict[new_strand[i]]
            except KeyError:
                raise ValueError(f"Malformed Strand: {new_strand[i]} not valid")
        return ''.join(new_strand)
    elif type_strand == CODING:
        for char in strand:
            if char not in DNA_BASES:
                raise ValueError(f"Malformed Strand: {char} not valid")
        return strand.replace("T", "U")
    raise ValueError(f"Invalid strand type: {type_strand}")


def extract_codons(strand):
    first_strand_l = []
    i = 0
    while i + 2 < len(strand):
        if strand[i:i + 3] == START_CODON:
            first_strand_l.append(START_CODON)
            i += 3
            while i + 2 < len(strand):
                codon = strand[i:i + 3]
                if codon not in STOP_CODONS:
                    first_strand_l.append(codon)
                    i += 3
                else:
                    first_strand_l.append(codon)
                    break
            return first_strand_l
        else:
            i += 1
    return first_strand_l


def translate(strand):
    proteins = []
    if strand:
        for sequence in strand:
            protein = protein_dict[sequence]
            proteins.append(protein)
            if protein == "stop":
                break
        if proteins and proteins[-1] != "stop":
            proteins.append("...")
        return proteins
    else:
        raise ValueError("Error: Methionine not found")


def decode(strand, strand_type, five_to_three):
    strand = strand.upper()
    prime = five_three(five_to_three, strand)
    converted = convert(strand_type, prime)
    codons = extract_codons(converted)
    proteins = translate(codons)
    return "".join(codons), proteins
