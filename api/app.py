from flask import Flask, request, jsonify
from routes.health import health_bp
from routes.predict import predict_bp
from routes.model_info import model_info_bp
from routes.login import login_bp
import logging, sys
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.before_request
def log_request():
    logger.info({
        "method": request.method,
        "path": request.path,
        "ip": request.remote_addr,
        "body": request.get_json(silent=True)
    })

app.register_blueprint(health_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(model_info_bp)
app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)