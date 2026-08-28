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

app = FastAPI()
app.openapi_version = "3.0.2"
app.servers = [
    {"url": PUBLIC_BASE_URL}
]

app.mount(
    "/files",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="generated_files",
)


class StatisticsRequest(BaseModel):
    numbers: list[float]


class WordDocumentRequest(BaseModel):
    title: str = Field(..., description="Word 文档标题")
    paragraphs: list[str] = Field(
        ...,
        min_length=1,
        description="Word 正文段落；每个数组元素是一段正文",
    )


@app.get("/")
def root():
    return {
        "message": "Python Tool API is running"
    }


@app.post("/statistics")
def statistics(request: StatisticsRequest):
    return calculate_statistics(request.numbers)


@app.post("/documents/word")
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