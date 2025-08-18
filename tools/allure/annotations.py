from enum import Enum


class AllureEpics(str, Enum):
    LMS = "LMS service"
    STUDENT = "Student service"
    ADMINISTRATION = "Administration service"

class AllureFeatures(str, Enum):
    USERS = "Users"
    FILES = "Files"
    COURSES = "Courses"
    EXERCISES = "Exercises"
    AUTHENTICATION = "Authentication"