from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class MonthSpending(BaseModel):
    food: float = Field(..., alias="식비")
    transport: float = Field(..., alias="교통")
    culture: float = Field(..., alias="문화")
    health: float = Field(..., alias="의료")
    housing: float = Field(0, alias="주거")
    shopping: Optional[float] = Field(0, alias="쇼핑")
    education: Optional[float] = Field(0, alias="교육")
    etc: Optional[float] = Field(0, alias="기타")

    class Config:
        populate_by_name = True
        extra = "allow"

class SpendingInput(BaseModel):
    this_month: MonthSpending
    last_month: MonthSpending

    class Config:
        populate_by_name = True

@router.post("/analyze-spending", tags=["Analysis"])
async def analyze_spending(input_data: SpendingInput):
    this = input_data.this_month.dict(by_alias=True)
    last = input_data.last_month.dict(by_alias=True)

    top_category = max(this, key=this.get)
    top_value = this[top_category]
    last_value = last.get(top_category, 0)

    change = top_value - last_value
    change_percent = f"{change * 100:+.1f}%"

    comment = (
        f"📊 이번 달에는 '{top_category}' 분야에 소비가 가장 많았습니다.\n"
        f"🔮 다음 달에도 '{top_category}' 소비가 높을 가능성이 있습니다."
    )

    return {
        "top_category": top_category,
        "comment": comment,
        "change_from_last_month": change_percent
    }
