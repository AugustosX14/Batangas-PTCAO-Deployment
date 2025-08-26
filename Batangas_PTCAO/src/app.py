# File: /Users/antonio/Documents/development_folder/Batangas_PTCAO/Batangas_PTCAO/src/app.py
import os
from flask import Flask, render_template, send_from_directory
from config import Config
from extension import db, bcrypt, jwt
from model import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'events'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'destinations'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'properties'), exist_ok=True)
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.TOURIST_Home import tourist_home_bp
    from routes.TOURIST_Destination import tourist_api_bp
    from routes.TOURIST_Map import tourist_map_bp
    from routes.TOURIST_Events import tourist_events_bp
    from routes.MTO import mto_bp
    from routes.MTO_Dashboard import dashboard_bp
    from routes.MTO_Destinations import destinations_bp
    from routes.MTO_Property import properties_bp
    from routes.MTO_Events import events_bp
    from routes.MTO_Analytics import analytics_bp
    from routes.MTO_VisitorsRecords import visitor_records_bp
    from routes.MTO_Announcement import announcement_bp
    from routes.MTO_Reports import reports_bp
    from routes.PTCAO_Dashboard import ptcao_dashboard_bp
    from routes.PTCAO_Destinations import ptcao_destinations_bp
    from routes.PTCAO_Property import ptcao_properties_bp
    from routes.ADMIN_dashboard import admin_dashboard_bp
    from routes.ADMIN_users import admin_users_bp
    from routes.ADMIN_reports import admin_reports_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tourist_home_bp)
    app.register_blueprint(tourist_api_bp)
    app.register_blueprint(tourist_map_bp)
    app.register_blueprint(tourist_events_bp)
    app.register_blueprint(mto_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(visitor_records_bp)
    app.register_blueprint(announcement_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(ptcao_dashboard_bp)
    app.register_blueprint(ptcao_destinations_bp)
    app.register_blueprint(ptcao_properties_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_reports_bp)
    
    # Static file serving
    @app.route('/static/<path:filename>')
    def serve_static_file(filename):
        return send_from_directory('static', filename)
    
    # Root route
    @app.route('/')
    def index():
        return render_template('TOURIST_Home.html')
    
    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    return app

# Create the app
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
