import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from new_vaccines import COVID19Vaccine as Vaccine
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
                    self.vac = Vaccine('Pfizer', 2, 21, cursor)
                    # See if vaccine instance has been created correctly
                    sqlQuery = '''
                                SELECT VaccineName, DosesPerPatient, DaysBetweenDoses
                                FROM Vaccines
                                WHERE VaccineName = 'Pfizer'
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    correct_output = {'VaccineName': 'Pfizer', 'DosesPerPatient': 2, 'DaysBetweenDoses':21}
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
                    self.vac = Vaccine('Pfizer', 2, 21, cursor)

                    self.vac.AddDose('Pfizer', 2, cursor)

                    # Check if the VacTotalDoese is correctly updated
                    sqlQuery = '''
                                SELECT AvailableDoses
                                FROM Vaccines
                                WHERE VaccineName = 'Pfizer'
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    for row in rows:
                        if row['AvailableDoses'] != 2:
                            self.fail('Vaccine AddDose verification failed: incorect number of total doses '+str(row['AvailableDoses']))

                    clear_tables(sqlClient)


                    # Try AddDose for the wrong index 
                    message = self.vac.AddDose('Pf', 2, cursor)
                    
                    if message !='Wrong Id':
                        self.fail("AddDose fail to detect the wrong VaccineName")


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
                    self.vac = Vaccine('Pfizer', 2, 21, cursor)

                    self.vac.AddDose('Pfizer', 2, cursor)
                    self.vac.ReserveDoses('Pfizer',cursor)
                    # Check if the VacTotalDoese is correctly updated
                    sqlQuery = '''
                                SELECT AvailableDoses, ReservedDoses
                                FROM Vaccines
                                WHERE VaccineName = 'Pfizer'
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['AvailableDoses'] != 0 or row['ReservedDoses'] != 2 :
                            self.fail('Vaccine Add2Dose verification failed. Incorrect number total: '+str(row['AvailableDoses'])+' Reserve: '+ str(row['AvailableDoses']))

                    clear_tables(sqlClient)
                    
                    # repeat the researve and nothing should change, enter not enough condition 

                    message = self.vac.ReserveDoses('Pfizer',cursor)
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['AvailableDoses'] != 0 or row['ReservedDoses'] != 2 or message != 'Not enough':
                            self.fail('Vaccine Second Dose reserve -not enough- conditon failed')

                    # Try AddDose for the wrong index 
                    message2 = self.vac.ReserveDoses('Pf', cursor)       
                    if message2 !='Wrong Id':
                        self.fail("ReserveDose fail to detect the wrong VaccineName")

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
                    self.vac = Vaccine('Jonthan', 1, 0, cursor)

                    self.vac.AddDose('Jonthan', 1, cursor)
                    self.vac.ReserveDoses('Jonthan',cursor)
                    # Check if the VacTotalDoese is correctly updated
                    sqlQuery = '''
                                SELECT AvailableDoses, ReservedDoses
                                FROM Vaccines
                                WHERE VaccineName = 'Jonthan'
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['AvailableDoses'] != 0 or row['ReservedDoses'] != 1 :
                            self.fail('Vaccine Add2Dose verification failed. Incorrect number total: '+str(row['AvailableDoses'])+' Reserve: '+ str(row['AvailableDoses']))

                    # repeat the researve and nothing should change, enter not enough condition 
                    message = self.vac.ReserveDoses('Jonthan',cursor)
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    for row in rows:
                        if row['AvailableDoses'] != 0 or row['ReservedDoses'] != 1 or message != 'Not enough':
                            self.fail('Vaccine Second Dose reserve -not enough- conditon failed')
                            
                    # Try AddDose for the wrong index 
                    message2 = self.vac.ReserveDoses('Pf', cursor)       
                    if message2 !='Wrong Id':
                        self.fail("ReserveDose fail to detect the wrong VaccineName")


                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail('Vaccine ReserveDose (second dose) verification failed')




if __name__ == '__main__':
    unittest.main()
