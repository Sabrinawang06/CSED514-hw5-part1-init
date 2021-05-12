import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from new_vaccines import COVID19Vaccine as Vaccine

"""
with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:
        try:
           
            sqlQuery = '''
                        SELECT StatusCode
                        FROM AppointmentStatusCodes
                        WHERE StatusCodeId = 0
                        '''
            cursor.execute(sqlQuery)
            rows = cursor.fetchall()
            for row in rows:
                print(row['StatusCode'])

            sqlQuery = '''
                        SELECT StatusCode
                        FROM AppointmentStatusCodes
                        WHERE StatusCodeId = 1
                        '''
            cursor.execute(sqlQuery)
            rows = cursor.fetchall()
            print(rows)

        except Exception:
            pass
"""


with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:
        cursor.execute("DELETE FROM Vaccines")
        vac = Vaccine('Pfizer', 2, 21, cursor) 
        vac.AddDose('Pfizer', 1, cursor)
        vac.ReserveDoses('Pfizer', cursor)



        # vac = Vaccine('Jonthan', 1, cursor) 
        # vac.AddDose('Jonthan', 1, cursor)
        # vac.ReserveDoses('Jonthan',cursor)

        sqlQuery = '''
                    SELECT *
                    FROM Vaccines
                    '''
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        print(rows)

# vid = 1
# name = 'Pifzer'
# second = 1

# print("INSERT INTO Vaccines (VaccineId, VaccineName, SecondDose) VALUES ({},{},{})".format(vid,"'"+name+"'",second))