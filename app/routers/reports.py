from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.database import crud
from app.dependencies import get_db
from app.schemas import reports
from app.utils import auth


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.get("/customers/profit", summary="Profit pre customer")
async def cutomers_profit(
    start_date: str = None,
    end_date: str = None,
    db=Depends(get_db)
) -> List[reports.CutomerProfit]:
    rows = crud.reports.get_customer_sum_report(db, start_date, end_date)
    res: List[reports.CutomerProfit] = []
    for uuid, full_name, sum in rows:
        res.append(reports.CutomerProfit(uuid=uuid, full_name=full_name, sum=sum))
    if not res:
        raise HTTPException(status_code=404)
    res.sort(key=lambda x: -x.sum)
    return res
