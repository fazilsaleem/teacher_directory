'''
Created on 01-Feb-2020

@author: Sarath Sankar
'''

class BaseMessages(object):
    def __init__(self):
        self.INVALID_CREDENTIALS = "Please provide valid  credentials"
        self.USER_NOT_EXISTS = "User with provided email does not exist."
        self.LOGIN_SUCCESS = "Login success, Welcome."
        self.SUBJECT_DELETED = "Subject deletion successful."
        self.SUBJECT_NOT_FOUND = "Something went wrong. Please try again."
        self.SUBJECT_NOTCREATED = "Subject could not create. Please try again."
        self.SUBJECT_CREATED = "New subject added."
        self.TEACHER_DELETED = "Teacher deletion successful."
        self.TEACHER_NOT_FOUND = "Something went wrong. Please try again."
        self.EMAIL_EXISTS = "This email is already registered. Please use a different email address."
        self.TEACHER_UPDATE = "Teacher details updated."
        self.NOT_CSV = "Unsupported format, Please upload a csv file."
        self.SUBJECT_DATA_EXISTS = "Could not delete this subject, already assigned to a teacher."

