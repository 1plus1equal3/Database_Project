--User Table
DROP TABLE User_info;
GO;
CREATE TABLE User_info(
	user_id int PRIMARY KEY IDENTITY(1, 1), -- Student ID/Teacher ID
	username nvarchar(255) NOT NULL,
	user_password nvarchar(255) NOT NULL, -- > 8 character
	email nvarchar(255) NOT NULL, -- check validation
	user_type int NOT NULL-- admin(1) or participant(0)
);

select -1;

INSERT INTO User_info(username, user_password, email, user_type)
VALUES 
('Nguyen Dang Duy', 'aothatday123', 'dontunderstandyou12345@gmail.com', 1),
('Bui Duc Viet', 'vietdepzai123', 'viet.bd215254@sis.hust.edu.vn', 1),
('Tran Thuy Chau', 'chauxinggai123', 'chau.tt215182@sis.hust.edu.vn', 1),
('Pham Quang Huy', 'huydepzai123', 'huy.pq215207@sis.hust.edu.vn', 1);

TRUNCATE TABLE User_info;

SELECT * FROM User_info;

UPDATE User_info
SET user_type = 1
WHERE user_id BETWEEN 0 AND 13;

DELETE FROM User_info
WHERE username = 'test';

--Question table
DROP TABLE Question;

CREATE TABLE Question (
        question_id VARCHAR(50) PRIMARY KEY,
        question_content VARCHAR(3000) NOT NULL,
        level INT NOT NULL,
        subject VARCHAR(255),
        topic VARCHAR(255),
		ans CHAR
);

ALTER TABLE Question
ADD ans CHAR; 


SELECT * FROM Question WHERE question_content = 'Platelets transfusion must be completed in how many hours after entering the bag';

DROP TABLE Question;

--Answer table
DROP TABLE Answer;

CREATE TABLE Answer (
        question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
        opt CHAR NOT NULL,
        answer_content VARCHAR(1000) NOT NULL,
        is_correct BIT NOT NULL
);

ALTER TABLE Answer
DROP COLUMN is_correct;

SELECT * FROM Answer where question_id = 'e38f2f41-bc94-4276-85c9-d4225212a141';

--Explaination table
DROP TABLE Explaination;

CREATE TABLE Explaination (
        question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
        explaination VARCHAR(8000)
);

SELECT * FROM Explaination;

--Test table
DROP TABLE Test;

CREATE TABLE Test (
        test_id INT IDENTITY(1,1) PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        date_created DATE,
        admin_id INT
);

ALTER TABLE Test
DROP COLUMN ans; 

ALTER TABLE Test 
ALTER COLUMN title VARCHAR(255) NOT NULL;

SELECT * FROM Test;
UPDATE Test
SET admin_id = 5
WHERE test_id between 21 and 30;
DELETE FROM Test WHERE test_id = 6;

Insert into Test (title, date_created, admin_id)
values ('test_0', cast(getdate() as date), 0);

DROP TABLE Test_question;

CREATE TABLE Test_question(
		question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
		test_id INT FOREIGN KEY REFERENCES Test(test_id)
)

SELECT * FROM Test_question;

BACKUP DATABASE Project
TO DISK = 'C:\Users\D\Documents\GitHub\Database_Project\Backend_Server\backup_db';

DROP TABLE History;

CREATE TABLE History(
		user_id INT NOT NULL FOREIGN KEY REFERENCES User_info(user_id),
		test_id INT NOT NULL FOREIGN KEY REFERENCES Test(test_id),
		score FLOAT NOT NULL,
		finish_time DATE NOT NULL DEFAULT GETDATE()
);

TRUNCATE TABLE History;

-- Test insert history
Insert into History(user_id, test_id, score) Values(1, 10, 10);

Select * from History;