from flask import Flask
from controller import wide_charController, boolController, errorController, timeController, unionController

app = Flask(__name__)
app.register_blueprint(wide_charController.bp)
app.register_blueprint(boolController.bp)
app.register_blueprint(errorController.bp)
app.register_blueprint(timeController.bp)
app.register_blueprint(unionController.bp)
if __name__ == "__main__":
    app.run()
