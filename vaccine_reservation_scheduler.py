import datetime
from enum import IntEnum
import os
import pymssql
import traceback

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
# from covid19_vaccine import COVID19Vaccine as covid
# from vaccine_patient import VaccinePatient as patient


class VaccineReservationScheduler:

    def __init__(self):
        return

    def CheckStatus(self, slotid, cursor):
        self.slotSchedulingId = slotid
        self.getAppointmentSQL = "SELECT SlotStatus FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = {}".format(slotid)

        try:
            cursor.execute(self.getAppointmentSQL)
            row = cursor.fetchone()
            current_status = row['SlotStatus']
              

            return current_status

        except TypeError:
            print('Input slot id is invalid')
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])           
            cursor.connection.rollback()
            return -1

    def PutHoldOnAppointmentSlot(self, slotid, cursor):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Parameter:
        slotid: CaregiverSlotSchedulingId int 
         '''
        # Note to students: this is a stub that needs to replaced with your code
        self.slotSchedulingId = slotid
        self.getAppointmentSQL = "SELECT SlotStatus FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = {}".format(slotid)
        self.setOnHold =  "UPDATE CareGiverSchedule SET SlotStatus = 1 WHERE CaregiverSlotSchedulingId = {}".format(slotid)
        try:
            cursor.execute(self.getAppointmentSQL)
            rows = cursor.fetchall()
            current_status = -1
            message = ''
            for row in rows:
                current_status = row['SlotStatus']
            
            if current_status == -1:
                message = "Wrong Slot ID"
                print("Incorrect Slot ID; please check your input ID")
            elif current_status == 0:
                cursor.execute(self.setOnHold)
                cursor.connection.commit()
                print("Slot {} has been successfully set on hold".format(slotid))
            else: 
                message = 'Slot not free'
                print('Given slot is not free')
                cursor.connection. rollback() 

            return message
        
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])           

            cursor.connection.rollback()
            return -1

    def ScheduleAppointmentSlot(self, slotid, cursor):
        '''method that marks a slot on Hold with a definite reservation  
        slotid is the slot that is currently on Hold and whose status will be updated 
        returns the same slotid when the database update succeeds 
        returns 0 is there if the database update dails 
        returns -1 the same slotid when the database command fails
        returns 21 if the slotid parm is invalid '''
        # Note to students: this is a stub that needs to replaced with your code

        self.slotSchedulingId = slotid
        self.getAppointmentSQL = "SELECT SlotStatus FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = {}".format(slotid)
        self.setOnHold =  "UPDATE CareGiverSchedule SET SlotStatus = 2 WHERE CaregiverSlotSchedulingId = {}".format(slotid)
        try:
            cursor.execute(self.getAppointmentSQL)
            rows = cursor.fetchall()
            current_status = -1
            message = ''
            for row in rows:
                current_status = row['SlotStatus']
            
            if current_status == -1:
                message = "Wrong Slot ID"
                print("Incorrect Slot ID; please check your input ID")
            elif current_status == 1:
                cursor.execute(self.setOnHold)
                cursor.connection.commit()
                print("Slot {} has been successfully set on hold".format(slotid))
            else: 
                message = 'Slot not on hold'
                print('Given slot is not on hold')
                cursor.connection. rollback() 

            return message
            
        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            cursor.connection.rollback()
            return -1

if __name__ == '__main__':
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            clear_tables(sqlClient)
            vrs = VaccineReservationScheduler()

            # get a cursor from the SQL connection
            dbcursor = sqlClient.cursor(as_dict=True)

            # Iniialize the caregivers, patients & vaccine supply
            caregiversList = []
            caregiversList.append(VaccineCaregiver('Carrie Nation', dbcursor))
            caregiversList.append(VaccineCaregiver('Clare Barton', dbcursor))
            caregivers = {}
            for cg in caregiversList:
                cgid = cg.caregiverId
                caregivers[cgid] = cg

            # Add a vaccine and Add doses to inventory of the vaccine
            # Ass patients
            # Schedule the patients
            
            # Test cases done!
            clear_tables(sqlClient)
