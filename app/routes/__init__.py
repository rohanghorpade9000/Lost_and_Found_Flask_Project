from app.routes.lost_routes import lost_bp
from app.routes.found_routes import found_bp
from app.routes.match_routes import match_bp
from app.routes.search_routes import search_bp
from app.routes.users_routes import users_bp

def init_routes(app):
    app.register_blueprint(lost_bp, url_prefix="/api")
    app.register_blueprint(found_bp, url_prefix="/api")
    app.register_blueprint(match_bp, url_prefix="/api")
    app.register_blueprint(search_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api")


