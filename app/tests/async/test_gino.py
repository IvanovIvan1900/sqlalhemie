import pytest
from gino import Gino


class TestQuery():
    
    @pytest.mark.asyncio
    async def test_insert_items(self, db:Gino, table_tasks)->None:
        user = await table_tasks.create(task_name='First task')
        a = 4
