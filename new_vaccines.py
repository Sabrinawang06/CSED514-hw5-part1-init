from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the Vaccine inventory to the DB '''
    def __init__(self, vname, second, days, cursor):

        self.sqltext = "INSERT INTO Vaccines (VaccineName, DosesPerPatient, DaysBetweenDoses) VALUES ({},{},{})".format("'"+ vname +"'",second, days)

        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()

            # cursor.connection.commit()
            print('Query executed successfully. Vaccine  {}'.format(vname))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Caregivers! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            print("SQL text that resulted in an Error: " + self.sqltext)


    def AddDose(self, vname, num, cursor):
        ''' Method that add a given amount of vaccine doses to a certain vaccine'''

        self.addDoseSQL = "UPDATE Vaccines SET AvailableDoses = AvailableDoses + {}, TotalDoses = TotalDoses + {} WHERE VaccineName = {}".format(num, num,"'"+ vname +"'")
        self.checkDose = "SELECT AvailableDoses FROM Vaccines  WHERE VaccineName = {}".format("'"+ vname +"'")
        try:
            cursor.execute(self.addDoseSQL)
            cursor.execute(self.checkDose)
            rows = cursor.fetchall()
            current_num = -1

            for row in rows:
                current_num = (row['AvailableDoses'])
            cursor.connection.commit()

            # If the current_num is not updated, indicates a wrong VaccineName
            if current_num == -1:
                print('No research result in the inventory. Please check your VaccineName')
                return 'Wrong Id'

            else:
                print("Vaccine: {} has {} in the inventory".format(vname,current_num))
        
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))           
            print("SQL text that resulted in an Error: " + self.addDoseQL)
            cursor.connection.rollback()
            return -1

    def ReserveDoses(self, vname, cursor):
        '''increment to the ReservedDoses to a given vaccine'''

        self.checkSecond = "SELECT DosesPerPatient FROM Vaccines  WHERE VaccineName = {}".format("'"+ vname +"'")
        self.checkDose = "SELECT AvailableDoses FROM Vaccines  WHERE VaccineName = {}".format("'"+ vname +"'")
        self.reserve2DoseSQL = "UPDATE Vaccines SET ReservedDoses = ReservedDoses + 2  WHERE VaccineName = {}".format("'"+ vname +"'")
        self.deduct2DoseSQL = "UPDATE Vaccines SET AvailableDoses = AvailableDoses -2  WHERE VaccineName = {}".format("'"+ vname +"'")
        self.reserveDoseSQL = "UPDATE Vaccines SET ReservedDoses = ReservedDoses + 1  WHERE VaccineName = {}".format("'"+ vname +"'")
        self.deductDoseSQL = "UPDATE Vaccines SET AvailableDoses = AvailableDoses -1  WHERE VaccineName = {}".format("'"+ vname +"'")
        try:
            cursor.execute(self.checkSecond)
            rows = cursor.fetchall()

            if len(rows) ==0:
                # If the current_num is not updated, indicates a wrong VaccineName
                print('No research result in the inventory. Please check your VaccineName')
                return 'Wrong Id'

            else: 

                for row in rows:
                    # check if second doses is needed
                    if row['DosesPerPatient']==2: 

                        cursor.execute(self.checkDose)
                        rows = cursor.fetchall()
                        for row in rows:
                            current_num = (row['AvailableDoses'])

                        # Add two to the reserve doses and subtract two from the total doeses if the total doses is greater or equal to two
                        if current_num >=2:
                            cursor.execute(self.reserve2DoseSQL)
                            cursor.execute(self.deduct2DoseSQL)
                            cursor.connection.commit()

                            print("Vaccine "+str(vname)+' has been succesfully reserved')

                        else:
                            print("Not enough vaccine left for vaccine " + str(vname))
                            return 'Not enough'
                    
                    else:
                        
                        cursor.execute(self.checkDose)
                        rows = cursor.fetchall()
                        for row in rows:
                            current_num = (row['AvailableDoses'])
                        
                        # Add one to the reserve doses and subtract one from the total doeses if the total doses is greater or equal to one 
                        if current_num >=1:
                            cursor.execute(self.reserveDoseSQL)
                            cursor.execute(self.deductDoseSQL)
                            cursor.connection.commit()

                            print("Vaccine "+str(vname)+' has been succesfully reserved')

                        else:
                            print("Not enough vaccine left for vaccine " + str(vname))

                            return 'Not enough'

        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            return -1