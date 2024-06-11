-- GET A CLASS'S INFORMATION
CREATE PROCEDURE GetClassInfo
    @teacherID INT,
    @classID INT
AS
BEGIN
    SET NOCOUNT ON
    -- Check if the class exists
    IF NOT EXISTS (SELECT * FROM dbo.Class WHERE class_id = @classID AND teacher_id = @teacherID)
    BEGIN
        PRINT 'This class does not exist or does not belong to the specified teacher'
        RETURN -1
    END
    
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
END


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
                        COMMIT;
					END;
				ELSE
					BEGIN
						--PRINT 'This student existed in this class';
						SELECT -1;
					END;
			END;
	END;
END;

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
                            COMMIT;
					END;
			END;
	END;
END;