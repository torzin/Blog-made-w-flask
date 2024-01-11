from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import RegisterForm, CreatePostForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DATABASENAME.db"
app.config['SECRET_KEY'] = "YOUR SECRET KEY"
Bootstrap(app)
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)


# CONFIG. DATABASE
db = SQLAlchemy(app)


class Author(db.Model, UserMixin):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)


class Posts(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer,unique=False, nullable=False)

    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Author, user_id)


@app.route('/')
def home():

    posts = Posts.query.all()
    return render_template('index.html', all_posts=posts, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = Author.query.filter_by(email=email).first()
        if not user:
            flash("Incorrect credentials")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Incorrect credentials")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form, current_user=current_user)



@app.route('/register', methods=['POST', 'GET'])
def register():

    form = RegisterForm()
    if request.method == "POST":
        password_hash = generate_password_hash(
            request.form.get('password'),
            method="YOUR METHOD HERE",
            salt_length=16
        )
        new_user = Author(
            name=request.form.get('name'),
            password=password_hash,
            email=request.form.get('email')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = CreatePostForm()

    if request.method == "POST":
        new_post = Posts(
            title=request.form.get('title'),
            content=form.content.data,
            author_id=current_user.id,
            description=request.form.get('description')
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('see_post', post_id=new_post.id))
    return render_template('create_post_page.html', form=form)

''
@app.route('/see_post/<int:post_id>', methods=['GET'])
def see_post(post_id):
    requested_post = db.session.get(Posts, post_id)
    user_author = db.session.get(Author, (db.session.get(Posts, post_id).author_id)).name
    print(type(requested_post.content))

    return render_template('post.html', post=requested_post, user_author=user_author)


@app.route('/delete_post/<int:post_id>', methods=["GET"])
@login_required
def delete_post(post_id):
    post_to_delete = Posts.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
