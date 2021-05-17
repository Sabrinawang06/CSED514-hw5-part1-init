from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the Vaccine inventory to the DB '''
    def __init__(self, vname, second, days, cursor):
        """
        Parameter: 
        vname: Vaccine Name (str)
        second: 2 for vaccines requires a second shot and 1 for one shot vaccine (int)
        days: the number of days between two shots for two-shot vaccine, 0 for one shot vaccine (int)
        """

        self.vname = vname
        self.second = second
        self.days = days

        self.sqltext = "INSERT INTO Vaccines (VaccineName, DosesPerPatient, DaysBetweenDoses) VALUES ({},{},{})".format("'"+ self.vname +"'",self.second, self.days)

        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()

            # cursor.connection.commit()
            print('Query executed successfully. Vaccine  {}'.format(self.vname))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Caregivers! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            cursor.connection.rollback()

    def CheckDose(self, cursor):
        ''' Method that check avaliable doses
        '''

        self.checkDose = "SELECT AvailableDoses FROM Vaccines  WHERE VaccineName = {}".format("'"+ self.vname +"'")

        try:
            cursor.execute(self.checkDose)
            rows = cursor.fetchone()
            current_num = rows['AvailableDoses']
            cursor.connection.commit()
            
            return current_num

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))           
            cursor.connection.rollback()
            return -1

    def AddDose(self, num, cursor):
        ''' Method that add a given amount of vaccine doses to a certain vaccine
        Parameter: 
        num: number add to the total doses and avaliable doses (int)
        '''

        self.addDoseSQL = "UPDATE Vaccines SET AvailableDoses = AvailableDoses + {}, TotalDoses = TotalDoses + {} WHERE VaccineName = {}".format(num, num,"'"+ self.vname +"'")

        try:
            cursor.execute(self.addDoseSQL)
            current_num = self.CheckDose(cursor)

            # If the current_num is not updated, indicates a wrong VaccineName
            # if current_num == -1:
            #     print('No research result in the inventory. Please check your VaccineName')
            #     return 'Wrong Id'

            print("Vaccine: {} has {} in the inventory".format(self.vname,current_num))
        
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))           
            cursor.connection.rollback()
            return -1


    def ReserveDoses(self, cursor):
        '''increment to the ReservedDoses to a given vaccine'''

        self.checkSecond = "SELECT DosesPerPatient FROM Vaccines  WHERE VaccineName = {}".format("'"+ self.vname +"'")

        self.reserve2DoseSQL = "UPDATE Vaccines SET ReservedDoses = ReservedDoses + 2  WHERE VaccineName = {}".format("'"+ self.vname +"'")
        self.deduct2DoseSQL = "UPDATE Vaccines SET AvailableDoses = AvailableDoses -2  WHERE VaccineName = {}".format("'"+ self.vname +"'")
        self.reserveDoseSQL = "UPDATE Vaccines SET ReservedDoses = ReservedDoses + 1  WHERE VaccineName = {}".format("'"+ self.vname +"'")
        self.deductDoseSQL = "UPDATE Vaccines SET AvailableDoses = AvailableDoses -1  WHERE VaccineName = {}".format("'"+ self.vname +"'")
        try:
    
            cursor.execute(self.checkSecond)
            rows = cursor.fetchone()
            current_num = self.CheckDose(cursor)

            # if len(rows) ==0:
            #     # If the current_num is not updated, indicates a wrong VaccineName
            #     print('No research result in the inventory. Please check your VaccineName')
            #     return 'Wrong Id'

            # else: 


                # check if second doses is needed
            if rows['DosesPerPatient']==2: 

                # Add two to the reserve doses and subtract two from the total doeses if the total doses is greater or equal to two
                if current_num >=2:
                    cursor.execute(self.reserve2DoseSQL)
                    cursor.execute(self.deduct2DoseSQL)
                    cursor.connection.commit()

                    print("Vaccine "+str(self.vname)+' has been succesfully reserved')

                    return 0

                else:
                    print("Not enough vaccine left for vaccine " + str(self.vname))
                    return 'Not enough'
            
            else:
                
                # Add one to the reserve doses and subtract one from the total doeses if the total doses is greater or equal to one 
                if current_num >=1:
                    cursor.execute(self.reserveDoseSQL)
                    cursor.execute(self.deductDoseSQL)
                    cursor.connection.commit()

                    print("Vaccine "+str(self.vname)+' has been succesfully reserved')

                    return 0

                else:
                    print("Not enough vaccine left for vaccine " + str(self.vname))

                    return 'Not enough'

        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            cursor.connection.rollback()
            return -1