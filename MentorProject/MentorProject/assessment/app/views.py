import datetime
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.decorators import api_view
from .utils import generate_jwt_token
from .models import *
from .serializer import RegistrationSerializer,MentorSerializer,QuestionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .message_code import *
import logging
logger = logging.getLogger(__name__)


@api_view(['POST', ])
@permission_required([IsAuthenticated])
def Mentor_register(request):
    """
        This API use for Register_mentor
        Request parameter:->{"email": "salman.k@gmail.com",
                            "password": "Salman@!@#2",
                            "password2": "Salman@!@#2",
                            "role": "mentor"
                            }
        RETURN:->
        {
        "message": "User registered successfully",
        "status": 200,
        "result": {
            "email": "demo20fyeh@gmail.com",
            "role": "mentor"
            }
        }

    """
    logger_user_id = request.META['REMOTE_ADDR']
    logger.debug("[" + str(logger_user_id) + "][Mentor_register][POST]Entered" + f'Request Parameter:{request.data}')
    try:
        role = request.data.get("role") or None
        if role:
            if role == "mentor":
                serializer = MentorSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({"message": SUCCESS_REGISTERED_SUCCESSFULLY,
                                     "status": status.HTTP_200_OK,
                                     "result": {"email": user.email, "role": user.role}}, status=status.HTTP_200_OK)
                else:
                    error_list = [serializer.errors[error][0] for error in serializer.errors][0]
                    return Response({"message": error_list, "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": PROVIDE_CORRECT_ROLE, "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": PROVIDE_CORRECT_ROLE, "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("[" + logger_user_id + "][Mentor_register][GET]Error Occurred " + str(e))
        return Response({"message": ERROR_TECHNICAL, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_required([IsAuthenticated])
def Student_register(request):
    """
        This API use for Register_student
        Request parameter:-> {
                            "student_email": "saman.m@gmail.com",
                            "password": "salman@!12",
                            "password2": "salman@!12",
                            "mentor_email": "salman.k@gmail.com",
                            "role": "student"
                            }
        RETURN:->
        {
        "message": "User registered successfully",
        "status": 200,
        "result": {
            "email": "salman11SS7sr2@gmail.com",
            "role": "student"
            }
        }

    """
    logger_user_id = request.META['REMOTE_ADDR']
    logger.debug("[" + str(logger_user_id) + "][Student_register][POST]Entered" + f'Request Parameter:{request.data}')
    try:
        role = request.data.get("role") or None
        if request.user.is_authenticated:
            if role:
                value = None
                if role == "student":
                    value = RegistrationSerializer
                if value:
                    email = request.data.get("mentor_email") or None
                    mentor = Mentor.objects.get(email=email)
                    data = {"mentor": mentor.pk,
                            "email": request.data.get("student_email"),
                            "password": request.data.get("password"),
                            "password2": request.data.get("password2"),
                            "mentor_email": email,
                            "role": "student"}
                    serializer = value(data=data)
                    if serializer.is_valid():
                        user = serializer.save()
                        return Response({"message": SUCCESS_REGISTERED_SUCCESSFULLY,"status": status.HTTP_200_OK,
                                         "result": {"email": user.email, "role": user.role}}, status=status.HTTP_200_OK)
                    else:
                        error_list = [serializer.errors[error][0] for error in serializer.errors][0]
                        return Response({"message": error_list, "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": PROVIDE_CORRECT_ROLE_STUDENT, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": PROVIDE_CORRECT_ROLE_STUDENT, "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": LOGIN_FIRST, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("[" + logger_user_id + "][Student_register][POST]Error Occurred " + str(e))
        return Response({"message": ERROR_TECHNICAL, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_required([IsAuthenticated])
def User_login(request):
    """
            This API use for Register_mentor
            Request parameter:-> {
                                "email": "salmanmohdk83@gmail.com",
                                "password": "Salman@!2",
                                "role": "mentor"
                                }
            RETURN:->
                {
                "message": "User logged in successfully",
                "status": 200,
                "result": {
                "user_email": "demo234@gmail.com",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNjM5NjYxNzQwfQ.k9dTYLgIZ1juwn-DxOl_ZR85U7R1tHoS3kj8KQ3akXQ",
                "login_time": "09 Dec 2021 13:35 PM",
                "registration_date": "09 Dec 2021 09:56 AM"
                }
            }
        """
    logger_user_id = request.META['REMOTE_ADDR']
    logger.debug("[" + str(logger_user_id) + "][User_login][POST]Entered" + f'Request Parameter:{request.data}')
    try:
        email = request.data.get("email") or None
        password = request.data.get("password") or None
        role = request.data.get("role") or None
        if email and password:
            value = None
            if role == "mentor":
                value = Mentor
            elif role == "student":
                value = NewUser
            if value:
                try:
                    user = value.objects.get(email=email)
                    if check_password(password, user.password):
                        auth.login(request, user)
                        data = {"user_email": user.email, "token": generate_jwt_token(user), "login_time": datetime.now().strftime('%d %b %Y %H:%M %p'),
                                "registration_date": user.registration_date.strftime('%d %b %Y %H:%M %p')}
                        return Response({"message": LOGGED_SUCCESSFULLY, "status": status.HTTP_200_OK,
                                         "result": data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": INVALID_PASSWORD, "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error("[" + logger_user_id + "][User_login][POST]Error Occurred " + str(e))
                    return Response({"message": INVALID_USERNAME, "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": CHECK_PERMISSION_ROLE, "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": REQUEST_PARAMETER, "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("[" + logger_user_id + "][User_login][POST]Error Occurred " + str(e))
        return Response({"message": ERROR_TECHNICAL, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@login_required(login_url='/app/user_login/')
@permission_required([IsAuthenticated])
def post_questions(request):
    """
            This API use for Register_student
            Request parameter:-> {
                                 "student_email": "salmanmohdk83@gmail.com",
                                "mentor_email": "salman.m@gmail.com",
                                "question": "What is Meta data",
                                "message": ""
             }
            RETURN:->
            {
             "message": "Query saved successfully",
            "status": 200,
            "result": {
                    "question": "Good questions",
                    "student_email": "salman1172@gmail.com",
                    "mentor_email": "salmanmohdk83@gmail.com"
                    }
            }
    """
    logger_user_id = request.META['REMOTE_ADDR']
    logger.debug("[" + str(logger_user_id) + "][post_question][POST]Entered" + f'Request Parameter:{request.data}')
    try:
        student_email = request.data.get("student_email") or None
        mentor_email = request.data.get("mentor_email") or None
        question = request.data.get("question") or None
        message = request.data.get("message") or None
        file = request.FILES.get("file") or None
        if request.user.is_authenticated:
            if student_email and question:
                try:
                    user = NewUser.objects.get(email=student_email)
                    mentor = Mentor.objects.get(email=mentor_email)
                    dict_value = {"mentor": mentor.pk, "user": user.pk, "question": question, "message": message,
                             "reply": None, "file_name": file.name if file else None,
                             "file": file, "post_time": datetime.now(), "replied_time": None}
                    serializer = QuestionSerializer(data=dict_value)
                    if serializer.is_valid():
                        data = serializer.save()
                        return Response({"message": SAVED_SUCCESSFULLY, "status": status.HTTP_200_OK,
                                         "result": {"question": data.question, "student_email": data.user.email,
                                            "mentor_email": data.mentor.email }}, status=status.HTTP_200_OK)
                    else:
                        error_list = [serializer.errors[error][0] for error in serializer.errors][0]
                        return Response({"message": error_list, "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error("[" + logger_user_id + "][post_question][POST]Error Occurred " + str(e))
                    return Response({"message": USER_NOT_FOUND, "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": REQUEST_PARAMETER, "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": LOGIN_FIRST, "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("[" + logger_user_id + "][post_question][POST]Error Occurred " + str(e))
        return Response({"message": ERROR_TECHNICAL, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@login_required(login_url='/app/user_login/')
@permission_required([IsAuthenticated])
def all_questions(request):
    """
            This API use for Register_student
            Request parameter:-> {
                                    "email": "salmanmohdk83@gmail.com"
                                    "role": "mentor"
                                }
            RETURN:->
            {
                "message": "Data Retrieved successfully",
                "status": 200,
                "result": [
                        {
                        "student_email": "salman1172@gmail.com",
                        "mentor_email": "salmanmohdk83@gmail.com",
                        "question": "what is Meta data",
                        "reply": null,
                        "attachment_name": null
                        },
                        {
                        "student_email": "salman1172@gmail.com",
                        "mentor_email": "salmanmohdk83@gmail.com",
                        "question": "data about data",
                        "reply": null,
                        "attachment_name": null
                        },
                        {
                        "student_email": "salman1172@gmail.com",
                        "mentor_email": "salmanmohdk83@gmail.com",
                        "question": "Good questions",
                        "reply": null,
                        "attachment_name": null
                        }
                    ]
            }
                    """
    logger_user_id = request.META['REMOTE_ADDR']
    logger.debug("[" + str(logger_user_id) + "][all_questions][POST]Entered" + f'Request Parameter:{request.data}')
    try:
        email = request.data.get("email") or None
        role = request.data.get("role") or None
        if request.user.is_authenticated:
            questions = None
            if role == "mentor":
                mentor = Mentor.objects.get(email=email)
                questions = Questions.objects.filter(mentor=mentor)
            elif role == "student":
                user = NewUser.objects.get(email=email)
                questions = Questions.objects.filter(user=user)
            if questions:
                question_list = []
                for question in questions:
                    data = {"student_email": question.user.email, "mentor_email": question.mentor.email,
                            "question": question.question, "reply": question.reply, "attachment_name": question.file_name}
                    question_list.append(data)
                if question_list:
                    return Response({"message": SUCCESS_DATA_RETRIEVED, "status": status.HTTP_200_OK,
                                     "result": question_list}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": DATA_NOT_FOUND, "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": NO_DATA_ASSOCIATED, "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": LOGIN_FIRST, "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("[" + logger_user_id + "][all_questions][POST]Error Occurred " + str(e))
        return Response({"message": ERROR_TECHNICAL, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@login_required(login_url='/app/login_user/')
@permission_required(['app.reply_question', IsAuthenticated])
def questions_reply(request):
    """
                This API use for Register_student
                Request parameter:-> {
                            "student_email": "salmanmohdk83@gmail.com",
                            "mentor_email": "salman.m@gmail.com",
                            "question": "What is Meta data",
                            "reply": "Data about data",
                            "role": "mentor",
                            "message": ""

                            }
                RETURN:->
                {
                 "message": "Query saved successfully",
                "status": 200,
                "result": {
                            ""

                            }
                }
        """
    logger_user_id = request.META['REMOTE_ADDR']
    logger.debug("[" + str(logger_user_id) + "][questions_reply][POST]Entered" + f'Request Parameter:{request.data}')
    try:
        student_email = request.data.get("student_email") or None
        mentor_email = request.data.get("mentor_email") or None
        question = request.data.get("question") or None
        reply = request.data.get("reply") or None
        role = request.data.get("role") or None
        message = request.data.get("message") or None
        file = request.FILES.get("file") or None
        if request.user.is_authenticated:
            if role == "mentor":
                if student_email and mentor_email and question and reply:
                    try:
                        user = NewUser.objects.get(email=student_email)
                        mentor = Mentor.objects.get(email=mentor_email)
                        question_data = Questions.objects.get(user=user, mentor=mentor, question__exact=question)
                        question_data.reply = reply
                        question_data.message = message
                        question_data.reply_time = datetime.now()
                        question_data.file_name = file.name if file else None
                        question_data.file = file
                        question_data.save()
                        return Response({"message": REPLIED_SUCCESSFULY, "status": status.HTTP_200_OK,
                                         "result": {"student": user.email, "mentor": mentor.email, "question": question,
                                            "reply": reply}}, status=status.HTTP_200_OK)
                    except Exception as e:
                        logger.error("[" + logger_user_id + "][questions_reply][POST]Error Occurred " + str(e))
                        return Response({"message": USER_NOT_FOUND, "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": REQUEST_PARAMETER, "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": CAN_NOT_REPLY_QUESTIONS, "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": LOGIN_FIRST, "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("[" + logger_user_id + "][questions_reply][POST]Error Occurred " + str(e))
        return Response({"message": ERROR_TECHNICAL, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
