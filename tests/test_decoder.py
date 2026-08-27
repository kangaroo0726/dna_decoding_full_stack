import pytest
from decoder.constants import CODING, MRNA, TEMPLATE
from decoder.decoder import convert, decode, extract_codons, five_three, translate

@pytest.mark.parametrize(
    "answer, strand, expected",
    [
        (False, "ATGC", "CGTA"),
        (False, "AUGCCU", "UCCGUA"),
        (False, "AAAA", "AAAA"),
        (True, "TTTT", "TTTT"),
        (False, "", ""),
        (True, "", ""),
        (False, "ATCGGTATGCCCCCCGTA", "ATGCCCCCCGTATGGCTA"),
        (True, "ATCGGTATGCCCCCCGTA", "ATCGGTATGCCCCCCGTA"),
        (True, "TTTAAATTTAAA", "TTTAAATTTAAA"),
        (True, "A", "A")
    ]
)

def test_five_three(answer, strand, expected):
    result = five_three(answer, strand)
    assert result == expected


@pytest.mark.parametrize(
    "strand_type, strand, expected",
    [
        (MRNA, "AUGCCU", "AUGCCU"),
        (MRNA, "", ""),
        (CODING, "ATGC", "AUGC"),
        (CODING, "", ""),
        (TEMPLATE, "TACG", "CGUA"),
        (TEMPLATE, "", ""),
    ]
)
def test_convert(strand_type, strand, expected):
    result = convert(strand_type, strand)
    assert result == expected


@pytest.mark.parametrize(
    "strand_type, strand",
    [
        (MRNA, "AUGT"),
        (CODING, "AUGC"),
        (TEMPLATE, "TAX"),
        ("invalid", "AUG"),
    ]
)
def test_convert_invalid_strand(strand_type, strand):
    with pytest.raises(ValueError):
        convert(strand_type, strand)


@pytest.mark.parametrize(
    "strand, expected",
    [
        ("", []),
        ("CCCAUGGCUUAA", ["AUG", "GCU", "UAA"]),
        ("AUGUAGGCU", ["AUG", "UAG"]),
        ("AUGGCUUGA", ["AUG", "GCU", "UGA"]),
        ("AUGGCU", ["AUG", "GCU"]),
        ("CCAUGG", ["AUG"]),
        ("AUGAUGUAA", ["AUG", "AUG", "UAA"]),
    ]
)
def test_extract_codons(strand, expected):
    result = extract_codons(strand)
    assert result == expected


@pytest.mark.parametrize(
    "strand",
    [
        ("CCCUUU"),
        ("CCCA"),
        ("AAA"),
    ]
)
def test_extract_codons_without_start(strand):
    result = extract_codons(strand)
    assert result == []


@pytest.mark.parametrize(
    "strand, expected",
    [
        (["AUG", "GCU", "UAA"], ["methionine", "alanine", "stop"]),
        (["AUG", "GCU"], ["methionine", "alanine", "..."]),
        (["UAA", "AUG"], ["stop"]),
    ]
)
def test_translate(strand, expected):
    result = translate(strand)
    assert result == expected


def test_translate_empty_strand():
    with pytest.raises(ValueError):
        translate([])


def test_translate_unknown_codon():
    with pytest.raises(ValueError):
        translate(["XXX"])


def test_translate_stops_before_later_invalid_codon():
    result = translate(["AUG", "UAA", "XXX"])
    assert result == ["methionine", "stop"]


@pytest.mark.parametrize(
    "strand, strand_type, five_to_three, expected_codons, expected_proteins",
    [
        (
            "CCCAUGGCUUAA",
            MRNA,
            True,
            "AUGGCUUAA",
            ["methionine", "alanine", "stop"],
        ),
        (
            "CCCATGGCTTAA",
            CODING,
            True,
            "AUGGCUUAA",
            ["methionine", "alanine", "stop"],
        ),
        (
            "TTAAGCCATGGG",
            TEMPLATE,
            True,
            "AUGGCUUAA",
            ["methionine", "alanine", "stop"],
        ),
        (
            "UCCGUA",
            MRNA,
            False,
            "AUGCCU",
            ["methionine", "proline", "..."],
        ),
        (
            "cccatggcttaa",
            CODING,
            True,
            "AUGGCUUAA",
            ["methionine", "alanine", "stop"],
        ),
    ]
)
def test_decode(strand, strand_type, five_to_three, expected_codons, expected_proteins):
    result = decode(strand, strand_type, five_to_three)
    assert result == (expected_codons, expected_proteins)


@pytest.mark.parametrize(
    "strand, strand_type",
    [
        ("CCCGGG", MRNA),
        ("CCCGGG", CODING),
        ("CCCGGG", TEMPLATE),
    ]
)
def test_decode_without_start_codon(strand, strand_type):
    with pytest.raises(ValueError, match="Methionine not found"):
        decode(strand, strand_type, True)


@pytest.mark.parametrize(
    "strand, strand_type",
    [
        ("AUGXCCU", MRNA),
        ("ATGXCC", CODING),
        ("TAX", TEMPLATE),
    ]
)
def test_decode_rejects_malformed_strand(strand, strand_type):
    with pytest.raises(ValueError, match="Malformed Strand"):
        decode(strand, strand_type, True)
