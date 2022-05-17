from ast import Num
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class LoginForm(FlaskForm):
    account = StringField('account',validators=[DataRequired(message=u'帳號不可為空'), Length(max=64,message=u"帳號過長")])
    password = PasswordField('password', validators=[DataRequired(message=u'密碼不可為空')])
    submit = SubmitField('submit')

class RegisterForm(FlaskForm):
    name = StringField(u'名字',validators=[DataRequired(message=u'名字不可為空'), Regexp('[a-zA-Z]+',message="格式錯誤")])
    phonenumber = StringField(u'電話',validators=[DataRequired(message=u'電話號碼不可為空'),Regexp('[0-9]{10}',message="格式錯誤")])
    account = StringField(u'帳號',validators=[DataRequired(message=u'帳號不可為空'),Regexp('[a-zA-Z0-9]+',message="格式錯誤")])
    password = StringField(u'密碼',validators=[DataRequired(message=u'密碼不可為空'), Length(max=64,message=u"密碼過長"), Length(min=6,message=u"密碼過短"),Regexp('[a-zA-Z0-9]+',message="格式錯誤")])
    re_password = StringField(u'密碼驗證',validators=[EqualTo(u'password', message=u'密碼不匹配')])
    latitude = FloatField(u'緯度',validators=[InputRequired(message=u'緯度不可為空'), NumberRange(-90,90,message="格式錯誤"), DataRequired(message="格式錯誤")])
    longitude = FloatField(u'精度',validators=[InputRequired(message=u'經度不可為空'), NumberRange(-180,180,message="格式錯誤"), DataRequired(message="格式錯誤")])
    submit = SubmitField('submit')