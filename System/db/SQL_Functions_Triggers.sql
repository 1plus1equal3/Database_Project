-- Login/Sign up function

--Login function
DROP FUNCTION dbo.func_login;
GO;

CREATE FUNCTION func_login
(@u_name nvarchar(255), @u_pass nvarchar(255))
RETURNS INT
AS
BEGIN
DECLARE @u_id INT;
SELECT @u_id = user_id FROM User_info WHERE username = @u_name AND user_password = @u_pass;
IF @u_id IS NOT NULL
RETURN @u_id;
RETURN -1;
END;
GO;

--Test function
SELECT dbo.func_login('Nguyen Dang Duy', 'aothatday123');
GO;

-- Check privilege
DROP FUNCTION dbo.checkUserRole;
GO;

CREATE FUNCTION checkUserRole
(@user_id INT)
RETURNS INT
AS
BEGIN
DECLARE @u_role INT;
SELECT @u_role = user_type FROM User_info WHERE user_id = @user_id;
RETURN @u_role
END
GO;

--Test check role
select dbo.checkUserRole(1);

--Sign up store_procedure
DROP PROC func_register;
GO;

CREATE PROC func_register 
(@u_name nvarchar(255), @u_pass nvarchar(255), @email nvarchar(255))
AS
BEGIN
DECLARE @name INT;
SELECT @name = COUNT(username) FROM User_info WHERE username = @u_name;
IF @name <> 0 --If not return -1
BEGIN
SELECT -1
RETURN
END
ELSE --Else insert and return 0
BEGIN
INSERT INTO User_info(username, user_password, email, user_type)
VALUES (@u_name, @u_pass, @email, 0);
COMMIT
SELECT 1
RETURN
END
END
GO;

--Test register
EXEC func_register 'test', 'test', 'test@gmail.com';
SELECT * FROM User_info;
GO;

-- @@@@ User function
-- Load user_info
DROP PROC getUserInfo;
GO;

CREATE PROC getUserInfo
(@user_id INT)
AS
BEGIN
	SELECT * FROM User_info WHERE user_id = @user_id;
END
GO;

-- Test get user info
EXEC getUserInfo @user_id = 6;
GO;
 
-- Load dashboard with random exam
DROP VIEW request_exam_list;
GO;

CREATE VIEW request_exam_list
AS SELECT TOP 10 * FROM Test
ORDER BY NEWID();
GO;

DROP FUNCTION dbo.request_exam;
GO;

CREATE FUNCTION request_exam()
RETURNS TABLE
AS
RETURN SELECT * FROM request_exam_list;
GO;

--Test request_exam
SELECT * FROM dbo.request_exam();
GO;

--Error
CREATE FUNCTION request_exam_1()
RETURNS TABLE
AS
RETURN (SELECT TOP 10 * FROM Test
ORDER BY NEWID());
GO;

-- Query exam created by admin
DROP FUNCTION dbo.request_admin_exam;
GO;

CREATE FUNCTION request_admin_exam(@admin_id INT)
RETURNS TABLE
AS
RETURN SELECT * FROM Test WHERE admin_id = @admin_id;
GO;

-- Test query exam by admin id
SELECT * FROM User_info;
SELECT * FROM dbo.request_admin_exam(13);
GO;


-- Get question id and question content
DROP PROC GetTestQuestions;
GO;

CREATE PROCEDURE GetTestQuestions
(@TestID INT)
AS
BEGIN
    SELECT Q.question_id, Q.question_content
    FROM Test_question T, Question Q 
    WHERE test_id = @TestID
    AND Q.question_id = T.question_id;
END;
GO;

-- Test get questions
EXEC GetTestQuestions @TestID = 7;
GO;

-- Get question option procedure
DROP PROC GetAnswerText;
GO;

CREATE PROCEDURE GetAnswerText
(@question_ID VARCHAR(50))
AS
BEGIN
    SELECT answer_content
    FROM Answer
    WHERE question_id = @question_ID
END;
GO;

--Test GetAnswerText procedure
EXEC GetAnswerText @question_ID = "ed2a9e8e-66a7-4090-84f1-21d823db1ade";
GO;

--Get correct answer function
DROP FUNCTION dbo.getCorrectAns;
GO;

CREATE FUNCTION getCorrectAns
(@question_id VARCHAR(50))
RETURNS CHAR
AS
BEGIN
DECLARE @opt CHAR
SELECT @opt=ans
FROM Question
WHERE question_id = @question_id
RETURN @opt
END
GO;

--Test getCorrectAns
SELECT dbo.getCorrectAns('ed2a9e8e-66a7-4090-84f1-21d823db1ade');
GO;

-- Insert History function
DROP PROC insertHistory;
GO;

CREATE PROC insertHistory
(@user_id INT, @test_id INT, @score FLOAT)
AS
BEGIN
	INSERT INTO History(user_id, test_id, score)
	VALUES (@user_id, @test_id, @score);
END
GO;

-- Test insert History
EXEC insertHistory @user_id = 5, @test_id = 10, @score = 8.8;
SELECT * FROM History;
GO;

-- Get user history
DROP FUNCTION dbo.request_user_history;
GO;

CREATE FUNCTION request_user_history
(@user_id INT)
RETURNS TABLE
AS
RETURN 
(SELECT h.*, t.title, t.admin_id FROM History h
JOIN Test t ON h.test_id = t.test_id
WHERE h.user_id = @user_id);
GO;

--Test request_user_history
SELECT * FROM User_info;
SELECT * FROM dbo.request_user_history(14);
GO;

-- Search Test by title
DROP PROC SearchTestTitle;
GO;

CREATE PROCEDURE SearchTestTitle
	@title varchar(255)
AS
BEGIN
	SELECT test_id, title, date_created, username FROM Test, User_info 
	WHERE title LIKE '%'+@title+'%' AND Test.admin_id = User_info.user_id
END;
GO;

--Test search by title
EXEC SearchTestTitle 'test';
GO;

-- Search Test by Id
DROP PROC SearchTestID;
GO;

CREATE PROCEDURE SearchTestID
	@TestID INT
AS
BEGIN
	SELECT test_id, title, date_created, username FROM Test, User_info 
	WHERE test_id = @TestID AND admin_id = user_id
END;
GO

--Test search by Id
EXEC SearchTestID 10;
GO;

-- Create random test
DROP PROC createTest;
GO;

CREATE PROC createTest(
@num_of_question INT, 
@title VARCHAR(255), 
@date DATE, 
@admin_id INT, 
@subject VARCHAR(30), 
@level INT
)
AS
BEGIN
DECLARE @test_id INT;
IF NOT EXISTS(SELECT title FROM Test WHERE title = @title)
BEGIN
	--Insert into Test
	INSERT INTO Test (title, date_created, admin_id, subject, difficulty_level)
	VALUES (@title, @date, @admin_id, @subject, @level);
	SET @test_id = SCOPE_IDENTITY();
	--Insert into Test_question
	IF (@subject) = 'Unknown'
	INSERT INTO Test_question
	SELECT TOP (@num_of_question) question_id, @test_id FROM Question
	WHERE level = @level ORDER BY NEWID();
	ELSE
	INSERT INTO Test_question
	SELECT TOP (@num_of_question) question_id, @test_id FROM Question
	WHERE subject = @subject AND level = @level ORDER BY NEWID();
	--Return 1
	SELECT @test_id;
END
ELSE
SELECT 0;
END;
GO;

--Test create Test
EXEC createTest 10, 'test_1', '2023-01-12', 1, "Unknown", 1;
GO;

--Delete Test
DROP PROC deleteTest;
GO;

CREATE PROC deleteTest
(@test_id INT)
AS
BEGIN
IF EXISTS(SELECT test_id FROM Test WHERE test_id = @test_id)
BEGIN
DELETE FROM Test_question WHERE test_id = @test_id;
DELETE FROM Test WHERE test_id = @test_id;
SELECT 'Delete test: successfully!'
END
ELSE
SELECT 'Delete test fail!'
END
GO;

--Test delete test
SELECT * FROM Test;
EXEC deleteTest 158;
GO;

-- Get User list
DROP FUNCTION dbo.userList;
GO;

CREATE FUNCTION userList()
RETURNS TABLE
AS
RETURN SELECT user_id, username, email FROM User_info WHERE user_type = 0;
GO;

--Test user list function
SELECT * FROM dbo.userList();
GO;

--Student statistics
DROP FUNCTION dbo.Statist;
GO;

CREATE FUNCTION Statist
(@used_id INT)
RETURNS TABLE
AS
RETURN (
SELECT COUNT (*) AS num_of_test, AVG(score) AS average_score, MAX(score) 
AS max_score, MIN(score) AS min_score
FROM History WHERE user_id = @used_id
);
GO;

--Search question by subject
DROP PROC SearchQuesSubject;
GO;

CREATE PROCEDURE SearchQuesSubject
	@subject varchar(255)
AS
BEGIN 
SELECT question_id, question_content 
FROM Question WHERE subject LIKE '%' + @subject + '%' 
END;
GO;

--Test search question by subject
EXEC SearchQuesSubject @subject = 'Medi';
GO;

--Search question by content
DROP PROC SearchQuesContent;
GO;

CREATE PROCEDURE SearchQuesContent
	@content varchar(255)
AS
BEGIN 
SELECT question_id, question_content 
FROM Question WHERE question_content LIKE '%' + @content + '%' 
END;
GO;

--Test search Question by content
EXEC SearchQuesContent @content = 'What';
GO;

--Search question
DROP PROC searchQuestion;
GO;

CREATE PROC searchQuestion
(@content VARCHAR(255), @subject VARCHAR(255), @level INT)
AS
BEGIN
IF (@subject) = 'Unknown'
SELECT TOP 20 * FROM Question
WHERE question_content LIKE '%' + @content + '%'
AND level = @level
ELSE
SELECT TOP 20 * FROM Question
WHERE question_content LIKE '%' + @content + '%'
AND level = @level
AND subject = @subject
END;
GO;

--Test search question
EXEC searchQuestion 'What', 'Skin', 1;
GO;

-- View classes belong to the teacher
CREATE PROCEDURE viewTeacherClasses(@teacherId INT)
AS
BEGIN
	IF NOT EXISTS (SELECT * FROM Class WHERE teacher_id = @teacherId)
		BEGIN
			PRINT 'You have no classes'
			SELECT -1
		END
	ELSE
		BEGIN
			SELECT * FROM Class WHERE teacher_id = @teacherId
		END
END;
GO;

--Test query class
EXEC viewTeacherClasses 13;
GO;

-- createNewClass
DROP PROC createClass;
GO;

CREATE PROCEDURE createClass(@teacherId INT, @className VARCHAR(50))
AS
BEGIN
SET NOCOUNT ON
	IF EXISTS (SELECT * FROM Class WHERE class_name = @className)
		BEGIN
			SELECT 0;
		END
	ELSE
		BEGIN
			INSERT INTO Class(teacher_id, class_name, number_student)
            VALUES (@teacherId, @className, 0);
			--COMMIT;
            SELECT 1;
		END
END;
GO;

--Test create new class
Select * from Class;
exec createClass @teacherId = 13, @className = 'class_06';
GO;

--Delete class
DROP PROCEDURE deleteClass;
GO;
CREATE PROCEDURE deleteClass @class_id INT
AS
BEGIN
SET NOCOUNT ON
	IF EXISTS (SELECT * FROM Class WHERE class_id=@class_id)
		BEGIN 
		DELETE FROM Class WHERE class_id = @class_id;
		SELECT 1;
		END;
	ELSE
		BEGIN
		SELECT 0;
		END;
END;
--Test delete class
Select * From Class;
EXEC dbo.deleteClass 15;
GO;

--Get Class info
--Get Student info in class
DROP PROC studentInfoClass;
GO;
CREATE PROC studentInfoClass @class_id INT
AS
BEGIN
	SELECT 
        ui.user_id, 
        ui.username, 
		MAX(ch.score) AS max_score,
        AVG(ch.score) AS avg_score,
		(SELECT COUNT(ch.user_id) FROM Class_history ch WHERE ch.user_id = ui.user_id) AS test_per_std
    FROM dbo.User_info ui, dbo.Class_history ch, dbo.Class_user cu
	WHERE cu.class_id = @class_id
	AND cu.user_id = ui.user_id
	AND ch.user_id = ui.user_id
    GROUP BY ui.user_id, ui.username
END;
GO;
--Test get student from class
EXEC dbo.studentInfoClass 2;
GO;

--Query number of Test and number of student inside a class
DROP PROC classInfo;
GO;
CREATE PROC classInfo @class_id INT
AS
BEGIN
Select number_student, (SELECT COUNT(test_id) FROM Class_test WHERE class_id=@class_id) FROM Class WHERE class_id=@class_id;
END;
GO;

--Test get class info
EXEC dbo.classInfo 2;
GO;


--Add student to class
-- ADD STUDENT TO CLASS---
DROP PROCEDURE addStudentToClass
GO;
SET ANSI_NULLS ON
GO;
SET QUOTED_IDENTIFIER ON
GO;
CREATE PROCEDURE addStudentToClass
	@classId INT, @studentId INT
AS
BEGIN
SET NOCOUNT ON
--Check if the student existed
IF NOT EXISTS (SELECT 1 FROM User_info WHERE user_id = @studentId)
	BEGIN
		--PRINT 'This student is not exist'
		SELECT 0;
	END;
ELSE
	BEGIN
	--Check if this student was in this class
	IF NOT EXISTS (SELECT 1 FROM Class_user WHERE class_id = @classId AND user_id = @studentId)
		BEGIN
		INSERT INTO Class_user(class_id, user_id) VALUES (@classId, @studentId);
		INSERT INTO Class_history(class_id, user_id)
		VALUES (@classId, @studentId);
		SELECT  1;
		END;
	ELSE
		BEGIN
		--PRINT 'This student existed in this class';
		SELECT -1;
		END;
    END;
END;


--Test add student to class
EXEC dbo.addStudentToClass 2, 26;
--See students in class
Select * From Class_user;
GO;

--DELETE STUDENT FROM CLASS
DROP PROCEDURE deleteStudentFromClass;
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE deleteStudentFromClass @classId INT, @studentId INT
AS
BEGIN
SET NOCOUNT ON
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
GO;
--Test delete student from class
EXEC dbo.deleteStudentFromClass 2, 26

-----------------------------------------------
---TRIGGER UPDATE NUMBER OF STUDENT IN CLASS---
-----------------------------------------------
DROP TRIGGER updateNumStudent;
GO;
CREATE TRIGGER updateNumStudent ON Class_user FOR INSERT
AS
BEGIN
	UPDATE Class 
	SET number_student = number_student + 1
	FROM Class, inserted WHERE Class.class_id = inserted.class_id;
END
GO;

--Test trigger
SELECT * FROM Class where class_id=2;
Insert into Class_user
values (2, 21);
SELECT * FROM Class where class_id=2;
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

----------------------------
---GET CLASS TEST---
----------------------------
DROP PROC getClassTest;
GO;
CREATE PROC getClassTest @class_id INT
AS
BEGIN
SELECT t.*, ct.duration FROM Class_test ct, Test t WHERE ct.class_id=@class_id AND ct.test_id=t.test_id;
END
GO;
--Get class test
EXEC getClassTest 2;



----------------------------
---GET STUDENT CLASS---
----------------------------
DROP PROC getStudentClass;
GO;
CREATE PROC getStudentClass @id INT
AS
BEGIN
SELECT c.*, t.username as teacher FROM Class c, Class_user cu, User_info t WHERE cu.user_id=@id AND c.class_id=cu.class_id AND t.user_id=c.teacher_id;
END
GO;

--Test Get Student Class
EXEC getStudentClass 14;

----------------------------
---INSERT CLASS HISTORY---
----------------------------
DROP PROC insertClassHistory;
GO;
CREATE PROC insertClassHistory 
(@user_id INT, @test_id INT, @class_id INT, @score FLOAT)
AS
BEGIN
INSERT INTO Class_history(class_id, user_id, test_id, score)
VALUES (@class_id, @user_id, @test_id, @score)
END
GO;

----------------------------
---Add Test to Class---
----------------------------
DROP PROC addTestToClass;
GO;
CREATE PROC addTestToClass @classId INT, @testId INT, @duration INT
AS
BEGIN
SET NOCOUNT ON
--Check if the test existed
IF NOT EXISTS (SELECT 1 FROM Test WHERE test_id = @testId)
	BEGIN
		--PRINT 'This test is not exist'
		SELECT 0;
	END;
ELSE
	BEGIN
	--Check if this test was in this class
	IF NOT EXISTS (SELECT 1 FROM Class_test WHERE class_id = @classId AND test_id = @testId)
		BEGIN
		INSERT INTO Class_test(class_id, test_id, duration) VALUES (@classId, @testId, @duration);
		SELECT  1;
		END;
	ELSE
		BEGIN
		--PRINT 'This test existed in this class';
		SELECT -1;
		END;
    END;
END

--Test add test
EXEC dbo.addTestToClass 2, 42, 120;
SELECT * FROM Class_test;
GO;
----------------------------
---Delete Test From Class---
----------------------------
DROP PROC deleteTestFromClass;
GO;
CREATE PROC deleteTestFromClass @classId INT, @testId INT
AS
BEGIN
SET NOCOUNT ON
--Check if the test existed
IF NOT EXISTS (SELECT 1 FROM Test WHERE test_id = @testId)
	BEGIN
		--PRINT 'This test is not exist'
		SELECT 0;
	END;
ELSE
	BEGIN
	--Check if this test was in this class
	IF NOT EXISTS (SELECT 1 FROM Class_test WHERE class_id = @classId AND test_id = @testId)
		BEGIN
		SELECT  -1;
		END;
	ELSE
		BEGIN
		--PRINT 'This test existed in this class';
		DELETE FROM Class_test WHERE class_id=@classId AND test_id=@testId;
		SELECT 1;
		END;
    END;
END

--Test add test
EXEC dbo.deleteTestFromClass 2, 42;
SELECT * FROM Class_test;
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
        SELECT u.username, ch.user_id, ch.test_id, ch.score, ch.finish_time
        FROM dbo.Class_history ch, User_info u
        WHERE ch.user_id = @userID AND ch.test_id = @testID AND ch.class_id = @classID AND u.user_id=ch.user_id;
    END
    -- Scenario 2: Only userID is provided
    ELSE IF @userID IS NOT NULL AND @testID IS NULL
    BEGIN
        SELECT u.username, ch.user_id, ch.test_id, ch.score, ch.finish_time
        FROM dbo.Class_history ch, User_info u
        WHERE ch.user_id = @userID AND ch.class_id = @classID AND u.user_id=ch.user_id;
    END
    -- Scenario 3: Only testID is provided
    ELSE IF @userID IS NULL AND @testID IS NOT NULL
    BEGIN
        SELECT u.username, ch.user_id, ch.test_id, ch.score, ch.finish_time
        FROM dbo.Class_history ch, User_info u
        WHERE ch.test_id = @testID AND ch.class_id = @classID AND u.user_id=ch.user_id;
    END
    -- Scenario 4: Neither userID nor testID is provided
    ELSE
    BEGIN
        SELECT user_id, test_id, score, finish_time
        FROM dbo.Class_history;
    END
END
GO;

--Test get test result
EXEC GetTestResults 14, 100, 2;