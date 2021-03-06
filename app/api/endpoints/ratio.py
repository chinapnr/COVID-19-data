from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fishbase.fish_logger import logger

from app.db import get_db
from app.models.covid import Covid19
from app.schemas.common import get_area_filters, get_date_filters
from app.schemas.filters import RegionFilters, DateFilters
from app.schemas.ratio import *

router = APIRouter()


@router.get("/gender", response_model=GenderRatioInResponse, name="ratio:gender")
async def ratio_gender(
        db: Session = Depends(get_db),
        area_filters: RegionFilters = Depends(get_area_filters),
        time_filters: DateFilters = Depends(get_date_filters), ) -> GenderRatioInResponse:
    """
    查询男女比例信息<br/>
    """
    logger.info(f"received parameters, time_filters:{time_filters}, area_filters:{area_filters}")
    all_data = Covid19.get_all(db)
    print(all_data)
    return GenderRatioInResponse()


@router.get("/age", response_model=AgeRatioInResponse, name="ratio:age")
async def ratio_age(
        area_filters: RegionFilters = Depends(get_area_filters),
        time_filters: DateFilters = Depends(get_date_filters), ) -> AgeRatioInResponse:
    """
    查询年龄比例<br/>
    """
    print(area_filters, time_filters)
    return AgeRatioInResponse()


@router.get("/sars", response_model=SarsNcovRatioInResponse, name="ratio:sars")
async def ratio_sars(
        area_filters: RegionFilters = Depends(get_area_filters),
        time_filters: DateFilters = Depends(get_date_filters), ) -> SarsNcovRatioInResponse:
    """
    查询 ncov 和 sars 的比例<br/>
    """
    print(area_filters, time_filters)
    return SarsNcovRatioInResponse()


@router.get("/rehabilitation", response_model=RehabilitationRatioResponse, name="ratio:rehabilitation")
async def ratio_rehabilitation(
        area_filters: RegionFilters = Depends(get_area_filters),
        time_filters: DateFilters = Depends(get_date_filters), ) -> RehabilitationRatioResponse:
    """
    查询治愈和死亡的比例<br/>
    """
    print(area_filters, time_filters)
    return RehabilitationRatioResponse()
