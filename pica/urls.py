from django.urls import path
from . import views

app_name = "pica"
urlpatterns = [
    path('', views.home, name="home"),
    path('create_departemen/', views.CreateDepartemenView.as_view(), name="create_departemen"),
    path('update_departemen/<int:pk>/', views.UpdateDepartemenView.as_view(), name="update_departemen"),
    path('delete_departemen/<int:pk>/', views.DeleteDepartemenView.as_view(), name="delete_departemen"),
    path('create_forum/', views.CreateForumView.as_view(), name="create_forum"),
    path('update_forum/<int:pk>/', views.UpdateForumView.as_view(), name="update_forum"),
    path('delete_forum/<int:pk>/', views.DeleteForumView.as_view(), name="delete_forum"),
    path('create_company/', views.CreateCompanyView.as_view(), name="create_company"),
    path('update_company/<int:pk>/', views.UpdateCompanyView.as_view(), name="update_company"),
    path('delete_company/<int:pk>/', views.DeleteCompanyView.as_view(), name="delete_company"),
    path('create_peserta/', views.CreatePesertaView.as_view(), name="create_peserta"),
    path('update_peserta/<int:pk>/', views.UpdatePesertaView.as_view(), name="update_peserta"),
    path('delete_peserta/<int:pk>/', views.DeletePesertaView.as_view(), name="delete_peserta"),
    path('add_peserta/<int:pk>/', views.add_peserta, name="add_peserta"),
    path('masukkan_peserta/<int:pk1>/<int:pk2>/', views.masukkan_peserta, name="masukkan_peserta"),
    path('hapus_peserta/<int:pk1>/<int:pk2>/', views.hapus_peserta, name="hapus_peserta"),
    path('create_pica/<int:pk>/', views.create_pica, name="create_pica"),
    path('update_pica/<int:pk1>/<int:pk2>/', views.update_pica, name="update_pica"),
    path('update_pica_action/<int:pk1>/<int:pk2>/', views.update_pica_action, name="update_pica_action"),
    path('add_pic/<int:pk1>/<int:pk2>/', views.add_pic, name="add_pic"),
    path('meet_render_pdf/<int:pk>/', views.meet_render_pdf, name="meet_render_pdf"),
    path('meet_signature_pdf/<int:pk>/', views.meet_signature_pdf, name="meet_signature_pdf"),
    path('send_meet_render_pdf/<int:pk>/', views.send_meet_render_pdf, name="send_meet_render_pdf"),
    path('masukkan_pic/<int:pk1>/<int:pk2>/<int:pk3>/<str:pk4>/', views.masukkan_pic, name="masukkan_pic"),
    path('hapus_pic/<int:pk1>/<int:pk2>/<int:pk3>/', views.hapus_pic, name="hapus_pic"),
    path('create_meeting/', views.CreateMeetingView.as_view(), name="create_meeting"),
    path('history_meeting/', views.history_meeting, name="history_meeting"),
    path('meeting_dashboard/<int:pk>/<int:hs>/', views.meeting_dashboard, name="meeting_dashboard"),
    path('update_dashboard/<int:pk>/', views.UpdateDashboardView.as_view(), name="update_dashboard"),
    path('list_pica/<int:pk>/', views.list_pica, name="list_pica"),
    path('create_activity/<int:pk>/', views.create_activity, name="create_activity"),
    path('update_activity/<int:pk>/', views.update_activity, name="update_activity"),
    path('delete_activity/<int:pk>/', views.delete_activity, name="delete_activity"),
    path('list_activity/<int:pk>/<int:ctr>/', views.list_activity, name="list_activity"),
    path('add_topik/<int:pk>/', views.add_topik, name="add_topik"),
    path('delete_topik/<int:pk1>/<int:pk2>/', views.delete_topik, name="delete_topik"),
    path('masukkan_topik/<int:pk1>/<int:pk2>/', views.masukkan_topik, name="masukkan_topik"),
    path('hapus_topik/<int:pk1>/<int:pk2>/', views.hapus_topik, name="hapus_topik"),
    path('topik_expired_check/', views.topik_expired_check, name="topik_expired_check"),
    path('list_open_pica/', views.list_open_pica, name="list_open_pica"),
    path('search_topik/', views.search_topik, name="search_topik"),
    path('search_all/', views.search_all, name="search_all"),
    path('notify_all/', views.notify_all, name="notify_all"),
]
