from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import Project, Contact, Quote, User, BlogPost
from app.forms import LoginForm, RegisterForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/projects")
@app.route("/projects/<int:id>")
def projects(id=None):
    if id:
        project = Project.query.get(id)            
        return render_template("project.html", project=project)
    else:
        projects = Project.query.all()
        return render_template("projects.html", projects=projects)

@app.route("/blog")
@app.route("/blog/<int:id>")
def blog(id=None):
    if id:
        blog_post = BlogPost.query.get(id)            
        return render_template("blog-post.html", blog_post=blog_post)
    else:
        blog_posts = BlogPost.query.all()
        return render_template("blog.html", blog_posts=blog_posts)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        new_contact = Contact(
            name=name, 
            email=email, 
            subject=subject, 
            message=message
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for("contact"))
    
@app.route("/quote", methods=["POST"])
def quote():
    website = request.form.get("website")
    email = request.form.get("email")
    new_quote = Quote(
        email=email,
        website=website, 
    )
    db.session.add(new_quote)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('index'))
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)