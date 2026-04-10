from pydantic import BaseModel
from typing import List, Optional

class KitchenIntent(BaseModel):
    layout: Optional[str] = None
    style: Optional[str] = None
    colors: List[str] = []
    budget_max: Optional[int] = None
    priorities: List[str] = []
    ambiguities: List[str] = []
    confidence: float