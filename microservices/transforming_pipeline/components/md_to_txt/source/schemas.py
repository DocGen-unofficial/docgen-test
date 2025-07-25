from pydantic import BaseModel
from typing import Optional

### Schemas for FastAPI ###

class ParquetConverterResponse(BaseModel):
    status: bool
    details: str
    output_path: Optional[str] = None

class ParquetConverterRequest(BaseModel):
    input_path: str
    output_path: str