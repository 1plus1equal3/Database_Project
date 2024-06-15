DROP PROCEDURE dbo.GetClassInfo;
GO;
-- GET A CLASS'S INFORMATION
CREATE PROCEDURE GetClassInfo
    @teacherID INT,
    @classID INT
AS
BEGIN
    SET NOCOUNT ON
    -- Query to get student information and their average score
    SELECT 
        ui.user_id, 
        ui.username, 
        AVG(ch.score) AS avg_score
    INTO #StudentInfo
    FROM dbo.User_info ui, dbo.Class_history ch, dbo.Class_user cu
	WHERE cu.class_id = @classID
	AND cu.user_id = ui.user_id
	AND ch.user_id = ui.user_id
    GROUP BY ui.user_id, ui.username

    -- Number of students
    DECLARE @num_students INT
    SELECT @num_students = COUNT(*) FROM #StudentInfo

    -- Number of tests
    DECLARE @num_tests INT
    SELECT @num_tests = COUNT(*)
    FROM dbo.Class_test ct 
    WHERE ct.class_id = @classID

    -- Output the results
    SELECT @num_students AS number_of_students, @num_tests AS number_of_tests
    SELECT * FROM #StudentInfo

    -- Cleanup temporary table
    DROP TABLE #StudentInfo
END;
GO;

--Get info of a class
EXEC dbo.GetClassInfo 13, 2
GO;


-- GET TEST RESULTS
CREATE PROCEDURE GetTestResults
    @userID INT = NULL,
    @testID INT = NULL,
    @classID INT
AS
BEGIN
    -- Scenario 1: Both userID and testID are provided
    IF @userID IS NOT NULL AND @testID IS NOT NULL
    BEGIN
        SELECT ch.user_id, ch.test_id, ch.score, ch.finish_time
        FROM dbo.Class_history ch
        WHERE ch.user_id = @userID AND ch.test_id = @testID AND ch.class_id = @classID;
    END
    -- Scenario 2: Only userID is provided
    ELSE IF @userID IS NOT NULL AND @testID IS NULL
    BEGIN
        SELECT ch.user_id, ch.test_id, ch.score, ch.finish_time
        FROM dbo.Class_history ch
        WHERE ch.user_id = @userID AND ch.class_id = @classID;
    END
    -- Scenario 3: Only testID is provided
    ELSE IF @userID IS NULL AND @testID IS NOT NULL
    BEGIN
        SELECT ch.user_id, ch.test_id, ch.score, ch.finish_time
        FROM dbo.Class_history ch
        WHERE ch.test_id = @testID AND ch.class_id = @classID;
    END
    -- Scenario 4: Neither userID nor testID is provided
    ELSE
    BEGIN
        SELECT user_id, test_id, score, finish_time
        FROM dbo.Class_history;
    END
END




-- ADD STUDENT TO CLASS---
DROP PROCEDURE addStudentToClass
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE addStudentToClass
	@classId INT, @studentId INT
AS
BEGIN
SET NOCOUNT ON
--Check if the student existed
IF NOT EXISTS (SELECT user_id FROM User_info WHERE user_id = @studentId)
	BEGIN
		--PRINT 'This student is not exist'
		SELECT -1;
	END;
ELSE
	BEGIN
        --Check if the class existed
		IF NOT EXISTS (SELECT class_id FROM Class WHERE class_id = @classId)
			BEGIN
				--PRINT 'This class is not exist'
				SELECT -1;
			END;
		ELSE
			BEGIN
			    --Check if this student was in this class
				IF NOT EXISTS (SELECT 1 FROM Class_user WHERE class_id = @classId AND user_id = @studentId)
					BEGIN
						INSERT INTO Class_user(class_id, user_id) VALUES (@classId, @studentId);
						SELECT  1;
					END;
				ELSE
					BEGIN
						--PRINT 'This student existed in this class';
						SELECT -1;
					END;
			END;
	END;
END;

--Test add student to class
EXEC dbo.addStudentToClass 2, 20;
--See students in class
Select * From Class_user;
GO;

--DELETE STUDENT FROM CLASS
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE deleteStudentFromClass @classId INT, @studentId INT
AS
BEGIN
SET NOCOUNT ON
--Check if the student existed
IF NOT EXISTS (SELECT user_id FROM User_info WHERE user_id = @studentId)
	BEGIN
		--PRINT 'This student is not exist'
		SELECT -1;
	END;
ELSE
	BEGIN
        --Check if the class existed
		IF NOT EXISTS (SELECT class_id FROM Class WHERE class_id = @classId)
			BEGIN
				--PRINT 'This class is not exist'
				SELECT -1;
			END;
		ELSE
			BEGIN
			    --Check if this student was in this class
				IF NOT EXISTS (SELECT 1 FROM Class_user WHERE class_id = @classId AND user_id = @studentId)
					BEGIN
						-- PRINT 'This student is not in this class';
						SELECT -1;
					END;
				ELSE
					BEGIN
                        DELETE FROM Class_user WHERE class_id = @classId AND user_id = @studentId;
						SELECT  1;
					END;
			END;
	END;
END;
GO;

-----------------------------------------------
---TRIGGER UPDATE NUMBER OF STUDENT IN CLASS---
-----------------------------------------------
CREATE TRIGGER updateNumStudent ON Class_user FOR INSERT
AS
BEGIN
	UPDATE Class 
	SET number_student = number_student + 1
	FROM Class, inserted WHERE Class.class_id = inserted.class_id
END
GO;


----------------------------
---TRIGGER DELETE STUDENT---
----------------------------
CREATE TRIGGER decreaseNumStudent ON Class_user FOR DELETE
AS
BEGIN
	UPDATE Class 
	SET number_student = number_student - 1
	FROM Class, deleted WHERE Class.class_id = deleted.class_id
END
GO;
--------------------------------------------------------
---CHECCK DATE OFF THE CURRENT TEST BEFORE ADDING NEW---
--------------------------------------------------------
create function checkDate(@classId int)
returns int
as
begin
	declare @duration int;
	declare @startTime datetime;
	declare @currentTime datetime = GETDATE();

	select @duration = Duration from (select top 1* from Class_test where class_id = @classId order by addTime desc)
	as dur
	select @startTime = addTime from (select top 1* from Class_test where class_id = @classId order by addTime desc)
	as st
	return datediff(minute, @startTime, @currentTime) - @duration
end
GO;
-----------------------
---ADD TEST TO CLASS---
-----------------------
create procedure addTestToClass
	@testId int, @classId int, @duration int
as
begin
    declare @valid int
    ---Check if the test exist
	if not exists(select test_id from Test where test_id = @testId)
		begin
			--print 'This test is not exist'
			select -1
		end;
	else
		begin
		    ---Check if the class exist
			if not exists (select class_id from Class where class_id = @classId)
				begin
					--print 'This class is not exist'
					select -1
                end;
			else
				begin
					---Check if the test was in class
					if not exists (select 1 from Class_test where class_id = @classId and test_id = @testId)
						begin
							select @valid = dbo.checkDate(@classId)
							if @valid > 0
							begin 
								insert into Class_test(class_id, test_id, Duration, addTime) values (@classId, @testId, @duration, GETDATE())
								select 1
							end
							else
							begin
								--print 'The another test is in force'
								select -2
							end
						end
					else
						begin
							--print 'This test had been added'
							select -3
						end
				end
			end
		end
GO;						
--------------------------------
---STUDENT TAKE TEST IN CLASS---
--------------------------------

create procedure takeTestInClass(@classId int)
as
begin
    declare @isValid int;
	select @isValid = dbo.checkDate(@classId)
	if @isValid < 0
		begin
		print 'Out of time of this test'
		return -1
		end
	else
		select top 1 test_id from Class_test where class_id = @classId order by addTime desc
end
GO;
---------------------------------
---SEE RESULT OF TEST IN CLASS---
---------------------------------
create procedure seeTestResult
@classId int, @testId int
as
begin 
if not exists (select 1 from Class_history where class_id = @classId and test_id = @testId)
	begin
	print 'This test is not in this class'
	return -1
	end
else
begin
select * from Class_history where class_id = @classId and test_id = @testId
end
end
GO;
------------------------------------
---SEE RESULT OF STUDENT IN CLASS---
------------------------------------
create procedure seeStudentResult
@classId int, @studentId int
as
begin 
if not exists (select 1 from Class_history where class_id = @classId and user_id = @studentId)
	begin
	print 'This student is not in this class'
	return -1
	end
else
begin
select * from Class_history where class_id = @classId and user_id = @studentId
end
end
GO;



drop procedure takeTestInClass

insert into Class(class_id, teacher_id, class_name, number_student, create_date) values (3, 1, 'Mid_term2', 0, GETDATE())

insert into Class_test(class_id, test_id, Duration, addTime) values (3, 15, 10, GETDATE())

select top 1 Duration from Class_test where class_id = 3 order by addTime desc

exec addTestToClass @testId = 19, @classId = 1, @duration = 20

exec takeTestInClass @classId = 1 

select top 1 test_id from Class_test where class_id = 3 order by addTime desc


---Tạo thêm 1 table mới để lưu history trong lớp học, không sửa bảng history cũ vì sẽ liên quan đến code Python---

create table Class_history(
class_id int,
user_id int,
test_id int,
finish_time datetime,
primary key(class_id, user_id, test_id)
)