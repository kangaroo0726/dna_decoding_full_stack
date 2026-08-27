# DNA Decoder

DNA Decoder is a full-stack web application that converts DNA and mRNA sequences into mRNA codons and translated proteins.

## Live Demo

Click [here](https://dna-decoding-full-stack.vercel.app/ "DNA Decoder").

Note: The backend may take longer than usual to respond to the first request after a period of inactivity due to a cold start. Subsequent requests should respond normally.

## Overview

This project started during my final year of high school, when I wanted to code a DNA decoder to help me with a biology assignment. After building the initial decoder, I kept expanding on the idea and improving how it worked. What began as a simple command-line tool eventually grew into a full-stack application with a React frontend and a FastAPI backend, making DNA decoding more accessible through a web interface.

## Features

- Decode DNA and mRNA sequences through a simple web interface.
- Support template DNA, coding DNA, and mRNA input formats.
- Convert template DNA to its complementary mRNA sequence.
- Convert coding DNA into mRNA by replacing thymine (`T`) with uracil (`U`).
- Handle sequence orientation by allowing input to be interpreted in either its current direction or from 5' to 3'.
- Search for the start codon (`AUG`) and extract codons until a stop codon is reached.
- Translate extracted mRNA codons into their corresponding protein names.
- Accept sequences entered directly into the text area or loaded from `.txt` files.
- Display the converted mRNA/codon sequence and translated proteins separately.
- Provide loading feedback while the frontend communicates with the backend.
- Report malformed sequences, invalid strand types, missing start codons, and connection failures to the user.

## Architecture

### React frontend --> FastAPI REST API --> DNA decoder

The React frontend provides the input form, strand-type and orientation controls, file upload, loading state, and result display. When the user selects **Decode**, it sends the sequence and decoding options to the backend as a JSON request.

The FastAPI backend exposes the `/decode` endpoint. It validates the request with Pydantic, passes the data to the decoder, and returns the converted sequence and translated proteins as JSON. Invalid input is returned to the frontend as an informative HTTP error.

The Python DNA decoder contains the core biological and algorithmic logic. It applies the requested orientation, converts the selected strand type into mRNA, finds the reading frame from the start codon to a stop codon, and translates the resulting codons into protein names.

## Tech Stack

Frontend

- React
- JavaScript
- CSS

Backend

- Python
- FastAPI
- Pydantic

Deployment

- Vercel
- Render

## How It Works

- mRNA is interpreted in the 5' to 3' direction. If the input is not provided in that orientation, the sequence is reversed before processing.
- Template DNA is reversed and converted using complementary base pairing to produce an mRNA sequence.
- Coding DNA is converted to mRNA by replacing each thymine (`T`) with uracil (`U`). Existing mRNA sequences are processed without base conversion.
- Translation begins at the first start codon, `AUG`, which corresponds to methionine.
- After the start codon is located, the mRNA sequence is read in groups of three nucleotides, known as codons.
- Translation continues until a stop codon (`UGA`, `UAG`, or `UAA`) is encountered or the sequence contains no further complete codons.
- Each codon is matched to its corresponding protein using the genetic code defined in `decoder/constants.py`.
- Multiple codons may correspond to the same protein, reflecting the redundancy of the genetic code.

## Project Structure

```text
.
|-- .gitignore
|-- api/
|   |-- __init__.py
|   `-- main.py
|-- decoder/
|   |-- __init__.py
|   |-- constants.py
|   `-- decoder.py
|-- frontend/
|   |-- .gitignore
|   |-- eslint.config.js
|   |-- index.html
|   |-- package.json
|   |-- package-lock.json
|   |-- README.md
|   |-- vite.config.js
|   |-- public/
|   |   |-- favicon.svg
|   |   `-- icons.svg
|   `-- src/
|       |-- components/
|       |   |-- DecodeButton.jsx
|       |   |-- DnaInput.jsx
|       |   `-- Results.jsx
|       |-- App.css
|       |-- App.jsx
|       |-- index.css
|       `-- main.jsx
|-- tests/
|   |-- __init__.py
|   |-- constants.py
|   |-- dna_template_100k.txt
|   |-- dna_template_1m.txt
|   |-- test_api.py
|   `-- test_decoder.py
|-- requirements.txt
`-- README.md
```

- `api/main.py` defines the FastAPI application, CORS configuration, request model, and `/decode` endpoint. `api/__init__.py` marks the API module as a package.
- `decoder/decoder.py` implements strand orientation, DNA-to-mRNA conversion, codon extraction, and protein translation.
- `decoder/constants.py` contains nucleotide rules, codon mappings, start and stop codons, and supported strand types.
- `frontend/src/App.jsx` coordinates input state, API requests, loading feedback, and result rendering.
- `frontend/src/components/` contains the sequence input, decode button, and output components.
- `frontend/src/App.css` and `frontend/src/index.css` define the frontend styling.
- `tests/test_decoder.py` contains unit tests for the decoder functions.
- `tests/test_api.py` contains endpoint, request-validation, and CORS tests.
- `tests/constants.py` contains shared API test constants.
- `tests/` also contains tracked large DNA fixtures for manual testing and automated test data.
- `requirements.txt` lists the Python backend and test dependencies.

## Local Development

### Backend

From the project root, create and activate a virtual environment, then install the Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Start the FastAPI development server from the project root:

```bash
uvicorn api.main:app --reload
```

The backend is then available at `http://localhost:8000`.

### Frontend

In a separate terminal, install the frontend dependencies and start the Vite development server:

```bash
cd frontend
npm install
npm run dev
```

The frontend is then available at `http://localhost:5173`.

### Environment Variable

Create a file named `.env` inside the `frontend/` directory with the backend URL:

```env
VITE_API_URL=http://localhost:8000
```

The Vite development server must be restarted after changes to environment variables. The local frontend origin is already permitted by the backend CORS configuration.

## API

### `POST /decode`

Decodes a DNA or mRNA strand and translates the resulting codons into proteins.

#### Request

The request body must be a JSON object containing the following fields:

```json
{
  "strand": "AUGCCCUAA",
  "strand_type": "mrna",
  "five_to_three": true
}
```

- `strand`: The DNA or mRNA sequence to decode.
- `strand_type`: The input type: `template`, `coding`, or `mrna`.
- `five_to_three`: A Boolean indicating whether the input is already oriented 5' to 3'.

#### Successful Response

```json
{
  "converted": "AUGCCCUAA",
  "proteins": ["methionine", "proline", "stop"]
}
```

- `converted`: The resulting mRNA sequence after strand conversion and codon extraction, up until the first stop codon.
- `proteins`: The translated protein names in sequence order. The terminating stop codon is included as `stop`.

Malformed sequences and sequences without a start codon return a `400 Bad Request` response with an explanatory `detail` message. Unsupported strand types, invalid field types, and requests that omit required fields are rejected by FastAPI with a `422 Unprocessable Entity` response.

Interactive API documentation is available at `http://localhost:8000/docs` when the backend is running.

## Deployment

The application is deployed as two separate services. The React frontend is built with Vite and hosted on Vercel at [dna-decoding-full-stack.vercel.app](https://dna-decoding-full-stack.vercel.app/). The FastAPI backend is hosted separately on Render and provides the `/decode` endpoint.

The production frontend uses the `VITE_API_URL` environment variable to locate the deployed Render API. When a decode request is submitted, the browser sends the sequence data from the Vercel frontend to the backend on Render, which performs the decoding and returns the results as JSON.

The backend CORS configuration permits requests from both the local Vite development server and the deployed Vercel frontend. The Render service may take longer to respond to its first request after inactivity because of a cold start.

## Testing

The automated test suite is stored in the `tests/` directory. It includes decoder unit tests and API tests for the `/decode` endpoint. Coverage includes valid strand types, orientation, malformed input, missing start codons, translation boundaries, request validation, and CORS behavior.

The directory also contains template DNA files containing 100,000 and 1,000,000 bases. These support manual testing of sequence input, file upload, decoding behavior, and larger sequences.

Run the backend test suite from the project root with:

```bash
python -m pytest
```

Or simply:

```bash
pytest
```

## Development Progress

### Stage 1: Core Application and Documentation (Complete)

Stage 1 established the working DNA decoding application and its supporting documentation. The original command-line decoder was expanded into a full-stack system with a React and Vite frontend, a FastAPI backend, and a Python decoding layer.

- [x] Implemented support for template DNA, coding DNA, and mRNA sequences.
- [x] Added strand orientation handling, complementary-base conversion, mRNA conversion, codon extraction, and protein translation.
- [x] Added a web interface with direct text entry, `.txt` file upload, strand-type selection, orientation controls, loading feedback, and separate result displays.
- [x] Added the `POST /decode` API endpoint with Pydantic request validation, JSON responses, CORS configuration, and client-error handling.
- [x] Added manual test inputs, generated large DNA fixtures, and documentation for the project overview, features, architecture, workflow, project structure, local development, API, deployment, and current testing status.
- [x] Deployed the frontend to Vercel and the backend to Render, with environment-based API configuration.

### Stage 2: Engineering Quality (In Progress)

Stage 2 will strengthen the application's reliability, maintainability, and test coverage.

- [x] **Testing:** Added decoder unit tests and API tests for `POST /decode`, including invalid input, error responses, boundary conditions, request validation, and CORS behavior.
- [ ] **Frontend testing:** Add targeted tests for the React components and user workflows.
- [x] **Validation and error handling:** Added request validation at the Pydantic and API layers while retaining decoder-level checks. Expected client errors are returned as consistent `400` or `422` responses.
- [ ] **Continuous integration and delivery:** Configure GitHub Actions to run automated checks and prevent changes that fail validation from being merged or deployed.
- [ ] **Code quality:** Improve naming and documentation, reduce duplication, and refine the architecture where necessary.
- [ ] **Decoder capabilities:** Extend the current DNA functionality where additional features provide practical value.
- [ ] **Performance assessment:** Establish profiling and benchmarking practices before applying optimizations, with particular attention to large-input processing.

The intended outcome is a more dependable application supported by repeatable quality checks.

### Stage 3: Users and Persistence

Stage 3 will introduce persistence and account management, transforming the public decoder into a multi-user application.

- [ ] **Data persistence:** Add PostgreSQL support for user accounts, saved DNA/RNA sequences, and decoding history.
- [ ] **Account management:** Implement registration, login, logout, password hashing, authentication, authorization, and user profiles.
- [ ] **Access control:** Add protected frontend routes and API endpoints, ensuring that user-specific data is accessible only to its owner.
- [ ] **Security:** Apply secure session and authentication practices together with appropriate protections for public API endpoints.
