import fastapi

from src.api.v1.routes.parcel import router as parcel_router

router = fastapi.APIRouter()
router.include_router(router=parcel_router)
