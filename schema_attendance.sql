CREATE DATABASE IF NOT EXISTS school_attendance_db;
USE school_attendance_db;

CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL UNIQUE,
  lrn VARCHAR(12) DEFAULT NULL,
  full_name VARCHAR(150) NOT NULL,
  grade_level VARCHAR(20) NOT NULL,
  section VARCHAR(50) NOT NULL,
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL,
  full_name VARCHAR(150) NOT NULL,
  grade_level VARCHAR(20) NOT NULL,
  section VARCHAR(50) NOT NULL,
  att_date DATE NOT NULL,
  time_in TIME NULL,
  time_out TIME NULL,
  status VARCHAR(20) DEFAULT 'PRESENT',
  remarks VARCHAR(100) DEFAULT NULL,
  INDEX idx_student_date (student_id, att_date)
);
