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

INSERT INTO User_info(username, user_password, email, user_type)
VALUES 
('Nguyen Dang Duy', 'aothatday123', 'dontunderstandyou12345@gmail.com', 1),
('Bui Duc Viet', 'vietdepzai123', 'viet.bd215254@sis.hust.edu.vn', 1),
('Tran Thuy Chau', 'chauxinggai123', 'chau.tt215182@sis.hust.edu.vn', 1),
('Pham Quang Huy', 'huydepzai123', 'huy.pq215207@sis.hust.edu.vn', 1);

insert into User_info(username, user_password, email, user_type) 
Values ('admin', 'admin', 'admin@gmail.com', 1);

SELECT * FROM User_info;

--Question table
DROP TABLE Question;

CREATE TABLE Question (
        question_id VARCHAR(50) PRIMARY KEY,
        question_content VARCHAR(3000) NOT NULL,
        level INT NOT NULL,
        subject VARCHAR(255),
        topic VARCHAR(255)
);

SELECT * FROM Question;

DROP TABLE Question;

--Answer table
DROP TABLE Answer;

CREATE TABLE Answer (
        question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
        opt CHAR NOT NULL,
        answer_content VARCHAR(1000) NOT NULL,
        is_correct BIT NOT NULL
);

SELECT * FROM Answer;

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
ALTER COLUMN title VARCHAR(255) NOT NULL;

SELECT * FROM Test;
DELETE FROM Test WHERE test_id = 6;

Insert into Test (title, date_created, admin_id)
values ('test_0', cast(getdate() as date), 0);

DROP TABLE Test_question;

CREATE TABLE Test_question(
		question_id VARCHAR(50) FOREIGN KEY REFERENCES Question(question_id),
		test_id INT FOREIGN KEY REFERENCES Test(test_id)
)

SELECT * FROM Test_question;

