import requests as rq
import urllib
import csv
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import DataModel
import DbTable

if __name__ == '__main__':
    FileURL = 'https://twtransfer.energytransfer.com/ipost/capacity/operationally-available'
    DbURL = "sqlite:///TecEnergyTakeHome.db"
    
    engine = create_engine(DbURL)
    DbTable.createTable(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    thisDay = datetime.datetime.now()
  
    for day in range(3):
        dt = thisDay.strftime('%m/%d/%Y')
        for cycle in range(1, 6):
            print("Running cycle {0} for date {1}".format(cycle, dt))
            RqPayload = {'f':'csv', 'extension':'csv', 'asset':'TW', 'gasDay': dt, 'cycle': str(cycle), \
                        'searchType': 'NOM', 'searchString': '', 'locType': 'ALL', 'locZone': 'ALL'}
                        
            Params = urllib.parse.urlencode(RqPayload)
            resp = rq.get(FileURL, params = Params)
            if resp.status_code == 200:
                decoded_content = resp.content.decode('utf-8')
                csvreader = csv.reader(decoded_content.splitlines(), delimiter=',')
                fields = next(csvreader)
                for i in range(len(fields)):
                    fields[i] = fields[i].replace(" ", "_")
                    fields[i] = fields[i].replace("/", "_")
                
                for row in csvreader:
                    RowData = {}
                    for i in range(len(fields)):
                        RowData[fields[i]] = row[i]
                        
                    # Row data validation
                    dModel = DataModel.DataModel(**RowData)
                    # Row database validation
                    db_energy = DbTable.Energy(Loc = dModel.Loc,
                                            Loc_Zn = dModel.Loc_Zn,
                                            Loc_Name = dModel.Loc_Name,
                                            Loc_Purp_Desc = dModel.Loc_Purp_Desc,
                                            Loc_QTI = dModel.Loc_QTI,
                                            Flow_Ind = dModel.Flow_Ind,
                                            DC = dModel.DC,
                                            OPC = dModel.OPC,
                                            TSQ = dModel.TSQ,
                                            OAC = dModel.OAC,
                                            IT = dModel.IT,
                                            Auth_Overrun_Ind = dModel.Auth_Overrun_Ind,
                                            Nom_Cap_Exceed_Ind = dModel.Nom_Cap_Exceed_Ind,
                                            All_Qty_Avail = dModel.All_Qty_Avail,
                                            Qty_Reason = dModel.Qty_Reason)
                    
                    session.add(db_energy)
                    session.commit()
                    session.refresh(db_energy)
            
            else:
                print("http status code was ", resp.status_code)
        
        thisDay = datetime.datetime.fromtimestamp(thisDay.timestamp() - 86400)