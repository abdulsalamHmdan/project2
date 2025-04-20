from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path("result",views.result,name="result"),
    path("setp",views.setp,name="setp"),
    path("setlan",views.setlan,name="setlan"),
    path("lang",views.lang,name="lang"),
    # path("result",views.result.as_view())
]