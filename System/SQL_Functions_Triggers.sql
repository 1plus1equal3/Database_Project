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