from src.schemas.facilities import FacilitiesSchemaAddData
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, facility_data: FacilitiesSchemaAddData):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()
        test_task.delay()
        return facility
