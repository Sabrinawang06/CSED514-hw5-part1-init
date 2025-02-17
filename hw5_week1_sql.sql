/* I have matched my Vaccine table to the SQL file provided in part 2, 
thus the creating table procedure is updated too 
I have uploaded a seperate group of file starting with "Old" which match up the orginal Schema*/

CREATE PROCEDURE InitDataModel
AS

Create Table Caregivers(
	CaregiverId int IDENTITY PRIMARY KEY,
	CaregiverName varchar(50)
	);

Create Table AppointmentStatusCodes(
	StatusCodeId int PRIMARY KEY,
	StatusCode   varchar(30)
);


INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (0, 'Open');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (1, 'OnHold');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (2, 'Scheduled');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (3, 'Completed');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (4, 'Missed');

Create Table PatientAppointmentStatusCodes(
	StatusCodeId int PRIMARY KEY,
	StatusCode   varchar(30)
);


INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (0, 'New');
INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (1, 'Queued for 1st Dose');
INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (2, '1st Dose Scheduled');
INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (3, '1st Dose Administered');
INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (4, 'Queued for 2nd Dose');
INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (5, '2nd Dose Scheduled');
INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (6, '2nd Dose Administered');
INSERT INTO PatientAppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (7, 'Vaccination Complete');

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



Create Table Patients(
	PatientId int IDENTITY PRIMARY KEY,
	PatientName varchar(50),
	VaccineStatus int NOT NULL
		CONSTRAINT FK_PatientStatusCode FOREIGN KEY (VaccineStatus) 
		     REFERENCES PatientAppointmentStatusCodes(StatusCodeId),

	);

Create Table Vaccines(
		VaccineName  varchar(50) PRIMARY KEY,
		VaccineSupplier  varchar(50) ,
		AvailableDoses int DEFAULT 0,
		ReservedDoses int DEFAULT 0,
		TotalDoses int DEFAULT 0,
		DosesPerPatient int DEFAULT 0,
		DaysBetweenDoses int DEFAULT 0

	);



Create Table VaccineAppointments(
 		VaccineAppointmentId int Identity PRIMARY Key, 
		VaccineName varchar(50) 
            CONSTRAINT FK_VaccineAppointmentVaccineName FOREIGN KEY (VaccineName)
			REFERENCES Vaccines(VaccineName), 
		PatientId int
			CONSTRAINT FK_VaccineAppointmentPatientID FOREIGN KEY (PatientId)
			REFERENCES Patients(PatientId),
		CaregiverSlotSchedulingId int
			CONSTRAINT FK_VaccineAppointmentCaregiverSlotSchedulingId FOREIGN KEY (CaregiverSlotSchedulingId)
			REFERENCES CareGiverSchedule(CaregiverSlotSchedulingId),
		ReservationDate date,
		ReservationStartHour int,
		ReservationStartMinute int,
		AppointmentDuration int, 
		SlotStatus int DEFAULT 0 NOT NULL
			CONSTRAINT FK_VaccineAppointStatusCode FOREIGN KEY (slotStatus) 
			REFERENCES AppointmentStatusCodes(statusCodeId), 
		DateAdministered datetime,
		DoseNumber int
);
