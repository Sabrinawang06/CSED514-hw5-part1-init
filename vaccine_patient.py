from datetime import datetime
from datetime import timedelta
import pymssql
from vaccine_reservation_scheduler import VaccineReservationScheduler


class VaccinePatient:
    ''' Adds the Vaccine inventory to the DB '''
    def __init__(self, pname, cursor):
        self.VaccinStatus = 0
        self.sqltext = """INSERT INTO Patients (PatientName, VaccineStatus) 
        VALUES ({},{})""".format("'"+ pname +"'",self.VaccinStatus)

        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()

            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.pid = _identityRow['Identity']

            # cursor.connection.commit()
            print('Patient {} has been successfully added to the database with PatientId = {}'.format(pname, self.pid))

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Caregivers! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            cursor.connection.rollback()


    def ReserveAppointment(self, schedulingId, Vaccine, cursor):

        self.Vaccine = Vaccine
        self.slotSchedulingId = schedulingId
        self.scheduler = VaccineReservationScheduler()
        self.VaccineName = Vaccine.vname
        self.DosesPerPatient = Vaccine.second
        self.DaysBetweenDoses = Vaccine.days
        
        
        try:

            self.getCurrentDate = """
            SELECT CONVERT(date, getdate()) AS D"""

            cursor.execute(self.getCurrentDate)
            rows = cursor.fetchone()
            self.curent_date = rows['D']


            self.getPatientStatus = """
            SELECT VaccineStatus
            FROM Patients
            WHERE PatientId = {}
            """.format(self.pid)

            cursor.execute(self.getPatientStatus)
            rows = cursor.fetchone()
            self.VaccinStatus = rows['VaccineStatus']


            self.updatePatientOne  = """
                        UPDATE Patients
                        SET VaccineStatus = 1
                        WHERE PatientId = {}
                        """.format(self.pid)  
            
            self.getFirstDate = """
                        select *
                        from CaregiverSchedule
                        WHERE CaregiverSlotSchedulingId = {}
                        """.format(self.slotSchedulingId)
         

            # Get the current status of that slot 
            current_status = self.scheduler.CheckStatus(self.slotSchedulingId, cursor)
            
            
            # If current_status is None, break the function and return -1 

            if current_status == None:
                return -1

            else: 

                # Check if the vaccine if two doese vaccine and if the patient is a new patient 

                if self.DosesPerPatient == 2 and self.VaccinStatus == 0:
                    
                    # Check if the status of the slot if 'Open'
                    if current_status == 0 :
                        if self.Vaccine.CheckDose(cursor) >= 2:
                            
                            # Get the date of the first appointment 
                            cursor.execute(self.getFirstDate)
                            rows = cursor.fetchone()
                            self.firstdate = rows['WorkDay']
                            self.firstHour = rows['SlotHour']
                            self.firstMin = rows['SlotMinute']

                            self.insertVacAppt = """
                            INSERT INTO VaccineAppointments (CaregiverSlotSchedulingId, PatientId, VaccineName,
                            ReservationDate, ReservationStartHour, ReservationStartMinute, 
                            AppointmentDuration, SlotStatus, DoseNumber) 
                            VALUES ({},{},{},{},{},{},{},{},{})""".format(self.slotSchedulingId, self.pid,"'"+ self.VaccineName +"'", 
                                                            "'"+ self.firstdate +"'", self.firstHour, self.firstMin, 
                                                            15, 1, 1)

                            self.findSecondSlot = """
                            select TOP 1 * 
                            from CaregiverSchedule
                            WHERE DATEDIFF(day, {}, WorkDay) > 21 
                            AND DATEDIFF(day, {}, WorkDay) < 42
                            AND SlotStatus = 0 
                            """.format("'"+ self.firstdate +"'", "'"+ self.firstdate +"'")

                            # Get the information for the second slot given the first slot date
                            cursor.execute(self.findSecondSlot)
                            row = cursor.fetchone()
                            self.secondslotId = row['CaregiverSlotSchedulingId']
                            self.secondDate = row['WorkDay']
                            self.secondHour = row['SlotHour']
                            self.secondMin = row['SlotMinute']

                            

                            self.scheduleSecond = """
                            INSERT INTO VaccineAppointments 
                            (CaregiverSlotSchedulingId, PatientId, VaccineName,
                            ReservationDate, ReservationStartHour, ReservationStartMinute, 
                            AppointmentDuration, SlotStatus, DoseNumber) 
                            VALUES ({},{},{},{},{},{},{},{},{})""".format(self.secondslotId, self.pid,
                                                         "'"+ self.VaccineName +"'", "'"+ self.secondDate +"'",
                                                         self.secondHour,self.secondMin, 15, 1, 2)
                            
                            self.updatePatientSecond  = """
                            UPDATE Patients
                            SET VaccineStatus = 4
                            WHERE PatientId = {}
                            """.format(self.pid)
                        

                            # Mark the first slot on hold 

                            self.scheduler.PutHoldOnAppointmentSlot(schedulingId,cursor=cursor)

                            # Mark the second slot on Hold
                            self.scheduler.PutHoldOnAppointmentSlot(self.secondslotId,cursor=cursor)

                            # Reserver the two doese
                            Vaccine.ReserveDoses(cursor)

                            # Insert the appoiontment and update patient status 
                            cursor.execute(self.insertVacAppt)
                            cursor.execute(self.updatePatientOne)
                            cursor.execute(self.scheduleSecond)
                            cursor.execute(self.updatePatientSecond)
                            cursor.connection.commit()

                            print('Two apppintmemnts for vaccine {} is researved at {},{}:{} amd {},{}:{}'.format(self.VaccineName, 
                            self.firstdate, self.firstHour, self.firstMin, self.secondDate, self.secondHour, self.secondMin))

            
                        else:
                            print ("Not enough avaliable doses for scheduling both shot, please check back later")
                    else:
                        print("Given slot not on open")

                elif self.DosesPerPatient == 1 and self.VaccinStatus == 0:
                    if current_status == 0 :
                        if self.Vaccine.CheckDose(cursor) >= 1:

                            cursor.execute(self.getFirstDate)
                            rows = cursor.fetchone()
                            self.firstdate = rows['WorkDay']
                            self.firstHour = rows['SlotHour']
                            self.firstMin = rows['SlotMinute']
                            
                            self.insertVacAppt = """
                            INSERT INTO VaccineAppointments (CaregiverSlotSchedulingId, PatientId, VaccineName,
                            ReservationDate, ReservationStartHour, ReservationStartMinute, 
                            AppointmentDuration, SlotStatus, DoseNumber) 
                            VALUES ({},{},{},{},{},{},{},{},{})""".format(self.slotSchedulingId, self.pid,"'"+ self.VaccineName +"'", 
                                                            "'"+ self.firstdate +"'", self.firstHour, self.firstMin, 
                                                            15, 1, 1)

                            self.scheduler.PutHoldOnAppointmentSlot(schedulingId,cursor=cursor)
                            Vaccine.ReserveDoses(cursor)
                            cursor.execute(self.insertVacAppt)
                            cursor.execute(self.updatePatientOne)
                            cursor.connection.commit()

                        else:
                            print("Not enough avaliable vaccine")
                    else:
                        print("Given slot not open")

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])           
            cursor.connection.rollback()
            return -1

    def ScheduleAppointment(self, cursor):

        self.scheduler = VaccineReservationScheduler()

        try:

            self.getStatus = """
            SELECT C.SlotStatus
            FROM CareGiverSchedule as C
            JOIN VaccineAppointments as VA on C.CaregiverSlotSchedulingId = VA.CaregiverSlotSchedulingId   
            WHERE VA.PatientId = {}
            """.format(self.pid)

            current_status = []

            cursor.execute(self.getStatus)
            rows = cursor.fetchall()
            for row in rows:
                current_status.append(row['SlotStatus'])
            


            if current_status == []:
                print("No slot has reserved yet. Please reserve your appointment first")

            else:

                self.updateSlotStauts = """
                UPDATE CareGiverSchedule 
                SET CareGiverSchedule.SlotStatus = 2
                FROM CareGiverSchedule as C
                JOIN VaccineAppointments as VA on C.CaregiverSlotSchedulingId = VA.CaregiverSlotSchedulingId   
                WHERE VA.PatientId = {}
                """.format(self.pid)

                self.updateAppointment = """
                UPDATE VaccineAppointments
                SET SlotStatus = 2
                WHERE PatientId = {}
                """.format(self.pid)

                
                self.updatePatientOne = """
                UPDATE Patients
                SET VaccineStatus = 2
                WHERE PatientId ={}
                """.format(self.pid)

                self.updatePatientTwo = """
                UPDATE Patients
                SET VaccineStatus = 5
                WHERE PatientId = {}
                """.format(self.pid)

                if len(current_status)==2:

                    cursor.execute(self.updateSlotStauts)
                    cursor.execute(self.updateAppointment)
                    cursor.execute(self.updatePatientTwo)
                    cursor.connection.commit()

                    print('Two appoints successfully scheduled')
                else:
                    cursor.execute(self.updateSlotStauts)
                    cursor.execute(self.updateAppointment)
                    cursor.execute(self.updatePatientOne)
                    cursor.connection.commit()

                    print('One appoints successfully scheduled')

        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            cursor.connection.rollback()
            return -1