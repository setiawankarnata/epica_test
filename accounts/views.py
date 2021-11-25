from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Profile
from .forms import CreateProfileForm, SignUpForm, UpdateProfileForm, UpdateUserForm, LoginForm


@login_required(login_url='accounts:login')
def home(request):
    return render(request, 'home.html', {})


class PasswordResetPageView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'


class PasswordResetDonePageView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirmPageView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'


class PasswordResetCompletePageView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


class PasswordChangePageView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'


class PasswordChangeDonePageView(SuccessMessageMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'
    success_message = "Password has been changed. Please login again."
    success_url = reverse_lazy('accounts:login')


class LoginPageView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class LogoutPageView(LogoutView):
    template_name = 'registration/logout.html'


class SignUpPageView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    success_message = "User was created successfully"


class ProfileUpdatePageView(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:home')
    success_message = "Profile berhasil diupdate"


def profile_update_page_view(request, pk):
    prof = get_object_or_404(Profile, pk=pk)
    usr = get_object_or_404(User, pk=request.user.pk)
    if request.method == "POST":
        form1 = UpdateProfileForm(request.POST, instance=prof)
        form2 = UpdateUserForm(request.POST, instance=usr)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, "Profile berhasil diupdate.")
            return redirect('accounts:home')
    else:
        form1 = UpdateProfileForm(instance=prof)
        form2 = UpdateUserForm(instance=usr)
    context = {
        'form1': form1,
        'form2': form2,
    }
    return render(request, 'accounts/profile_update.html', context)


class ProfileCreatePageView(SuccessMessageMixin, CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('accounts:home')
    success_message = 'Profile berhasil di create'

    def form_valid(self, form):
        form.instance.profile2user_id = self.kwargs['id']
        return super().form_valid(form)


def profile_page_view(request):
    pk = request.user.id
    user = User.objects.get(pk=pk)
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)
