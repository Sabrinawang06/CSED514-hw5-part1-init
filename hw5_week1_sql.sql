CREATE PROCEDURE InitDataModel
AS

BEGIN

    BEGIN
        CREATE TABLE Vaccines (
            VaccineId VARCHAR(20) PRIMARY KEY,
            VacTotalDoses int DEFAULT 0,
            VacReserveDoses int DEFAULT 0, 
            SecondDose BIT
        );
    END;

    BEGIN
        CREATE TABLE Patients (
            PatientId int IDENTITY PRIMARY KEY,
            PatientName varchar(30),
            PatientDOB date
        );
    END;

    BEGIN
        CREATE TABLE Appointment (
            VaccineAppointmentId int IDENTITY PRIMARY KEY,
            PatientId int FOREIGN KEY (PatientId)
                    REFERENCES Patients(PatientId),
            VaccineId VARCHAR(20) FOREIGN KEY (VaccineId)
                    REFERENCES Vaccines(VaccineId)
        );
    END;

    BEGIN
        Create Table Caregivers(
            CaregiverId int IDENTITY PRIMARY KEY,
            CaregiverName varchar(50)
            );
    END;

    BEGIN
        Create Table AppointmentStatusCodes(
            StatusCodeId int PRIMARY KEY,
            StatusCode   varchar(30)
        );
    END;

    BEGIN
        INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
            VALUES (0, 'Open');
    END;

    BEGIN
        INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
            VALUES (1, 'OnHold');
    END;

    BEGIN
        INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
            VALUES (2, 'Scheduled');
    END;

    BEGIN
        INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
            VALUES (3, 'Completed');
    END;

    BEGIN
        INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
            VALUES (4, 'Missed');
    END;

    BEGIN

        Create Table CareGiverSchedule(
            CaregiverSlotSchedulingId int Identity PRIMARY KEY, 
            CaregiverId int DEFAULT 0 NOT NULL
                CONSTRAINT FK_CareGiverScheduleCaregiverId FOREIGN KEY (caregiverId)
                    REFERENCES Caregivers(CaregiverId),
            WorkDay date,
            SlotTime time,
            SlotHour int DEFAULT 0 NOT NULL,
            SlotMinute int DEFAULT 0 NOT NULL,
            SlotStatus int  DEFAULT 0 NOT NULL
                CONSTRAINT FK_CaregiverStatusCode FOREIGN KEY (SlotStatus) 
                    REFERENCES AppointmentStatusCodes(StatusCodeId),
            VaccineAppointmentId int DEFAULT 0 NOT NULL);
    END;

END;   

