import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as Vaccine
# from vaccine_patient import VaccinePatient as patient

class TestDB(unittest.TestCase):

    def test_db_connection(self):
        try:
            self.connection_manager = SqlConnectionManager(Server=os.getenv("Server"),
                                                           DBname=os.getenv("DBName"),
                                                           UserId=os.getenv("UserID"),
                                                           Password=os.getenv("Password"))
            self.conn = self.connection_manager.Connect()
        except Exception:
            self.fail("Connection to databse failed")


class TestVaccineCaregiver(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new VaccineCaregiver object
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                                                    cursor=cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Caregivers
                               WHERE CaregiverName = 'Steve Ma'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating caregiver failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating caregiver failed")
    
    def test_verify_schedule(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new VaccineCaregiver object
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                                                    cursor=cursor)
                    # check if schedule has been correctly inserted into CareGiverSchedule
                    sqlQuery = '''
                               SELECT *
                               FROM Caregivers, CareGiverSchedule
                               WHERE Caregivers.CaregiverName = 'Steve Ma'
                                   AND Caregivers.CaregiverId = CareGiverSchedule.CaregiverId
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    hoursToSchedlue = [10,11]
                    minutesToSchedlue = [0, 15, 30, 45]
                    for row in rows:
                        slot_hour = row["SlotHour"]
                        slot_minute = row["SlotMinute"]
                        if slot_hour not in hoursToSchedlue or slot_minute not in minutesToSchedlue:
                            self.fail("CareGiverSchedule verification failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("CareGiverSchedule verification failed")


class TestVaccine(unittest.TestCase):
    def test_vaccine(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    clear_tables(sqlClient)
                    # Create a Vaccine object
                    self.vac = Vaccine(1, 'Pfizer', 1, cursor)
                    # See if vaccine instance has been created correctly
                    sqlQuery = '''
                                SELECT VaccineId, VaccineName, SecondDose
                                FROM Vaccines
                                WHERE VaccineId = 1
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    correct_output = {'VaccineId': 1, 'VaccineName': 'Pfizer', 'SecondDose': True}
                    for row in rows:
                        if row != correct_output:
                            self.fail("Vaccine verification failed")
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Vaccine verification failed")                

    def test_AddDose(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try: 
                    clear_tables(sqlClient)
                    # Create a Vaccine object
                    self.vac = Vaccine(1, 'Pfizer', 1, cursor)

                    self.vac.AddDose(1, 2, cursor)

                    # Check if the VacTotalDoese is correctly updated
                    sqlQuery = '''
                                SELECT VacTotalDoses
                                FROM Vaccines
                                WHERE VaccineId = 1
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    for row in rows:
                        if row['VacTotalDoses'] != 2:
                            self.fail('Vaccine AddDose verification failed: incorect number of total doses '+str(row['VacTotalDoses']))

                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail('Vaccine AddDose verification failed')

    def test_ReserveDoses_second(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
             with sqlClient.cursor(as_dict=True) as cursor:
                try: 
                    clear_tables(sqlClient)
                    # Create a Vaccine object
                    self.vac = Vaccine(1, 'Pfizer', 1, cursor)

                    self.vac.AddDose(1, 2, cursor)
                    self.vac.ReserveDoses(1,cursor)
                    # Check if the VacTotalDoese is correctly updated
                    sqlQuery = '''
                                SELECT VacTotalDoses, VacReserveDoses
                                FROM Vaccines
                                WHERE VaccineId = 1
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['VacTotalDoses'] != 0 or row['VacReserveDoses'] != 2 :
                            self.fail('Vaccine Add2Dose verification failed. Incorrect number total: '+str(row['VacTotalDoses'])+' Reserve: '+ str(row['VacTotalDoses']))

                    clear_tables(sqlClient)
                    
                    # repeat the researve and nothing should change, enter not enough condition 

                    message = self.vac.ReserveDoses(1,cursor)
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['VacTotalDoses'] != 0 or row['VacReserveDoses'] != 2 or message != 'Not enough':
                            self.fail('Vaccine Second Dose reserve -not enough- conditon failed')

                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail('Vaccine ReserveDose (second dose) verification failed')

    def test_ReserveDoses_one(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
             with sqlClient.cursor(as_dict=True) as cursor:
                try: 
                    clear_tables(sqlClient)
                    # Create a Vaccine object
                    self.vac = Vaccine(2, 'Jonthan', 0, cursor)

                    self.vac.AddDose(2, 1, cursor)
                    self.vac.ReserveDoses(2,cursor)
                    # Check if the VacTotalDoese is correctly updated
                    sqlQuery = '''
                                SELECT VacTotalDoses, VacReserveDoses
                                FROM Vaccines
                                WHERE VaccineId = 2
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['VacTotalDoses'] != 0 or row['VacReserveDoses'] != 1 :
                            self.fail('Vaccine Add2Dose verification failed. Incorrect number total: '+str(row['VacTotalDoses'])+' Reserve: '+ str(row['VacTotalDoses']))

                    # repeat the researve and nothing should change, enter not enough condition 
                    message = self.vac.ReserveDoses(2,cursor)
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['VacTotalDoses'] != 0 or row['VacReserveDoses'] != 1 or message != 'Not enough':
                            self.fail('Vaccine Second Dose reserve -not enough- conditon failed')

                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail('Vaccine ReserveDose (second dose) verification failed')




if __name__ == '__main__':
    unittest.main()
