from fastapi import APIRouter
from source.schemas import ParquetConverterResponse, ParquetConverterRequest
from source.converter import ParquetConverter

convert_to_text_router = APIRouter(prefix="/v4.2", tags=["Transforming Layer - Convert files to text"])

@convert_to_text_router.post("/convert-files-to-text/", response_model=ParquetConverterResponse)
async def transform_files_to_text(request: ParquetConverterRequest):
    """
    Trasformazione di file in formato .md e .rst in testo semplice.
    """
    extensions = ['.md', '.rst']

    transformer = ParquetConverter(
        input_path=request.input_path,
        output_path=request.output_path,
        extensions=extensions
    )

    await transformer.load_parquet()
    files = await transformer.file_to_text(transformer.extensions)
    files.to_parquet(request.output_path, index=False)

    return ParquetConverterResponse(
        status=True,
        details="File trasformati con successo.",
        output_path=request.output_path
    )