from uuid import UUID
from pydantic import BaseModel


class CutomerProfit(BaseModel):
    uuid: UUID | str
    sum: float
    full_name: str
