import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as Vaccine
from vaccine_patient import VaccinePatient as patient
from vaccine_reservation_scheduler import VaccineReservationScheduler

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


class TestReservationScheduler(unittest.TestCase):
    def testCheckStauts(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                    cursor=cursor)
                    # create a new scheduler 
                    self.scheduler = VaccineReservationScheduler()

                    current_status = self.scheduler.CheckStatus(1,cursor=cursor)

                    if current_status != 0:
                        self.fail("Fail to return the correct current status")

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Check Staus failed with an exception")

    def testHold(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                                        cursor=cursor)
                    # create a new scheduler 
                    self.scheduler = VaccineReservationScheduler()
                    self.scheduler.PutHoldOnAppointmentSlot(1,cursor=cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT SlotStatus
                               FROM CareGiverSchedule
                               WHERE CaregiverSlotSchedulingId = 1
                               '''
                    cursor.execute(sqlQuery)
                    row = cursor.fetchone()
                    if row['SlotStatus'] != 1:
                        self.fail("Put Schedulin Slot on Hold failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)

                    message1 = self.scheduler.PutHoldOnAppointmentSlot(1,cursor=cursor)
                    if message1 != "Given slot is not free":
                        self.fail("Fail to recognize slot as not free")

                    message2 = self.scheduler.PutHoldOnAppointmentSlot(999, cursor=cursor)
                    if message2 != "Wrong Slot ID":
                        self.fail("Fail to-recogonize wrong slot ID")

                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Put Schedulin Slot on Hold failed with an exception")


    def testReserveSlot(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                                        cursor=cursor)
                    # create a new scheduler 
                    self.scheduler = VaccineReservationScheduler()
                    self.scheduler.PutHoldOnAppointmentSlot(1,cursor=cursor)
                    self.scheduler.ScheduleAppointmentSlot(1,cursor=cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT SlotStatus
                               FROM CareGiverSchedule
                               WHERE CaregiverSlotSchedulingId = 1
                               '''
                    cursor.execute(sqlQuery)
                    row = cursor.fetchone()
                    if row['SlotStatus'] != 2:
                        self.fail("Put Schedulin Slot on Reserve failed")

                    message1 = self.scheduler.PutHoldOnAppointmentSlot(1,cursor=cursor)
                    if message1 != "Given slot is not on hold":
                        self.fail("Fail to recognize slot as not on hold")

                    message2 = self.scheduler.PutHoldOnAppointmentSlot(999, cursor=cursor)
                    if message2 != "Wrong Slot ID":
                        self.fail("Fail to-recogonize wrong slot ID")

                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Put Schedulin Slot on Hold failed with an exception")



class TestPatient(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new patient 

                    self.patient_a= patient('Jon Do', cursor = cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Patients
                               WHERE PatientName = 'Jon Do'

                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating patient failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating patient failed with some exception")

    def testReserveAppt(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new patient and vaccine

                    self.patient_a= patient('Jon Do', cursor = cursor)
                    self.vac = Vaccine('Pfizer', 2, 21, cursor)
                    self.vac.AddDose(4, cursor)

                    self.patient_a.ReserveAppointment(1,self.vac, cursor)

                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT VaccineStatus
                               FROM Patients
                               '''
                    cursor.execute(sqlQuery)
                    row = cursor.fetchone()

                    if row['VaccineStatus'] != 4:
                        self.fail("Fail to reserve both dose for patient")

                    
                    sqlQuery = '''
                               SELECT *
                               FROM VaccineAppointments
                               WHERE PatientId = 1 and VaccineNmae = 'Pfizer'
                               '''

                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 2:
                        self.fail("Fail to create two appointment entries of Appoint table")

                    for row in rows:
                        if row["CaregiverSlotSchedulingId"] != 0:
                            self.fail("Fail to assign correct slot Id to the Appointment table")

                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating patient failed with some exception")
    def testScheduleAppt(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new patient and vaccine

                    self.patient_a= patient('Jon Do', cursor = cursor)
                    self.vac = Vaccine('Pfizer', 2, 21, cursor)
                    self.vac.AddDose(4, cursor)

                    self.patient_a.ReserveAppointment(1,self.vac, cursor)

                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT VaccineStatus
                               FROM Patients
                               '''
                    cursor.execute(sqlQuery)
                    row = cursor.fetchone()

                    if row['VaccineStatus'] != 4:
                        self.fail("Fail to reserve both dose for patient")

                    
                    sqlQuery = '''
                               SELECT *
                               FROM VaccineAppointments
                               WHERE PatientId = 1 and VaccineNmae = 'Pfizer'
                               '''

                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 2:
                        self.fail("Fail to create two appointment entries of Appoint table")

                    for row in rows:
                        if row["CaregiverSlotSchedulingId"] != 0:
                            self.fail("Fail to assign correct slot Id to the Appointment table")

                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating patient failed with some exception")

class TestOverall(unittest.TestCase):
    def test_overall(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    clear_tables(sqlClient)
                    vac = Vaccine('Pfizer', 2, 21, cursor)
                    vac.AddDose(5, cursor)

                    # create a new VaccineCaregiver object
                    caregiver_a = VaccineCaregiver(name="John Smith",
                                                    cursor=cursor)
                    caregiver_b = VaccineCaregiver(name="Mary Smith",
                                                    cursor=cursor)

                    patient_a = patient('Adam Uno', cursor = cursor)
                    
                    patient_a.ReserveAppointment(1, vac, cursor)
                    patient_a.ScheduleAppointment(cursor)

                    patient_b = patient('Bruce Dos', cursor = cursor)
                    
                    patient_b.ReserveAppointment(2, vac, cursor)
                    patient_b.ScheduleAppointment(cursor)

                    patient_c = patient('Cathy Tres', cursor = cursor)
                    
                    patient_c.ReserveAppointment(3, vac, cursor)
                    patient_c.ScheduleAppointment(cursor)

                    patient_d = patient('Dasiy Cuatro', cursor = cursor)
                    
                    patient_d.ReserveAppointment(4, vac, cursor)
                    patient_d.ScheduleAppointment(cursor)

                    patient_e = patient('Ema Cinco', cursor = cursor)
                    
                    patient_e.ReserveAppointment(5, vac, cursor)
                    patient_e.ScheduleAppointment(cursor)

                    sqlQuery = '''
                                SELECT *
                                FROM Vaccines
                                '''
                    cursor.execute(sqlQuery)
                    vac_rows = cursor.fetchall()

                    sqlQuery = '''
                                SELECT PatientName
                                FROM Patients
                                WHERE VaccineStatus = 5
                                '''
                    cursor.execute(sqlQuery)
                    pat_rows = cursor.fetchall()

                    sqlQuery = '''
                                SELECT *
                                FROM VaccineAppointments
                                '''
                    cursor.execute(sqlQuery)
                    appt_rows = cursor.fetchall()


                    sqlQuery = '''
                                select CaregiverSlotSchedulingId
                                from CareGiverSchedule
                                where SlotStatus = 2
                                '''
                    cursor.execute(sqlQuery)
                    slot_rows = cursor.fetchall()
                    for row in slot_rows:
                        pass

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Overall testin failed with some exception")




if __name__ == '__main__':
    unittest.main()
