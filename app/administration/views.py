from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from _functools import reduce
from django.db.models.query_utils import Q
from administration.messages import BaseMessages
from administration.models import UserProfile
from django.views import View
from teachers.models import Subjects, Teachers


@method_decorator(login_required, name="dispatch")
class DashboradView(generic.TemplateView):
    """
    Dashboard view for users who have logged in, Others will be redirected to the Login page.
    """
    template_name = "administration/dashboard.html"
    model = Subjects
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            query_set = self.model.objects.filter(is_active=True)
            context['subjects'] = query_set
            context['subjects_count'] = query_set.count()
            context['teachers_count'] = Teachers.objects.filter(is_active=True).count()
            return context

class LoginView(generic.TemplateView):
    """
    User Login view. after login success, user will be redirected to the dashborad.
    """
    template_name = "administration/login.html"
    success_url = "dashboard"
    mesg_obj = BaseMessages()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST.get("email",None)
        password = request.POST.get("password",None)
        if not all([email,password]):
            messages.error(request,self.mesg_obj.INVALID_CREDENTIALS )
            return render(request, self.template_name, {})
        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            messages.error(request,self.mesg_obj.USER_NOT_EXISTS)
            return render(request, self.template_name, {"email" : email})
        user = authenticate(username=user_profile.user.username, password=password)
        if user:
            login(request, user)
        else:
            messages.error(request,"Incorrect password.")
            return render(request, self.template_name, {"email" : email})
        messages.success(request,self.mesg_obj.LOGIN_SUCCESS )
        return redirect(self.success_url)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name="dispatch")
class UserProfileView(generic.DetailView):
    template_name = "administration/user-profile.html"
    model = UserProfile



