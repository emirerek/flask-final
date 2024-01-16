from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from os import path

app = Flask(__name__)
app_dir = path.abspath(path.dirname(__file__))
src_dir = path.join(app_dir, "..")
db_path = path.join(src_dir, "instance", "site.db")
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)

login_manager = LoginManager(app)
login_manager.init_app(app)
babel = Babel(app)
admin = Admin(app, name="Admin", template_mode="bootstrap3")

from app import views, models
from app.models import Project, User, Quote, Contact, BlogPost

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Quote, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(BlogPost, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))