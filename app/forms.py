from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class IdeaForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])
    summary = TextAreaField('概要')
    status = SelectField('ステータス', choices=[
        ('検討中', '検討中'),
        ('開発中', '開発中'),
        ('完了', '完了')
    ])
    submit = SubmitField('保存')


class SignupForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    confirm_password = PasswordField('パスワード（確認）', validators=[
        DataRequired(), EqualTo('password', message='パスワードが一致しません')
    ])
    submit = SubmitField('登録')

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')
