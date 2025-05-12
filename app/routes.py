from flask import Blueprint, render_template, request, redirect, url_for
from .models import Idea, User
from .extensions import db
from .forms import IdeaForm, SignupForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.idea_list'))

@main.route('/ideas')
@login_required
def idea_list():
    status = request.args.get('status')  # ← クエリパラメータで取得
    query = Idea.query.filter_by(user_id=current_user.id)
    
    if status:  # ← statusが空じゃないときだけ追加フィルター
        query = query.filter_by(status=status)

    ideas = query.order_by(Idea.created_at.desc()).all()
    return render_template('ideas/list.html', ideas=ideas, selected_status=status)


@main.route('/ideas/new', methods=['GET', 'POST'])
@login_required
def new_idea():
    form = IdeaForm()
    if form.validate_on_submit():
        idea = Idea(
            title=form.title.data,
            summary=form.summary.data,
            status=form.status.data,
            user_id=current_user.id  
        )
        db.session.add(idea)
        db.session.commit()
        return redirect(url_for('main.idea_list'))
    return render_template('ideas/new.html', form=form)


@main.route('/ideas/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_idea(id):
    idea = Idea.query.get_or_404(id)
    form = IdeaForm(obj=idea)

    if form.validate_on_submit():
        idea.title = form.title.data
        idea.summary = form.summary.data
        idea.status = form.status.data
        db.session.commit()
        return redirect(url_for('main.idea_list'))

    return render_template('ideas/edit.html', form=form, idea=idea)

@main.route('/ideas/<int:id>/delete', methods=['POST'])
@login_required
def delete_idea(id):
    idea = Idea.query.get_or_404(id)
    db.session.delete(idea)
    db.session.commit()
    return redirect(url_for('main.idea_list'))


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    else:
        print(form.errors)  # ← エラー確認のために追加
    return render_template('ideas/signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.idea_list'))
        else:
            return "ユーザー名またはパスワードが間違っています", 401
    return render_template('ideas/login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


