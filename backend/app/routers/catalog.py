from fastapi import APIRouter

from app.catalog import CATALOG
from app.schemas import CatalogComponentOut, CatalogFieldOut

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


@router.get("/components", response_model=list[CatalogComponentOut])
def list_catalog_components():
    return [
        CatalogComponentOut(
            type_key=c.type_key,
            category=c.category.value,
            label_ko=c.label_ko,
            note_ko=c.note_ko,
            fields=[
                CatalogFieldOut(
                    key=f.key,
                    label_ko=f.label_ko,
                    type=f.type.value,
                    unit=f.unit,
                    min=f.min,
                    max=f.max,
                    step=f.step,
                    options=f.options,
                )
                for f in c.fields
            ],
        )
        for c in CATALOG
    ]
