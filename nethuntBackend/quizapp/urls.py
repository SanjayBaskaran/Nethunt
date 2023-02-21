from django.urls import path
from . import views
urlpatterns = [
    path("config", views.is_configured),
    path("get_questions", views.get_questions),
    path("set_config", views.add_config),
    path("add_question",views.add_question),
    path("startBy",views.get_startDate),
    path("endBy",views.get_endDate),
    # path("bottest",views.get_log)
]
