from django.urls import path
from . import views


app_name="polls"
urlpatterns=[
    path('',views.index,name='index'),
    path('<int:question_id>/details',views.details,name='details'),
    path('<int:question_id>/results', views.results,name='results'),
    path('<int:question_id>/vote',views.vote,name='vote'),
    path('<int:question_id>/delete_question',views.delete_question,name='delete_question'),
    path('add_question',views.add_question,name="add_question"),
    path('update_question/<int:question_id>/',views.update_question,name='update_question'),
    path('login/',views.login_page,name='login_page'),
    path('thanks/',views.thanks,name="thanks"),
    path('add_user/',views.add_user,name="add_user"),
]