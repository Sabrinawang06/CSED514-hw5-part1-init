import unittest
import os
from vaccine_reservation_scheduler import VaccineReservationScheduler

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as Vaccine
from vaccine_patient import VaccinePatient as patient

with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:
        # clear_tables(sqlClient)
        # vac = Vaccine('Pfizer', 2, 21, cursor)
        # #vac.CheckDose(cursor) 
        # vac.AddDose(4, cursor)




        # # vac2 = Vaccine('Jonthan', 1, 0, cursor) 
        # # vac2.AddDose(4, cursor)
        # # message = vac2.ReserveDoses(cursor)
        # # 

        # # sqlQuery = '''
        # #             SELECT *
        # #             FROM Vaccines
        # #             '''
        # # cursor.execute(sqlQuery)
        # # rows = cursor.fetchall()
        # # print(rows)

        # # clear the tables before testing


        # patient_a = patient('Jon Do', cursor = cursor)


        # # create a new VaccineCaregiver object
        # caregiver_a = VaccineCaregiver(name="Steve Ma",
        #                                 cursor=cursor)

        # #scheduler = VaccineReservationScheduler()
        # #scheduler.PutHoldOnAppointmentSlot(1,cursor=cursor)
        # # scheduler.PutHoldOnAppointmentSlot(2,cursor=cursor)
        # # scheduler.ScheduleAppointmentSlot(1,cursor = cursor)
        # # scheduler.ScheduleAppointmentSlot(3,cursor = cursor)

        # patient_a.ReserveAppointment(1,vac, cursor)

        # patient_a.ScheduleAppointment(cursor)


        # # sqlQuery = '''
        # #             SELECT WorkDay
        # #             FROM CareGiverSchedule
        # #             WHERE CaregiverSlotSchedulingId = 1
        # #             '''
        # # cursor.execute(sqlQuery)
        # # rows = cursor.fetchone()
        # # print(rows['WorkDay'])
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
