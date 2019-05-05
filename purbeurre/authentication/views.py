from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import User

# Create your views here.


class AccountView(LoginRequiredMixin, TemplateView):
    """Show Account informations."""
    template_name = 'authentication/account.html'

    def get(self, request, *args, **kwargs):
        # Redirection to save: Issue #2 keep substitute with no connection
        if 'keep_substitute' in request.session.keys():
            return redirect('products:save')
        fullname = " ".join([request.user.first_name, request.user.last_name])
        context = {'fullname': fullname}
        return render(request, self.template_name, context)


class RegisterView(FormView):
    """Show Registration form and create user if valid."""
    form_class = RegisterForm
    success_url = reverse_lazy('authentication:account')
    template_name = 'authentication/register.html'

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        if user:
            login(self.request, user)
        return super().form_valid(form)


@login_required
def LogoutView(request):
    """Logout user."""
    logout(request)
    return redirect('index')


class ModifyView(LoginRequiredMixin, UpdateView):
    """Modify User infos."""
    model = User
    fields = ["first_name", "last_name"]
    template_name = 'authentication/modify.html'
    success_url = reverse_lazy('authentication:account')

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.user.id)
        return obj
