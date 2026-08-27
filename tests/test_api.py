import pytest
from fastapi.testclient import TestClient
from api.main import app
from .constants import ENDPOINT, STATUS_CODE_BAD_REQUEST, STATUS_CODE_OK, STATUS_CODE_UNPROCESSABLE_CONTENT

client = TestClient(app)

@pytest.mark.parametrize(
    "request_data, expected_status, expected_response",
    [
        (
            {
                "strand": "CCCAUGGCUUAA",
                "strand_type": "mrna",
                "five_to_three": True,
            },
            STATUS_CODE_OK,
            {
                "converted": "AUGGCUUAA",
                "proteins": ["methionine", "alanine", "stop"],
            },
        ),
        (
            {
                "strand": "CCCATGGCTTAA",
                "strand_type": "coding",
                "five_to_three": True,
            },
            STATUS_CODE_OK,
            {
                "converted": "AUGGCUUAA",
                "proteins": ["methionine", "alanine", "stop"],
            },
        ),
        (
            {
                "strand": "TTAAGCCATGGG",
                "strand_type": "template",
                "five_to_three": True,
            },
            STATUS_CODE_OK,
            {
                "converted": "AUGGCUUAA",
                "proteins": ["methionine", "alanine", "stop"],
            },
        ),
        (
            {
                "strand": "UCCGUA",
                "strand_type": "mrna",
                "five_to_three": False,
            },
            STATUS_CODE_OK,
            {
                "converted": "AUGCCU",
                "proteins": ["methionine", "proline", "..."],
            },
        ),
        (
            {
                "strand": "cccatggcttaa",
                "strand_type": "coding",
                "five_to_three": True,
            },
            STATUS_CODE_OK,
            {
                "converted": "AUGGCUUAA",
                "proteins": ["methionine", "alanine", "stop"],
            },
        ),
        (
            {
                "strand": "CCCGGG",
                "strand_type": "mrna",
                "five_to_three": True,
            },
            STATUS_CODE_BAD_REQUEST,
            {"detail": "Error: Methionine not found"},
        ),
        (
            {
                "strand": "AUGXCCU",
                "strand_type": "mrna",
                "five_to_three": True,
            },
            STATUS_CODE_BAD_REQUEST,
            {"detail": "Malformed Strand: X not valid"},
        ),
        (
            {
                "strand": "ATGXCC",
                "strand_type": "coding",
                "five_to_three": True,
            },
            STATUS_CODE_BAD_REQUEST,
            {"detail": "Malformed Strand: X not valid"},
        ),
        (
            {
                "strand": "TAX",
                "strand_type": "template",
                "five_to_three": True,
            },
            STATUS_CODE_BAD_REQUEST,
            {"detail": "Malformed Strand: X not valid"},
        ),
        (
            {
                "strand": "AUG",
                "strand_type": "unknown",
                "five_to_three": True,
            },
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "literal_error",
                        "loc": ["body", "strand_type"],
                        "msg": "Input should be 'mrna', 'coding' or 'template'",
                        "input": "unknown",
                        "ctx": {"expected": "'mrna', 'coding' or 'template'"},
                    }
                ]
            },
        ),
        (
            {
                "strand": "",
                "strand_type": "mrna",
                "five_to_three": True,
            },
            STATUS_CODE_BAD_REQUEST,
            {"detail": "Error: Methionine not found"},
        ),
        (
            {
                "strand": "AUGUAA",
                "strand_type": "mrna",
                "five_to_three": True,
                "extra": "ignored",
            },
            STATUS_CODE_OK,
            {
                "converted": "AUGUAA",
                "proteins": ["methionine", "stop"],
            },
        ),
        (
            {"strand_type": "mrna", "five_to_three": True},
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "strand"],
                        "msg": "Field required",
                        "input": {"strand_type": "mrna", "five_to_three": True},
                    }
                ]
            },
        ),
        (
            {
                "strand": "AUG",
                "strand_type": "mrna",
                "five_to_three": "not-a-bool",
            },
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "bool_parsing",
                        "loc": ["body", "five_to_three"],
                        "msg": "Input should be a valid boolean, unable to interpret input",
                        "input": "not-a-bool",
                    }
                ]
            },
        ),
        (
            {"strand": "AUG", "five_to_three": True},
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "strand_type"],
                        "msg": "Field required",
                        "input": {"strand": "AUG", "five_to_three": True},
                    }
                ]
            },
        ),
        (
            {"strand": "AUG", "strand_type": "mrna"},
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "five_to_three"],
                        "msg": "Field required",
                        "input": {"strand": "AUG", "strand_type": "mrna"},
                    }
                ]
            },
        ),
        (
            {},
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "strand"],
                        "msg": "Field required",
                        "input": {},
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "strand_type"],
                        "msg": "Field required",
                        "input": {},
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "five_to_three"],
                        "msg": "Field required",
                        "input": {},
                    },
                ]
            },
        ),
        (
            {
                "strand": None,
                "strand_type": "mrna",
                "five_to_three": True,
            },
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "string_type",
                        "loc": ["body", "strand"],
                        "msg": "Input should be a valid string",
                        "input": None,
                    }
                ]
            },
        ),
        (
            {
                "strand": 123,
                "strand_type": "mrna",
                "five_to_three": True,
            },
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "string_type",
                        "loc": ["body", "strand"],
                        "msg": "Input should be a valid string",
                        "input": 123,
                    }
                ]
            },
        ),
        (
            {
                "strand": "AUG",
                "strand_type": 123,
                "five_to_three": True,
            },
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "literal_error",
                        "loc": ["body", "strand_type"],
                        "msg": "Input should be 'mrna', 'coding' or 'template'",
                        "input": 123,
                        "ctx": {"expected": "'mrna', 'coding' or 'template'"},
                    }
                ]
            },
        ),
        (
            ["AUG"],
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "model_attributes_type",
                        "loc": ["body"],
                        "msg": "Input should be a valid dictionary or object to extract fields from",
                        "input": ["AUG"],
                    }
                ]
            },
        ),
        (
            None,
            STATUS_CODE_UNPROCESSABLE_CONTENT,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body"],
                        "msg": "Field required",
                        "input": None,
                    }
                ]
            },
        ),
    ]
)

def test_decode_endpoint(request_data, expected_status, expected_response):
    response = client.post(ENDPOINT, json=request_data)
    assert response.status_code == expected_status
    assert response.json() == expected_response

cors_tests = pytest.mark.parametrize(
        "origin", 
        [
            "http://localhost:5173",
            "https://dna-decoding-full-stack.vercel.app"
        ]
)

@cors_tests
def test_cors_allows_frontend_origin(origin):
    response = client.post(
        ENDPOINT,
        json={
            "strand": "AUGUAA",
            "strand_type": "mrna",
            "five_to_three": True,
        },
        headers={"Origin": origin},
    )

    assert response.headers["access-control-allow-origin"] == origin

@cors_tests
def test_cors_preflight(origin):
    response = client.options(
        ENDPOINT,
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert "POST" in response.headers["access-control-allow-methods"]

def test_cors_rejects_unallowed_origin():
    response = client.post(
        ENDPOINT,
        json={
            "strand": "AUGUAA",
            "strand_type": "mrna",
            "five_to_three": True,
        },
        headers={"Origin": "https://example.com"},
    )

    assert "access-control-allow-origin" not in response.headers
