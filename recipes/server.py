from flask_app import app
from flask_app.controllers import accountss
from flask_app.controllers import recipes


if __name__ == "__main__":
    app.run(debug=True)