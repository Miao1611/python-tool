from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from calculator import calculate_statistics
from office_generator import create_word_document


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "generated_files"
OUTPUT_DIR.mkdir(exist_ok=True)

PUBLIC_BASE_URL = "https://python-tool-zhwh.onrender.com"

app = FastAPI(
    title="Office and Calculation API",
    description=(
        "A reusable API for numeric statistics and Office document generation. "
        "Use the statistics endpoint only for numeric calculations. "
        "Use the Word endpoint only when a DOCX document is requested."
    ),
    version="1.0.0",
    openapi_version="3.0.2",
    servers=[
        {"url": PUBLIC_BASE_URL}
    ],
)

app.mount(
    "/files",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="generated_files",
)


class StatisticsRequest(BaseModel):
    numbers: list[float] = Field(
        ...,
        min_length=1,
        description=(
            "A non-empty list of numbers. "
            "The API returns count, sum, average, minimum, and maximum."
        ),
    )


class StatisticsResponse(BaseModel):
    count: int = Field(..., description="Number of values in the input list.")
    sum: float = Field(..., description="Sum of all input values.")
    average: float = Field(..., description="Arithmetic mean of all input values.")
    min: float = Field(..., description="Smallest input value.")
    max: float = Field(..., description="Largest input value.")


class WordDocumentRequest(BaseModel):
    title: str = Field(
        ...,
        description="Title displayed at the top of the generated Word document.",
    )
    paragraphs: list[str] = Field(
        ...,
        min_length=1,
        description=(
            "Non-empty body paragraphs for the Word document. "
            "Each list item becomes one paragraph."
        ),
    )


class WordDocumentResponse(BaseModel):
    message: str = Field(
        ...,
        description="Confirmation that the Word document was created.",
    )
    filename: str = Field(
        ...,
        description="Name of the generated DOCX file.",
    )
    download_url: str = Field(
        ...,
        description=(
            "Public URL for downloading the generated DOCX file. "
            "Return this link directly to the user."
        ),
    )


@app.get(
    "/",
    tags=["System"],
    summary="Check API status",
    description="Confirms that the Office and Calculation API is running.",
)
def root():
    return {
        "message": "Office and Calculation API is running"
    }


@app.post(
    "/statistics",
    tags=["Calculation"],
    summary="Calculate numeric statistics",
    description=(
        "Use this endpoint when the user asks for count, sum, average, "
        "minimum, or maximum of a list of numbers. "
        "Do not calculate these values manually when this tool is available."
    ),
    operation_id="calculate_statistics",
    response_model=StatisticsResponse,
    response_description="Calculated statistics for the provided numbers.",
)
def statistics(request: StatisticsRequest):
    return calculate_statistics(request.numbers)


@app.post(
    "/documents/word",
    tags=["Office"],
    summary="Generate a Word document",
    description=(
        "Use this endpoint only when the user explicitly asks to create a "
        "Word document, DOCX report, summary, meeting minutes, or formal text file. "
        "Provide a title and one or more body paragraphs. "
        "On success, return the download_url to the user."
    ),
    operation_id="generate_word_document",
    response_model=WordDocumentResponse,
    response_description=(
        "Generated DOCX filename and its public download URL."
    ),
)
def create_word(request: WordDocumentRequest):
    filename = create_word_document(
        title=request.title,
        paragraphs=request.paragraphs,
        output_dir=OUTPUT_DIR,
    )

    return {
        "message": "Word document created successfully",
        "filename": filename,
        "download_url": f"{PUBLIC_BASE_URL}/files/{filename}",
    }