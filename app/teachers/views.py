from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from _functools import reduce
import operator
from django.db.models.query_utils import Q
from administration.messages import BaseMessages
from django.views.generic.list import ListView
from teachers.models import Subjects, Teachers
from django.views import View
from teachers.forms import TeacherProfileForm
import csv, io
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from zipfile import ZipExtFile, ZipFile


@method_decorator(login_required, name="dispatch")
class SubjectsListView(ListView):
    """
    Available subjects list
    """
    template_name = "teachers/subjects.html"
    model = Subjects

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            query_set = self.model.objects.filter(is_active=True).order_by('subject_name')
            context['subjects'] = query_set
            return context

@method_decorator(login_required, name="dispatch")
class DeleteSubjectView(View):
    redirect_url  = "subjects"
    model = Subjects
    mesg_obj = BaseMessages()

    def get(self, request, subject_id):
        try:
            if Teachers.objects.filter(subjects_taught__in =  [subject_id]).exists():
                messages.error(request, self.mesg_obj.SUBJECT_DATA_EXISTS)
                return redirect(self.redirect_url)
            self.model.objects.get(id=subject_id).delete()
            messages.success(request, self.mesg_obj.SUBJECT_DELETED)
            return redirect(self.redirect_url)
        except:
            messages.error(request, self.mesg_obj.SUBJECT_NOT_FOUND)
            return redirect(self.redirect_url)

@method_decorator(login_required, name="dispatch")
class AddSubjectView(View):
    success_url= 'subjects'
    model = Subjects
    mesg_obj = BaseMessages()

    def post(self, request):
        subject = request.POST.get("subject", None)
        if subject:
            self.model.objects.create(subject_name = subject)
            messages.success(request,self.mesg_obj.SUBJECT_CREATED )
        else:
            messages.error(request,self.mesg_obj.SUBJECT_NOTCREATED )
        return redirect(self.success_url)

@method_decorator(login_required, name="dispatch")
class TeachersListView(ListView):
    """
    Available subjects list
    """
    template_name = "teachers/teachers.html"
    model = Teachers

    def get_queryset(self):
        search_query = self.request.GET.get('lname_filter', '')
        subject = self.request.GET.get('subjects_taught', '')
        filter_list = [Q(is_active=True)]
        if search_query:
            search_query = search_query.strip()
            filter_list.append(Q(last_name__startswith=search_query))
        if subject: filter_list.append(Q(subjects_taught__id=subject))
        object_list = self.model.objects.filter(reduce(
                operator.and_, filter_list))
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_set = self.get_queryset
        context['teachers'] = query_set
        context['subjects'] = Subjects.objects.filter(is_active=True).order_by('subject_name')
        return context

@method_decorator(login_required, name="dispatch")
class DeleteTeacherView(View):
    redirect_url  = "teachers"
    model = Teachers
    mesg_obj = BaseMessages()

    def get(self, request, teacher_id):
        try:
            self.model.objects.get(id=teacher_id).delete()
            messages.success(request, self.mesg_obj.TEACHER_DELETED)
            return redirect(self.redirect_url)
        except:
            messages.error(request, self.mesg_obj.TEACHER_NOT_FOUND)
            return redirect(self.redirect_url)
            
@method_decorator(login_required, name="dispatch")
class AddTeacherView(generic.FormView):
    template_name = "teachers/create-teacher.html"
    model = Teachers
    mesg_obj = BaseMessages()
    success_url = 'teachers'
    form_class = TeacherProfileForm

    def get_context_data(self, **kwargs):
            context_data = generic.FormView.get_context_data(self, **kwargs)
            if 'form' not in kwargs:
                context_data['form'] = self.form_class
            context_data.update(kwargs)
            return context_data

    def form_invalid(self, teacher_form):
        kwargs = {}
        kwargs['form'] = teacher_form
        return render(self.request, self.template_name, self.get_context_data(**kwargs))

    def form_valid(self, teacher_form):
        teacher_form.save()
        return redirect(self.success_url)

@method_decorator(login_required, name='get')
class EditTeacherView(generic.UpdateView):
    template_name = 'teachers/edit-teacher.html'
    model = Teachers
    mesg_ob = BaseMessages()
    form_class = TeacherProfileForm
    success_url = 'teachers'

    def get_success_url(self):
        return "/directory/teachers"

@method_decorator(login_required, name="dispatch")
class ChangePictureView(View):

    def post(self, request, pk):
        profile_picture = request.FILES.get("profile_picture")
        try:
            teacher_obj = Teachers.objects.get(id=pk)
        except:
            return redirect('teachers')
        teacher_obj.profile_picture = profile_picture
        teacher_obj.save()
        return redirect('profile' ,teacher_obj.id)

@method_decorator(login_required, name="dispatch")
class TeacherProfileView(generic.DetailView):
    template_name = "teachers/profile.html"
    model = Teachers

@method_decorator(login_required, name="dispatch")
class DataImportView(View):
    redirect_url = "teachers"
    mesg_obj = BaseMessages()
    def post(self, request):
        uploaded_files = request.FILES.getlist('data_import')
        for file_item in uploaded_files:
            if file_item.name.endswith('.zip'):
                with ZipFile(file_item,'r') as images:
                    images.extractall(f'{settings.MEDIA_ROOT}/teacher_profile')
            elif file_item.name.endswith('.csv'):
                FNAME,LNAME,IMG,EMAIL,PHONE,ROOM,SUBJECTS = settings.CSV_ORDER.values()
                teacher_data = file_item.read().decode('UTF-8')
                buff_str = io.StringIO(teacher_data)
                next(buff_str)
                for column in csv.reader(buff_str, delimiter=',', quotechar='"'):
                    if column[0]:
                        if Teachers.objects.filter(email=column[EMAIL]).exists():
                            continue
                        teacher_object = Teachers()
                        teacher_object.first_name = column[FNAME]
                        teacher_object.last_name = column[LNAME]
                        column[IMG] = ' '.join(column[IMG].split())
                        if column[IMG]:
                            teacher_object.profile_picture = f'teacher_profile/{column[IMG]}'
                        else:
                            teacher_object.profile_picture = None
                        teacher_object.email = column[EMAIL]
                        teacher_object.phone_number = column[PHONE]
                        teacher_object.room_number = column[ROOM]
                        teacher_object.save()
                        subjects = column[SUBJECTS]
                        subject_obj_list = []
                        for subject in subjects.split(','):
                            subject_string = subject.strip().title()
                            subject_obj = None
                            subject_obj = Subjects.objects.filter(subject_name=subject_string).last()
                            if not subject_obj:
                                subject_obj = Subjects.objects.create(subject_name=subject_string)
                            subject_obj_list.append(subject_obj)   
                        for ind, subj in enumerate(subject_obj_list):
                            if ind <settings.MAX_SUBJECT:
                                teacher_object.subjects_taught.add(subj)
                        teacher_object.save()
        return redirect(self.redirect_url)











