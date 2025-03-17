from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Energy(Base):
    __tablename__ = 'TecEnergyTakeHome'
    id = Column(Integer, primary_key=True)
    Loc = Column(Integer)
    Loc_Zn = Column(String)
    Loc_Name = Column(String)
    Loc_Purp_Desc = Column(String)
    Loc_QTI = Column(String)
    Flow_Ind = Column(String)
    DC = Column(Integer, nullable=True)
    OPC = Column(Integer)
    TSQ = Column(Integer)
    OAC = Column(Integer)
    IT = Column(String)
    Auth_Overrun_Ind = Column(String)
    Nom_Cap_Exceed_Ind = Column(String)
    All_Qty_Avail = Column(String)
    Qty_Reason = Column(String, nullable=True)
    
def createTable(engine):
    Base.metadata.create_all(engine)