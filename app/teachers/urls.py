"""
teacher app  URL Configurations.
"""

from django.urls import path
from teachers.views import SubjectsListView, DeleteSubjectView, AddSubjectView,TeachersListView, DeleteTeacherView, AddTeacherView,\
    EditTeacherView, ChangePictureView, TeacherProfileView, CSVImportView, ImagesImportView

urlpatterns = [
    path('subjects', SubjectsListView.as_view(), name = 'subjects'),
    path('new-subject', AddSubjectView.as_view(), name = 'new-subject'),
    path('delete-subject/<int:subject_id>', DeleteSubjectView.as_view(), name = 'delete-subject'),
    path('teachers', TeachersListView.as_view(), name = 'teachers'),
    path('new-teacher', AddTeacherView.as_view(), name = 'new-teacher'),
    path('delete-teacher/<int:teacher_id>', DeleteTeacherView.as_view(), name = 'delete-teacher'),
    path('edit-teacher/<int:pk>', EditTeacherView.as_view(), name = 'edit-teacher'),
    path('change-picture/<int:pk>', ChangePictureView.as_view(), name = 'change-picture'),
    path('profile/<int:pk>', TeacherProfileView.as_view(), name = 'profile'),
    path('import-csv', CSVImportView.as_view(), name = 'import-csv'),
    path('import-images', ImagesImportView.as_view(), name = 'import-images'),
]
