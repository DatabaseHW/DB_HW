from ast import Num
from flask_wtf import FlaskForm
from more_itertools import quantify
from numpy import set_string_function
from wtforms import *
from wtforms.validators import *
from flask_wtf.file import *
from flask_uploads import UploadSet, IMAGES

class LoginForm(FlaskForm):
    account = StringField('account',validators=[DataRequired(message=u'帳號不可為空'), Length(max=64,message=u"帳號過長")])
    password = PasswordField('password', validators=[DataRequired(message=u'密碼不可為空')])
    submit = SubmitField('submit')

class RegisterForm(FlaskForm):
    name = StringField(u'名字',validators=[DataRequired(message=u'名字不可為空'), Regexp('[a-zA-Z]+',message="格式錯誤")])
    phonenumber = StringField(u'電話',validators=[DataRequired(message=u'電話號碼不可為空'),Regexp('[0-9]{10}',message="格式錯誤")])
    account = StringField(u'帳號',validators=[DataRequired(message=u'帳號不可為空'),Regexp('[a-zA-Z0-9]+',message="格式錯誤")])
    password = PasswordField(u'密碼',validators=[DataRequired(message=u'密碼不可為空'), Length(max=64,message=u"密碼過長"), Length(min=6,message=u"密碼過短"),Regexp('[a-zA-Z0-9]+',message="格式錯誤")])
    re_password = PasswordField(u'密碼驗證',validators=[EqualTo(u'password', message=u'密碼不匹配')])
    latitude = FloatField(u'緯度',validators=[InputRequired(message=u'緯度不可為空'), NumberRange(-90,90,message="格式錯誤"), DataRequired(message="格式錯誤")])
    longitude = FloatField(u'精度',validators=[InputRequired(message=u'經度不可為空'), NumberRange(-180,180,message="格式錯誤"), DataRequired(message="格式錯誤")])
    submit = SubmitField('submit')

class LocationForm(FlaskForm):
    latitude_modify = FloatField(u'緯度',validators=[InputRequired(message=u'緯度不可為空'), NumberRange(-90,90,message="格式錯誤"), DataRequired(message="格式錯誤")])
    longitude_modify = FloatField(u'精度',validators=[InputRequired(message=u'經度不可為空'), NumberRange(-180,180,message="格式錯誤"), DataRequired(message="格式錯誤")])
    location_submit = SubmitField('location_submit')

class RechargeForm(FlaskForm):
    recharge_addvalue = IntegerField(u'addvalue',validators=[DataRequired(message=u'儲值不可為空'), NumberRange(min=0,message="儲值不可為負")])
    recharge_submit = SubmitField('recharge_submit')

# class OrderCalcPriceForm(FlaskForm):
#     order_sid = StringField(u'order_sid')
#     order_calc_price_submit = SubmitField('order_calc_price_submit')

class OrderForm(FlaskForm):
    order_sid = StringField(u'order_sid')
    calcPrice_total = IntegerField('calcPrice_total')
    order_submit = SubmitField('order_submit')

# class MyOrderForm(FlaskForm):
#     my_order_submit = StringField('status')

class CancelMyOrderForm(FlaskForm):
    searchMyOrder_oid = StringField('searchMyOrder_oid')
    searchMyOrder_Cancel_submit = StringField('searchMyOrder_Cancel_submit')

class CancelShopOrderForm(FlaskForm):
    searchShopOrder_oid = StringField('searchShopOrder_oid')
    searchShopOrder_Cancel_submit = StringField('searchShopOrder_Cancel_submit')

class DoneShopOrderForm(FlaskForm):
    searchShopOrder_oid = StringField('searchShopOrder_oid')
    searchShopOrder_Done_submit = StringField('searchShopOrder_Done_submit')

class ShopForm(FlaskForm):
    name = StringField(u'名字',validators=[DataRequired(message=u'名字不可為空')])
    latitude = FloatField(u'緯度',validators=[InputRequired(message=u'緯度不可為空'), NumberRange(-90,90,message="格式錯誤"), DataRequired(message="格式錯誤")])
    longitude = FloatField(u'精度',validators=[InputRequired(message=u'經度不可為空'), NumberRange(-180,180,message="格式錯誤"), DataRequired(message="格式錯誤")])
    categorys = StringField(u'名字',validators=[DataRequired(message=u'名字不可為空')])
    Register_submit = SubmitField('Register_submit')

class ProductForm(FlaskForm):
    shop_name = StringField(u'商店名字',validators=[DataRequired(message=u'名字不可為空')])
    name = StringField(u'名字',validators=[DataRequired(message=u'名字不可為空')])
    quantity = IntegerField(u'數量',validators=[DataRequired(message=u'數量不可為空'), NumberRange(min=0, message="數量不可為負" )])
    price = IntegerField(u'價格',validators=[DataRequired(message=u'價格不可為空'), NumberRange(min=0, message="價格不可為負" )])
    picture = FileField(u'圖片', validators=[FileAllowed(UploadSet(extensions=IMAGES),message="格式錯誤，僅限上傳圖片檔")])
    Add_submit = SubmitField('Add_submit')

class DeleteForm(FlaskForm):
    delete_pid = StringField(u'delete_pid')
    Delete_submit = SubmitField('Delete_submit')

class ModifyForm(FlaskForm):
    modify_pid = StringField(u'modify_pid')
    quantity_modify = IntegerField(u'數量',validators=[DataRequired(message=u'數量不可為空'), NumberRange(min=0, message="數量不可為負" )])
    price_modify = IntegerField(u'價格',validators=[DataRequired(message=u'價格不可為空'), NumberRange(min=0, message="價格不可為負" )])
    Modify_submit = SubmitField('Modify_submit')
