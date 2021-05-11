/*

CREATE TABLE Patients (
    PatientId int IDENTITY PRIMARY KEY,
    PatientName varchar(30),
    PatientDOB date
);


CREATE TABLE Vaccines (
    VaccineId int  PRIMARY KEY,
    VaccineName VARCHAR(30),
    VacTotalDoses int DEFAULT 0,
    VacReserveDoses int DEFAULT 0, 
    SecondDose BIT
);




CREATE TABLE Appointment (
    VaccineAppointmentId int IDENTITY PRIMARY KEY,
    PatientId int FOREIGN KEY (PatientId)
            REFERENCES Patients(PatientId),
    VaccineId int FOREIGN KEY (VaccineId)
            REFERENCES Vaccines(VaccineId)
)


DROP TABLE Appointment
DROP TABLE Vaccines
*/

---INSERT INTO Vaccines (VaccineId, VaccineName, SecondDose) VALUES(1,'Pfizer',1)
---SELECT * FROM Vaccines




-- UPDATE Vaccines 
-- SET VacTotalDoses = SUM(VacTotalDoses,1)
-- WHERE VaccineId = 1;

-- Drop Table Caregivers
-- Drop Table CareGiverSchedule

-- Drop Table AppointmentStatusCodes
-- DROP TABLE Appointment
-- DROP TABLE Patients
-- Drop Table Vaccines



-- DROP PROCEDURE initDataModel;  
-- GO  

EXEC initDataModel;
GO


