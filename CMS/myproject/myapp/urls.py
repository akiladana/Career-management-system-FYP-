from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('rankingList', views.ranking_List, name='rankingList'),
    # path('form', views.generate_cv, name='form'),
    # path('generate-cv/', views.generate_cv, name='generate_cv'),
    path('mainFront', views.mainFront, name='mainFront'),
    path('suggestionList', views.suggestion_List, name='suggesionList'),
    path('gitdetail', views.gitdetail, name='gitdetail'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('jobposting', views.jobposting, name='jobposting'),
    # path('mainb', views.rankingList, name='ranking_list'),
    path('process/', views.ranking_List, name='process_selection'),
    path('get_user_info/<str:username>/', views.get_user_info, name='get_user_info'),
    path('suggestion-list/', views.suggestion_List, name='suggestionList'),
    path('create_job/', views.create_job, name='create_job'),
    # path('admin/', admin.site.urls),
    # path('myproject/', include('myproject.urls')),
    path('selectOption', views.selectOption, name='selectOption'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('testJb', views.testJb, name='testJb'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)