from django.contrib import admin, messages
from .models import Signature, Company, DivDept, Peserta, Forum, Meeting, Topik, Activity, Pic
from django import forms
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Register your models here.
admin.site.register(Signature)
admin.site.register(Company)
admin.site.register(DivDept)
admin.site.register(Forum)
admin.site.register(Meeting)
admin.site.register(Topik)
admin.site.register(Activity)
admin.site.register(Pic)


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
    # incl_header = forms.BooleanField(initial=False)


class PesertaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'bod')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                kolom = x.split(",")
                # if request.POST['incl_header'] == True:
                #     skip_header = True
                # else:
                #     skip_header = False
                created = Peserta.objects.update_or_create(
                    nama=kolom[0],
                    email=kolom[1],
                    bod=True if kolom[2] == "Y" else False
                )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


admin.site.register(Peserta, PesertaAdmin)
