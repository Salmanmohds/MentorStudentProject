from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path('mentor_register/', Mentor_register, name='mentor_register'),
    path('student_register/', Student_register, name='student_register'),
    path('user_login/', User_login, name='user_login'),
    path('post_question/', post_questions, name='post_question'),
    path('all_questions/', all_questions, name='all_questions'),
    path('question_reply/', questions_reply, name='question_reply'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
