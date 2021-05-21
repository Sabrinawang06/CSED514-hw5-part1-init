import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as Vaccine
from vaccine_patient import VaccinePatient as patient
from vaccine_reservation_scheduler import VaccineReservationScheduler

class temp(unittest.TestCase):
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
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                                        cursor=cursor)
                    self.patient_a.ReserveAppointment(1,self.vac, cursor)
                    self.patient_a.ScheduleAppointment(cursor)

                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT VaccineStatus
                               FROM Patients
                               '''
                    cursor.execute(sqlQuery)
                    row = cursor.fetchone()

                    if row['VaccineStatus'] != 5:
                        self.fail("Fail to reserve both dose for patient")

                    
                    sqlQuery = '''
                               SELECT CaregiverSlotSchedulingId
                               FROM VaccineAppointments
                               WHERE PatientId = 1 and VaccineName= 'Pfizer'
                               '''

                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 2:
                        self.fail("Fail to create two appointment entries of Appoint table")

                    if rows != [{'CaregiverSlotSchedulingId': 1}, {'CaregiverSlotSchedulingId': 33}]:
                        self.fail("Fail to assign correct slot id")

                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Scheduling Appointment failed with some exception")



if __name__ == '__main__':
    unittest.main()
