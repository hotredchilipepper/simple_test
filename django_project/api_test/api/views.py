from .models import Question, Users
from .serializers import UsersSerializer, QuestionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
import requests



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ для подписи токенов JWT.
SECRET_KEY = "b40ae6ced3498334c2d4a536e784769abf5481033a48e38430f95e298fc2b7a4"


# Алгоритм для подписи токенов JWT.
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 300


# Создание токена доступа jwt.
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class RegisterAPIView(APIView):

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email is None:
            return Response({'status': '0', 'data': '404'})
        if password is None:
            return Response({'status': '0', 'data': '404'})
        try:
            check_user = Users.objects.get(email=email)
            return Response({'status': '2','data': 'Пользователь с такой почтой уже существует'})
        except:
            hash_pass = pwd_context.hash(password)
            user = Users.objects.create(
                email = email,
                hash_pass = hash_pass
            )
            return Response({'status': '1', 'data': 'Успешная регистрация'})


class LoginAPIView(APIView):

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email is None:
            return Response({'status': '0', 'data': '404'})
        if password is None:
            return Response({'status': '0', 'data': '404'})
        try:
            check_user = Users.objects.get(email=email)
        except:
            return Response({'status': '0', 'data': 'Пользоавтеля с такой почтой не существует'})
        check_pass = pwd_context.verify(password, check_user.hash_pass)
        if check_pass is False:
            return Response({'status': '2', 'data': 'Пароль неверный'})
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return Response({'status': '1','data': {'token': access_token}})


class QuestionListAPIView(APIView):

    def post(self, request):
        token = request.data.get('token', None)
        question = request.data.get('question', None)
        if token is None:
            return Response({'status': '0', 'data': '404'})
        if question is None:
            return Response({'status': '0', 'data': '404'})
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise Http404
        except JWTError:
            raise Http404

        try:
            check_user = Users.objects.get(email=email)
        except:
            return Response({'status': '0', 'data': 'Пользоавтеля с такой почтой не существует'})
        
        # Запрос к сервису yesno.wtf
        
        response = requests.get('https://yesno.wtf/api/').json()['answer']

        new_question = Question.objects.create(
            email = email,
            question = question,
            answer = response
        )
        return Response({'status': '1', 'data': {'question': question, 'answer': response}})