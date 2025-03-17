from typing import Optional

from pydantic import BaseModel, Field, field_validator

class DataModel(BaseModel):
    Loc: int
    Loc_Zn: str
    Loc_Name: str
    Loc_Purp_Desc: str
    Loc_QTI: str
    Flow_Ind: str
    DC: Optional[int]
    OPC: int
    TSQ: int
    OAC: int
    IT: str
    Auth_Overrun_Ind: str
    Nom_Cap_Exceed_Ind: str
    All_Qty_Avail: str
    Qty_Reason: str = Field(default = "")
    
    @field_validator('DC', mode='before')
    def ifIntIsEmpty(cls, value) -> Optional[int]:
        if value == "":
            return None
        else:
            return int(value)
        