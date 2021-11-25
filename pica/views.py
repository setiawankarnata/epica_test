from datetime import datetime, date
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from .models import Company, Peserta, DivDept, Meeting, Forum, Topik, Activity, Signature
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template


def meet_render_pdf(request, pk):
    meet = get_object_or_404(Meeting, pk=pk)
    template_path = 'pica/pdf_daily_meeting.html'
    peserta = Peserta.objects.filter(peserta2meeting=meet, bod=True)
    all_peserta = Peserta.objects.filter(peserta2meeting=meet)
    topik = Topik.objects.filter(topik2meeting=meet)

    context = {
        'meet': meet,
        'peserta': peserta,
        'topik': topik,
        'all_peserta': all_peserta,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="meeting.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Terjadi error pada <pre>" + html + "</pre>")
    return response


def meet_signature_pdf(request, pk):
    meet = get_object_or_404(Meeting, pk=pk)
    template_path = 'pica/pdf_signature_meeting.html'
    peserta = Peserta.objects.filter(peserta2meeting=meet, bod=True)
    all_peserta = Peserta.objects.filter(peserta2meeting=meet)
    topik = Topik.objects.filter(topik2meeting=meet)
    forum = Forum.objects.get(pk=meet.meeting2forum.pk)
    signs = Signature.objects.filter(signature2forum=forum).order_by('-presdir')
    # for sig in signs:
    #
    context = {
        'meet': meet,
        'peserta': peserta,
        'topik': topik,
        'all_peserta': all_peserta,
        'signs': signs,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="signature_meeting.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Terjadi error pada <pre>" + html + "</pre>")
    return response


def send_meet_render_pdf(request, pk):
    meet = get_object_or_404(Meeting, pk=pk)
    template_path = 'pica/pdf_daily_meeting.html'
    peserta = Peserta.objects.filter(peserta2meeting=meet, bod=True)
    all_peserta = Peserta.objects.filter(peserta2meeting=meet)
    to_email = []
    for pes in peserta:
        to_email.append(pes.email)

    topik = Topik.objects.filter(topik2meeting=meet)
    person = {}
    # to_pic = {}
    for top in topik:
        pics = User.objects.filter(user2topik=top)
        lst = []
        # lst_pic = []
        for pic in pics:
            lst.append(pic.first_name + " " + pic.last_name)
            # lst_pic.append(pic.email)
        person[top.pk] = lst
        # to_pic[top.pk] = lst_pic
    context = {
        'meet': meet,
        'peserta': peserta,
        'topik': topik,
        'person': person,
        'all_peserta': all_peserta,
    }
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = result.getvalue()
    filename = "MEETING " + str(meet.meeting_date) + ".pdf"
    mail_subject = "Summary Meeting " + str(meet.meeting_date)
    mail_message = "Dengan Hormat, \n\n" + "Berikut MoM Meeting hari ini. \n" + "Mohon untuk di-follow up. \n" + "Demikian disampaikan, terimakasih atas perhatiannya. \n\n" + \
                   "Regards, \n\n" + "CPMD \n"

    email = EmailMessage(
        mail_subject,
        mail_message,
        settings.EMAIL_HOST_USER,
        to_email,
    )
    email.attach(filename, pdf, 'application/pdf')
    email.send(fail_silently=False)

    #############################
    # Render special topik
    #############################
    today = datetime.today().strftime("%Y-%m-%d")
    for top in topik:
        dept = get_object_or_404(DivDept, departemen2topik=top)
        activities = Activity.objects.filter(activity2topik=top)
        pics = User.objects.filter(user2topik=top)
        context = {
            'top': top,
            'activities': activities,
            'pics': pics,
        }
        template_path = 'pica/pdf_pic_topik.html'
        to_email = []
        cc_email = []
        for pic in pics:
            to_email.append(pic.email)
        # cc_email.append(dept.email_dir_in_charge)
        # cc_email.append(dept.email_dept_head_in_charge)
        template = get_template(template_path)
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        filename = "Topik Meeting " + str(today) + ".pdf"
        mail_subject = "Topik Meeting " + str(today)
        mail_message = "Mohon agar dapat segera ditindak lanjuti topik seperti terlampir."
        email = EmailMessage(
            mail_subject,
            mail_message,
            settings.EMAIL_HOST_USER,
            to_email,
            cc=cc_email,
        )
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)

    return HttpResponse("Email sent!")


def list_pica(request, pk):
    topiks = Topik.objects.filter(topik2user=pk).exclude(status="CLOSE").order_by('due_date')

    context = {
        'topiks': topiks,
    }
    return render(request, 'pica/list_pica.html', context)


def create_activity(request, pk):
    topik = get_object_or_404(Topik, pk=pk)
    usr = get_object_or_404(User, pk=request.user.pk)
    acts = topik.topik2activity.all().order_by('-date_activity')
    if request.method == "POST":
        form = CreateActivityForm(data=request.POST)
        if form.is_valid():
            act = topik.topik2activity.filter(date_activity=request.POST['date_activity'])
            if act:
                messages.error(request, "Activity untuk tanggal yang sama sudah ada.")
                return redirect('pica:create_activity', pk)
                pass
            else:
                new_form = form.save(commit=False)
                new_form.activity2topik = topik
                new_form.activity2user = usr
                new_form.save()
                return redirect("pica:create_activity", topik.pk)
    else:
        form = CreateActivityForm()
    context = {
        'form': form,
        'acts': acts,
        'topik': topik,
    }
    return render(request, 'pica/create_activity.html', context)


def list_activity(request, pk, ctr):
    topik = get_object_or_404(Topik, pk=pk)
    usr = get_object_or_404(User, pk=request.user.pk)
    acts = topik.topik2activity.all().order_by('-date_activity')
    form = ListActivityForm()
    context = {
        'form': form,
        'acts': acts,
        'topik': topik,
        'ctr': ctr,
    }
    return render(request, 'pica/list_activity.html', context)


def update_activity(request, pk):
    act = get_object_or_404(Activity, pk=pk)
    topik = get_object_or_404(Topik, pk=act.activity2topik.pk)
    if request.method == "POST":
        form = UpdateActivityForm(request.POST, instance=act)
        if form.is_valid():
            form.save()
            return redirect("pica:create_activity", act.activity2topik.pk)
    else:
        form = UpdateActivityForm(instance=act)
    context = {
        'form': form,
        'topik': topik,
    }
    return render(request, 'pica/update_activity.html', context)


def delete_topik(request, pk1, pk2):
    topik = get_object_or_404(Topik, pk=pk2)
    meet_id = pk1

    if request.method == "POST":
        topik.delete()
        messages.success(request, "Data berhasil di hapus.")
        return redirect('pica:meeting_dashboard', meet_id)
    context = {
        'topik': topik,
        'meet': meet_id,
    }
    return render(request, 'pica/delete_topik.html', context)


def delete_activity(request, pk):
    act = get_object_or_404(Activity, pk=pk)
    topik = act.activity2topik.pk
    if request.method == "POST":
        act.delete()
        return redirect('pica:create_activity', topik)
    context = {
        'act': act,
    }
    return render(request, 'pica/delete_activity.html', context)


def create_pica(request, pk):
    topiks = Topik.objects.exclude(status="CLOSE").order_by('due_date')
    if request.method == "POST":
        form = CreatePicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pica:create_pica", pk)
    else:
        form = CreatePicaForm()
    context = {
        'form': form,
        'topiks': topiks,
        'meet': pk,
    }
    return render(request, 'pica/create_pica.html', context)


def update_pica(request, pk1, pk2):
    topik = get_object_or_404(Topik, pk=pk1)
    topik_list = Topik.objects.exclude(status="CLOSE").order_by('due_date')
    all_activity = Activity.objects.filter(activity2topik=topik).order_by('date_activity')
    if request.method == "POST":
        form = UpdatePicaForm(request.POST, instance=topik)
        if form.is_valid():
            form.save()
            return redirect("pica:create_pica", pk2)
    else:
        form = UpdatePicaForm(instance=topik)
    context = {
        'form': form,
        'all_activity': all_activity,
        'meet': pk2,
        'topik': topik,
        'topik_list': topik_list,
    }
    return render(request, 'pica/update_pica.html', context)


def update_pica_action(request, pk1, pk2):
    topik = get_object_or_404(Topik, pk=pk1)
    meet = get_object_or_404(Meeting, pk=pk2)
    all_activity = Activity.objects.filter(activity2topik=topik).order_by('-date_activity')
    if request.method == "POST":
        form = UpdatePicaActionForm(request.POST, instance=topik)
        if form.is_valid():
            form.save()
            return redirect("pica:meeting_dashboard", meet.pk)
    else:
        form = UpdatePicaActionForm(instance=topik)
    context = {
        'form': form,
        'meet': meet,
        'all_activity': all_activity,
    }
    return render(request, 'pica/update_pica_action.html', context)


class CreateDepartemenView(SuccessMessageMixin, CreateView):
    model = DivDept
    form_class = CreateDepartemenForm
    template_name = 'pica/create_departemen.html'
    success_message = "Data divisi/departemen berhasil disimpan"
    success_url = reverse_lazy('pica:create_departemen')

    def get_context_data(self, **kwargs):
        depts = DivDept.objects.all().order_by('name')
        context = super(CreateDepartemenView, self).get_context_data(**kwargs)
        context['depts'] = depts
        return context


class UpdateDepartemenView(SuccessMessageMixin, UpdateView):
    model = DivDept
    template_name = 'pica/update_departemen.html'
    form_class = UpdateDepartemenForm
    success_message = 'Data departemen berhasil diupdate'
    success_url = reverse_lazy('pica:create_departemen')


class DeleteDepartemenView(SuccessMessageMixin, DeleteView):
    model = DivDept
    template_name = 'pica/delete_departemen.html'
    success_message = 'Data departemen berhasil dihapus'
    success_url = reverse_lazy('pica:create_departemen')

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        dept = DivDept.objects.get(pk=pk)
        context = super(DeleteDepartemenView, self).get_context_data(**kwargs)
        context['dept'] = dept
        return context


class CreateForumView(SuccessMessageMixin, CreateView):
    model = Forum
    form_class = CreateForumForm
    template_name = 'pica/create_forum.html'
    success_message = "Data forum berhasil disimpan"
    success_url = reverse_lazy('pica:create_forum')

    def get_context_data(self, **kwargs):
        forums = Forum.objects.all().order_by('nama_forum')
        context = super(CreateForumView, self).get_context_data(**kwargs)
        context['forums'] = forums
        return context


class UpdateForumView(SuccessMessageMixin, UpdateView):
    model = Forum
    template_name = 'pica/update_forum.html'
    form_class = UpdateForumForm
    success_url = reverse_lazy('pica:create_forum')


class UpdateDashboardView(SuccessMessageMixin, UpdateView):
    model = Meeting
    template_name = 'pica/update_dashboard.html'
    form_class = UpdateDashboardForm
    success_url = reverse_lazy('pica:create_meeting')

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        meet = Meeting.objects.get(pk=pk)
        context = super(UpdateDashboardView, self).get_context_data(**kwargs)
        context['meet'] = meet
        return context


class DeleteForumView(SuccessMessageMixin, DeleteView):
    model = Forum
    template_name = 'pica/delete_forum.html'
    success_message = 'Data forum berhasil dihapus'
    success_url = reverse_lazy('pica:create_forum')

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        forum = Forum.objects.get(pk=pk)
        context = super(DeleteForumView, self).get_context_data(**kwargs)
        context['forum'] = forum
        return context


class CreateCompanyView(SuccessMessageMixin, CreateView):
    model = Company
    form_class = CreateCompanyForm
    template_name = 'pica/create_company.html'
    success_message = "Data Company telah berhasil ditambahkan"
    success_url = reverse_lazy('pica:create_company')

    def get_context_data(self, **kwargs):
        companies = Company.objects.all().order_by('name')
        context = super(CreateCompanyView, self).get_context_data(**kwargs)
        context['companies'] = companies
        return context


class UpdateCompanyView(SuccessMessageMixin, UpdateView):
    model = Company
    template_name = 'pica/update_company.html'
    form_class = UpdateCompanyForm
    success_message = 'Data company berhasil diupdate'
    success_url = reverse_lazy('pica:create_company')


class DeleteCompanyView(SuccessMessageMixin, DeleteView):
    model = Company
    template_name = 'pica/delete_company.html'
    success_message = 'Data company berhasil dihapus'
    success_url = reverse_lazy('pica:create_company')

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        company = Company.objects.get(pk=pk)
        context = super(DeleteCompanyView, self).get_context_data(**kwargs)
        context['company'] = company
        return context


class CreatePesertaView(SuccessMessageMixin, CreateView):
    model = Peserta
    form_class = CreatePesertaForm
    template_name = 'pica/create_peserta.html'
    success_message = "Data Peserta telah berhasil ditambahkan"
    success_url = reverse_lazy('pica:create_peserta')

    def get_context_data(self, **kwargs):
        peserta = Peserta.objects.all().order_by('nama')
        context = super(CreatePesertaView, self).get_context_data(**kwargs)
        context['peserta'] = peserta
        return context


class UpdatePesertaView(SuccessMessageMixin, UpdateView):
    model = Peserta
    template_name = 'pica/update_peserta.html'
    form_class = UpdatePesertaForm
    success_message = 'Data peserta berhasil diupdate'
    success_url = reverse_lazy('pica:create_peserta')


class DeletePesertaView(SuccessMessageMixin, DeleteView):
    model = Peserta
    template_name = 'pica/delete_peserta.html'
    success_message = 'Data peserta berhasil dihapus'
    success_url = reverse_lazy('pica:create_peserta')

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        peserta = Peserta.objects.get(pk=pk)
        context = super(DeletePesertaView, self).get_context_data(**kwargs)
        context['peserta'] = peserta
        return context


class CreateMeetingView(SuccessMessageMixin, CreateView):
    model = Meeting
    form_class = CreateMeetingForm
    template_name = 'pica/create_meeting.html'
    success_message = "Data meeting berhasil disimpan"
    success_url = reverse_lazy('pica:create_meeting')

    def get_context_data(self, **kwargs):
        # meets = Meeting.objects.all().order_by('meeting_date')
        today = datetime.today()
        meets = Meeting.objects.filter(meeting_date__gte=today).order_by('meeting_date')
        context = super(CreateMeetingView, self).get_context_data(**kwargs)
        context['meets'] = meets
        return context


def history_meeting(request):
    meets = []
    if request.method == "POST":
        form = HistoryMeetingForm(request.POST)
        if form.is_valid():
            forum = form.cleaned_data['forum']
            period1 = form.cleaned_data['period1']
            period2 = form.cleaned_data['period2']
            meets = Meeting.objects.filter(meeting2forum__nama_forum=forum, meeting_date__range=(period1, period2))
            context = {
                'meets': meets,
                'form': form,
            }
            return render(request, 'pica/history_meeting.html', context)

    form = HistoryMeetingForm()
    context = {
        'meets': meets,
        'form': form,
    }
    return render(request, 'pica/history_meeting.html', context)


def meeting_dashboard(request, pk, hs):
    meeting = get_object_or_404(Meeting, pk=pk)
    topik = Topik.objects.filter(topik2meeting=pk)
    peserta = Peserta.objects.filter(peserta2meeting=pk)
    context = {
        'peserta': peserta,
        'topik': topik,
        'meeting': meeting,
        'hs': hs,
    }
    return render(request, 'pica/meeting_dashboard.html', context)


def add_peserta(request, pk):
    meet = Meeting.objects.get(pk=pk)
    current_peserta = meet.meeting2peserta.all()
    if request.method == "POST":
        nama = request.POST['nama_karyawan']
        non_bod_peserta = Peserta.objects.filter(nama__icontains=nama)
    else:
        non_bod_peserta = Peserta.objects.all()
    sisa_peserta = []
    for pes in non_bod_peserta:
        if pes not in current_peserta:
            sisa_peserta.append(pes)
    context = {
        'sisa_peserta': sisa_peserta,
        'meet': meet,
    }
    return render(request, 'pica/add_peserta.html', context)


def masukkan_peserta(request, pk1, pk2):
    meet = Meeting.objects.get(pk=pk1)
    pes = Peserta.objects.get(pk=pk2)
    meet.meeting2peserta.add(pes)
    return redirect('pica:add_peserta', meet.pk)


def hapus_peserta(request, pk1, pk2):
    meet = Meeting.objects.get(pk=pk1)
    pes = Peserta.objects.get(pk=pk2)
    meet.meeting2peserta.remove(pes)
    return redirect('pica:meeting_dashboard', meet.pk)


def add_pic(request, pk1, pk2):
    topik = Topik.objects.get(pk=pk1)
    user_topik = topik.topik2peserta.all()
    user_list = topik.topik2user.all()
    email_list = []
    for usr_email in user_list:
        email_list.append(usr_email.email)
    if request.method == "POST":
        nama_pic = request.POST['nama_pic']
        all_user = Peserta.objects.filter(nama__icontains=nama_pic).order_by('nama')
    else:
        all_user = Peserta.objects.all().order_by('nama')
    sisa_user = []
    for usr in all_user:
        if usr not in user_topik:
            sisa_user.append(usr)
    # sisa_user.sort()
    context = {
        'sisa_user': sisa_user,
        'topik': topik,
        'user_topik': user_topik,
        'meet': pk2,
        'user_list': user_list,
        'email_list': email_list,
    }
    return render(request, 'pica/add_pic.html', context)


def masukkan_pic(request, pk1, pk2, pk3, pk4):
    topik = Topik.objects.get(pk=pk1)
    pst = Peserta.objects.get(pk=pk2)
    # meet = Meeting.objects.get(pk=pk3)
    topik.topik2peserta.add(pst)

    if pk4 == 'Y':
        usr = User.objects.get(email=pst.email)
        topik.topik2user.add(usr)

    return redirect('pica:add_pic', topik.pk, pk3)


def hapus_pic(request, pk1, pk2, pk3):
    topik = Topik.objects.get(pk=pk1)
    pst = Peserta.objects.get(pk=pk2)
    lst_user = topik.topik2user.all()
    for usr in lst_user:
        if pst.email == usr.email:
            topik.topik2user.remove(usr)
    topik.topik2peserta.remove(pst)
    return redirect('pica:add_pic', topik.pk, pk3)


def add_topik(request, pk):
    meet = get_object_or_404(Meeting, pk=pk)
    current_topik = meet.meeting2topik.all()
    all_topik = Topik.objects.exclude(status="CLOSE")
    sisa_topik = []
    for tpk in all_topik:
        if tpk not in current_topik:
            sisa_topik.append(tpk)
    context = {
        'sisa_topik': sisa_topik,
        'meet': meet,
    }
    return render(request, 'pica/add_topik.html', context)


def masukkan_topik(request, pk1, pk2):
    meet = Meeting.objects.get(pk=pk1)
    tpk = Topik.objects.get(pk=pk2)
    tpk.topik2meeting = meet
    tpk.save()
    return redirect('pica:create_pica', meet.pk)


def hapus_topik(request, pk1, pk2):
    meet = Meeting.objects.get(pk=pk1)
    tpk = Topik.objects.get(pk=pk2)
    meet.meeting2topik.remove(tpk)
    return redirect('pica:meeting_dashboard', meet.pk)


def topik_expired_check(request):
    # today = datetime.today().strftime("%Y-%m-%d")
    hari_ini = date.today()
    topiks = Topik.objects.exclude(status="CLOSE", expired=False)
    for topik in topiks:
        if topik.due_date:
            # exp = topik.due_date.strftime("%Y-%m-%d")
            duedate = topik.due_date
            if duedate < hari_ini:
                topik.expired = True
                topik.save()
        else:
            pass
    topik_expired = Topik.objects.filter(status="OPEN", expired=True)
    context = {
        'topik_expired': topik_expired,
    }
    return render(request, 'pica/list_expired_topik.html', context)


def list_open_pica(request):
    topiks = []
    if request.method == "POST":
        form = ListOpenPicaForm(request.POST)
        if form.is_valid():
            forum = form.cleaned_data['forum']
            period1 = form.cleaned_data['period1']
            period2 = form.cleaned_data['period2']
            topiks = Topik.objects.filter(status="OPEN", topik2meeting__meeting2forum__nama_forum=forum,
                                          due_date__range=(period1, period2))
            context = {
                'topiks': topiks,
                'form': form,
            }
            return render(request, 'pica/list_open_pica.html', context)

    form = ListOpenPicaForm()
    context = {
        'topiks': topiks,
        'form': form,
    }
    return render(request, 'pica/list_open_pica.html', context)


def search_topik(request):
    results = []
    hasil = []
    person = {}

    if request.method == "POST":
        forms = SearchTopikForm(request.POST)
        if forms.is_valid():
            nama_query = forms.cleaned_data['nama_query']
            kategory = forms.cleaned_data['kategory']
            period1 = forms.cleaned_data['period1']
            period2 = forms.cleaned_data['period2']
            if kategory == '1':  # by Nama Topik
                results = Topik.objects.filter(nama_topik__icontains=nama_query)
            if kategory == '2':  # by Problem
                results = Topik.objects.filter(problem__icontains=nama_query)
            if kategory == '3':  # by Action
                results = Topik.objects.filter(action__icontains=nama_query)
            if kategory == '4':  # by Meeting forum
                topik_all = Topik.objects.all()
                for topik in topik_all:
                    if nama_query in topik.topik2meeting.meeting2forum.nama_forum:
                        results.append(topik)
            if kategory == '5':  # by Status
                results = Topik.objects.filter(status__icontains=nama_query)
            if kategory == '6':  # by Function
                results = Topik.objects.filter(topik2departemen__name__icontains=nama_query)
            if kategory == '7':  # by Company
                results = Topik.objects.filter(topik2company__name__icontains=nama_query)
            if kategory == '8':  # by PIC
                all_topik = Topik.objects.all()
                for top in all_topik:
                    usrs = top.topik2user.all()
                    for usr in usrs:
                        if (nama_query.lower() in usr.first_name.lower()) or (
                                nama_query.lower() in usr.last_name.lower()):
                            results.append(top)
            for result in results:
                if (result.topik2meeting.meeting_date >= period1) and (result.topik2meeting.meeting_date <= period2):
                    hasil.append(result)
    for top in hasil:
        pics = User.objects.filter(user2topik=top)
        lst = []
        for pic in pics:
            lst.append(pic.first_name + " " + pic.last_name)
        person[top.pk] = lst
    forms = SearchTopikForm()
    context = {
        'topiks': hasil,
        'person': person,
        'forms': forms,
    }
    return render(request, 'pica/search_topik.html', context)


def search_all(request):
    results = []
    person = {}

    if request.method == "POST":
        forms = SearchAllForm(request.POST)
        if forms.is_valid():
            cari = forms.cleaned_data['cari']
            results = Topik.objects.annotate(search=SearchVector('nama_topik', 'problem', 'action')).filter(search=cari)
    for top in results:
        pics = User.objects.filter(user2topik=top)
        lst = []
        for pic in pics:
            lst.append(pic.first_name + " " + pic.last_name)
        person[top.pk] = lst
    forms = SearchAllForm()
    context = {
        'topiks': results,
        'person': person,
        'forms': forms,
    }
    return render(request, 'pica/search_all.html', context)


def notify_all(request):
    topik_expired = Topik.objects.filter(expired=True)
    today = datetime.today().strftime("%Y-%m-%d")
    for topik in topik_expired:
        dept = get_object_or_404(DivDept, divdept2topik=topik)
        activities = Activity.objects.filter(activity2topik=topik)
        pics = User.objects.filter(user2topik=topik)
        context = {
            'topik': topik,
            'activities': activities,
            'pics': pics,
        }
        template_path = 'pica/pdf_topik_expired.html'
        to_email = []
        cc_email = []
        for pic in pics:
            to_email.append(pic.email)
        # cc_email.append(dept.email_dir_in_charge)
        # cc_email.append(dept.email_dept_head_in_charge)
        template = get_template(template_path)
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        filename = "Topik Oustanding " + str(today) + ".pdf"
        mail_subject = "Topik Oustanding " + str(today)
        mail_message = "Mohon agar dapat segera ditindak lanjuti outstanding topik seperti terlampir."
        email = EmailMessage(
            mail_subject,
            mail_message,
            settings.EMAIL_HOST_USER,
            to_email,
            cc=cc_email,
        )
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)

    return HttpResponse("Email sent!")


def show_messages(request):
    return render(request, 'show_messages.html')
