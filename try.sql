-- select TOP 1 * 
-- from CaregiverSchedule
-- WHERE DATEDIFF(day, '2021-5-14', WorkDay) > 21 
--       AND DATEDIFF(day, '2021-5-14', WorkDay) < 42
-- --       AND SlotStatus = 0 


SELECT *
FROM Patients;

select *
from vaccines;

select * 
from VaccineAppointments;

select * 
from CareGiverSchedule;

