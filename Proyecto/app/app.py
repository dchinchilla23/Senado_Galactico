from app.routes import bp

app = Flask(__name__)
app.register_blueprint(bp)
