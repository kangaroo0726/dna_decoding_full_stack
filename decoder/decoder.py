import create_random_strands as generator
from random import choice

protein_dict = {
    "AUG": "methionine",
    "UUU": "phenylalanine", "UUC": "phenylalanine",
    "UUA": "leucine", "UUG": "leucine", "CUA": "leucine", "CUU": "leucine", "CUC": "leucine", "CUG": "leucine",
    "AUA": "isoleucine", "AUU": "isoleucine", "AUC": "isoleucine",
    "GUA": "valine", "GUU": "valine", "GUC": "valine", "GUG": "valine",
    "UCA": "serine", "UCU": "serine", "UCC": "serine", "UCG": "serine", "AGC": "serine",
    "CCA": "proline", "CCU": "proline", "CCC": "proline", "CCG": "proline",
    "ACA": "threonine", "ACU": "threonine", "ACC": "threonine", "ACG": "threonine",
    "GCA": "alanine", "GCU": "alanine", "GCC": "alanine", "GCG": "alanine",
    "UAU": "tyrosine", "UAC": "tyrosine",
    "CAU": "histidine", "CAC": "histidine",
    "CAA": "glutamine", "CAG": "glutamine",
    "AAU": "asparagine", "AAC": "asparagine",
    "AAA": "lysine", "AAG": "lysine",
    "GAU": "aspartate", "GAC": "aspartate",
    "GAA": "glutamate", "GAG": "glutamate",
    "UGU": "cysteine", "UGC": "cysteine",
    "UGG": "tryptophan",
    "AGA": "arginine", "AGG": "arginine", "CGA": "arginine", "CGU": "arginine", "CGC": "arginine", "CGG": "arginine",
    "GGA": "glycine", "GGU": "glycine", "GGC": "glycine", "GGG": "glycine",
    "UAA": "stop", "UGA": "stop", "UAG": "stop"
}

def five_three(answer, strand):
    if answer == "Y":
        return strand
    elif answer == "N":
        new_strand = strand[::-1]
        return new_strand
    return None


def convert(type_strand, strand):
    if type_strand == "m":
        for char in strand:
            if char not in ["A", "U", "C", "G"]:
                raise ValueError(f"Malformed Strand: {char} not valid")
        return strand
    elif type_strand == "t":
        new_strand = strand[::-1]
        new_strand = list(new_strand)
        complement_dict = {"T": "A", "A": "U", "G": "C", "C": "G"}
        for i in range(len(new_strand)):
            try:
                new_strand[i] = complement_dict[new_strand[i]]
            except KeyError:
                raise ValueError(f"Malformed Strand: {new_strand[i]} not valid")
        new_strand = ''.join(new_strand)
        return new_strand
    elif type_strand == "c":
        new_strand_l = []
        for char in strand:
            if char in ["A", "C", "G", "T"]:
                new_strand_l.append(char)
            else:
                raise ValueError(f"Malformed Strand: {char} not valid")
        for i in range(len(new_strand_l)):
            if new_strand_l[i] == "T":
                new_strand_l[i] = "U"
        new_strand_s = ''.join(new_strand_l)
        return new_strand_s
    return None


def split(strand):
    first_strand_l = []
    i = 0
    while i + 2 < len(strand):
        if strand[i] == "A" and strand[i + 1] == "U" and strand[i + 2] == "G":
            first_strand_l.append("AUG")
            i += 3
            while i + 2 < len(strand):
                codon = strand[i:i + 3]
                if codon not in ["UGA", "UAA", "UAG"]:
                    first_strand_l.append(codon)
                    i += 3
                else:
                    first_strand_l.append(codon)
                    break
            return first_strand_l
        else:
            i += 1
    return first_strand_l


def form_proteins(strand):
    proteins = []
    if len(strand) != 0:
        for sequence in strand:
            protein = protein_dict.get(sequence)
            if protein:
                proteins.append(protein)
                if protein == "stop":
                    break
        if "stop" not in proteins:
            proteins.append("...")
        return proteins
    else:
        raise ValueError("Error: Methionine not found")


def main():
    generator.main()
    with open("tests/example_text.txt") as file_in:
        for line in file_in:
            try:
                line = line.strip()
                line = line.replace(" ", "")
                line = line.split(",")
                joined_strand = line[1]
                strand_type = line[0]
                five_to_three = choice(["Y", "N"])
                prime = five_three(five_to_three, joined_strand)
                converted = convert(strand_type, prime)
                print(f"\nFor the code:\n{joined_strand}\nYour mRNA strand is:\n{converted}\n")
                outcome = split(converted)
                protein = form_proteins(outcome)
                print("Your proteins are:\n")
                [print(f"{p}") for p in protein]
                print("\n")
            except ValueError as error:
                print(f"{error}\n")


if __name__ == "main":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
