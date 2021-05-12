def clear_tables(client):
    sqlQuery = '''
               DELETE From CareGiverSchedule
               DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 0)
               Delete From Caregivers
               DBCC CHECKIDENT ('Caregivers', RESEED, 0)
               DELETE FROM Vaccines
               '''
    client.cursor().execute(sqlQuery)
    client.commit()
