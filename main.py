from flask import Flask
from flask_login import LoginManager
from models.user_login import UserLogin
from core.db import get_connection
from blueprints.api import api_blueprint

app = Flask(__name__)
app.secret_key = 'super secret key'
loging_manager = LoginManager(app)


@loging_manager.user_loader
def load_user(user_login):
    with get_connection() as conn:
        return UserLogin().fromDB(user_login, conn)


app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
