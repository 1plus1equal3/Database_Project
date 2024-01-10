-- Login/Sign up function

--Login function
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




--Sign up store_procedure
CREATE PROC func_register 
(@u_name nvarchar(255), @u_pass nvarchar(255), @email nvarchar(255))
AS
BEGIN
DECLARE @name INT;
SELECT @name = COUNT(username) FROM User_info WHERE username = @u_name;
IF @name <> 0 --If not return -1
RETURN -1;
--Else insert and return 0
INSERT INTO User_info(username, user_password, email, user_type)
VALUES (@u_name, @u_pass, @email, 0);
RETURN 1;
END;
GO;

--Test register
DECLARE @result INT;
EXEC @result = func_register 'tester', 'tester', 'test_email';
SELECT @result;

SELECT * FROM User_info;
GO;


-- User function
 
-- Load dashboard with random exam

SELECT TOP 10 * FROM Test
ORDER BY NEWID();
GO;

CREATE VIEW request_exam_list
AS SELECT TOP 10 * FROM Test
ORDER BY NEWID();
GO;

CREATE FUNCTION request_exam()
RETURNS TABLE
AS
RETURN SELECT * FROM request_exam_list;
GO;

--Error
CREATE FUNCTION request_exam_1()
RETURNS TABLE
AS
RETURN (SELECT TOP 10 * FROM Test
ORDER BY NEWID());
GO;

--Test request_exam
SELECT * FROM dbo.request_exam();
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

CREATE PROCEDURE GetAnswerText
(@question_ID VARCHAR(50))
AS
BEGIN
    SELECT answer_content
    FROM Answer
    WHERE question_id = @question_ID
END;
GO;

EXEC GetAnswerText @question_ID = "ed2a9e8e-66a7-4090-84f1-21d823db1ade";
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
SELECT * FROM dbo.request_user_history(6);
GO;