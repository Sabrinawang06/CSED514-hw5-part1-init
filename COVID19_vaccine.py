from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the Vaccine inventory to the DB '''
    def __init__(self, vid, second, cursor):

        self.sqltext = "INSERT INTO Vaccines (VaccineId, SecondDose) VALUES ({},{})".format("'"+ vid +"'",second)

        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()

            # cursor.connection.commit()
            print('Query executed successfully. Vaccine  {}'.format(vid))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Caregivers! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            print("SQL text that resulted in an Error: " + self.sqltext)


    def AddDose(self, vid, num, cursor):
        ''' Method that add a given amount of vaccine doses to a certain vaccine'''

        self.addDoseSQL = "UPDATE Vaccines SET VacTotalDoses = VacTotalDoses + {} WHERE VaccineId = {}".format(num,"'"+ vid +"'")
        self.checkDose = "SELECT VacTotalDoses FROM Vaccines  WHERE VaccineId = {}".format("'"+ vid +"'")
        try:
            cursor.execute(self.addDoseSQL)
            cursor.execute(self.checkDose)
            rows = cursor.fetchall()
            current_num = -1

            for row in rows:
                current_num = (row['VacTotalDoses'])
            cursor.connection.commit()

            # If the current_num is not updated, indicates a wrong VaccineId
            if current_num == -1:
                print('No research result in the inventory. Please check your VaccineId')
                return 'Wrong Id'

            else:
                print("Vaccine: {} has {} in the inventory".format(vid,current_num))
        
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))           
            print("SQL text that resulted in an Error: " + self.addDoseQL)
            cursor.connection.rollback()
            return -1

    def ReserveDoses(self, vid, cursor):
        '''increment to the VacReserveDoses to a given vaccine'''

        self.checkSecond = "SELECT SecondDose FROM Vaccines  WHERE VaccineId = {}".format("'"+ vid +"'")
        self.checkDose = "SELECT VacTotalDoses FROM Vaccines  WHERE VaccineId = {}".format("'"+ vid +"'")
        self.reserve2DoseSQL = "UPDATE Vaccines SET VacReserveDoses = VacReserveDoses + 2  WHERE VaccineId = {}".format("'"+ vid +"'")
        self.deduct2DoseSQL = "UPDATE Vaccines SET VacTotalDoses = VacTotalDoses -2  WHERE VaccineId = {}".format("'"+ vid +"'")
        self.reserveDoseSQL = "UPDATE Vaccines SET VacReserveDoses = VacReserveDoses + 1  WHERE VaccineId = {}".format("'"+ vid +"'")
        self.deductDoseSQL = "UPDATE Vaccines SET VacTotalDoses = VacTotalDoses -1  WHERE VaccineId = {}".format("'"+ vid +"'")
        try:
            cursor.execute(self.checkSecond)
            rows = cursor.fetchall()

            if len(rows) ==0:
                # If the current_num is not updated, indicates a wrong VaccineId
                print('No research result in the inventory. Please check your VaccineId')
                return 'Wrong Id'

            for row in rows:
                # check if second doses is needed
                if row['SecondDose']: 

                    cursor.execute(self.checkDose)
                    rows = cursor.fetchall()
                    for row in rows:
                        current_num = (row['VacTotalDoses'])

                    # Add two to the reserve doses and subtract two from the total doeses if the total doses is greater or equal to two
                    if current_num >=2:
                        cursor.execute(self.reserve2DoseSQL)
                        cursor.execute(self.deduct2DoseSQL)
                        cursor.connection.commit()

                        print("Vaccine "+str(vid)+' has been succesfully reserved')

                    else:
                        print("Not enough vaccine left for vaccine " + str(vid))
                        return 'Not enough'
                   
                else:
                    
                    cursor.execute(self.checkDose)
                    rows = cursor.fetchall()
                    for row in rows:
                        current_num = (row['VacTotalDoses'])
                    
                    # Add one to the reserve doses and subtract one from the total doeses if the total doses is greater or equal to one 
                    if current_num >=1:
                        cursor.execute(self.reserveDoseSQL)
                        cursor.execute(self.deductDoseSQL)
                        cursor.connection.commit()

                        print("Vaccine "+str(vid)+' has been succesfully reserved')

                    else:
                        print("Not enough vaccine left for vaccine " + str(vid))

                        return 'Not enough'

        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            return -1