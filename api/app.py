from flask import Flask
from routes.health import health_bp
from routes.predict import predict_bp
from routes.model_info import model_info_bp
from routes.login import login_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(model_info_bp)
    app.register_blueprint(login_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)