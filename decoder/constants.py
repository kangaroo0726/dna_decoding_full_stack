PROTEIN_DICT = {
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
    "GGA": "glycine", "GGU": "glycine", "GGC": "glycine", "GGG": "glycine", "AGU": "serine",
    "UAA": "stop", "UGA": "stop", "UAG": "stop"
}

START_CODON = "AUG"
STOP_CODONS = {"UGA", "UAG", "UAA"}

MRNA_BASES = {"A", "U", "C", "G"}
DNA_BASES = {"A", "T", "C", "G"}

COMPLEMENT_DICT = {"T": "A", "A": "U", "G": "C", "C": "G"}

MRNA = "mrna"
CODING = "coding"
TEMPLATE = "template"