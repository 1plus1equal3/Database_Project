--User Table
DROP TABLE User_info;
GO;
CREATE TABLE User_info(
	user_id INT PRIMARY KEY IDENTITY(1, 1), -- Student ID/Teacher ID
	username NVARCHAR(255) NOT NULL,
	user_password NVARCHAR(255) NOT NULL, -- > 8 character
	email NVARCHAR(255) NOT NULL, -- check validation
	user_type INT NOT NULL-- admin(1) or participant(0)
);
EXEC sp_columns User_info;
SELECT * FROM User_info;

--Question table
DROP TABLE Question;
GO;
CREATE TABLE Question (
        question_id VARCHAR(50) PRIMARY KEY,
        question_content VARCHAR(3000) NOT NULL,
        level INT NOT NULL,
        subject VARCHAR(255),
        topic VARCHAR(255),
		ans CHAR
);
EXEC sp_columns Question;
SELECT * FROM Question;

--Answer table
DROP TABLE Answer;
CREATE TABLE Answer (
        question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
        opt CHAR NOT NULL,
        answer_content VARCHAR(1000) NOT NULL,
);
EXEC sp_columns Answer;
SELECT * FROM Answer;

--Explaination table
DROP TABLE Explaination;
CREATE TABLE Explaination (
        question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
        explaination VARCHAR(8000)
);
EXEC sp_columns Explaination;
SELECT * FROM Explaination;

--Test table
DROP TABLE Test;
CREATE TABLE Test (
        test_id INT IDENTITY(1,1) PRIMARY KEY,
        title VARCHAR(255) NOT NULL UNIQUE,
        date_created DATE,
        admin_id INT,
		subject VARCHAR(30),
		difficulty_level INT
);
EXEC sp_columns Test;
SELECT * FROM Test;

--Reset identity to current max identity
DECLARE @max int
SELECT @max=MAX(test_id) FROM Test
IF @max IS NULL   --check when max is returned as null
  SET @max = 0
DBCC CHECKIDENT ('Test', RESEED, @max)

--Test question table
DROP TABLE Test_question;
CREATE TABLE Test_question(
		question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
		test_id INT FOREIGN KEY REFERENCES Test(test_id)
)
EXEC sp_columns Test_question;
SELECT * FROM Test_question;

--History table
DROP TABLE History;
CREATE TABLE History(
		user_id INT NOT NULL FOREIGN KEY REFERENCES User_info(user_id),
		test_id INT NOT NULL FOREIGN KEY REFERENCES Test(test_id),
		score FLOAT NOT NULL,
		finish_time DATE NOT NULL DEFAULT GETDATE()
);
EXEC sp_columns History;
Select * FROM History;

--Class table
DROP TABLE Class;
CREATE TABLE Class(
  class_id INT IDENTITY(1,1) PRIMARY KEY,
  teacher_id INT,
  class_name VARCHAR(50) UNIQUE,
  number_student INT NOT NULL DEFAULT 0,
  create_date date NOT NULL DEFAULT GETDATE()
);
EXEC sp_columns Class;
Select * FROM Class;

--Add test data
INSERT INTO Class(teacher_id, class_name) VALUES
(13, 'class_01'),
(13, 'class_02'),
(13, 'class_03'),
(13, 'class_04'),
(13, 'class_05');

CREATE TABLE Class_user(
  class_id INT,
  user_id INT,
  FOREIGN KEY(class_id) REFERENCES Class(class_id),
  FOREIGN KEY(user_id) REFERENCES User_info(user_id)
)

CREATE TABLE Class_test(
  class_id INT,
  test_id INT,
  FOREIGN KEY(class_id) REFERENCES Class(class_id),
  FOREIGN KEY(test_id) REFERENCES Test(test_id)
)