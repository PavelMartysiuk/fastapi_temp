from typing import List, Optional

from pydantic import BaseModel

from server.enums.status_enum import StatusEnum


class StatusSchema(BaseModel):
    status: StatusEnum
    errors: Optional[List[str]]
