# Batangas PTCAO Tourism Management System

A comprehensive web application for managing tourism properties, events, destinations, and visitor records in Batangas Province, Philippines.

## 🏗️ System Architecture

This Flask-based web application serves multiple user types:
- **Tourists**: Browse destinations, events, and accommodations
- **MTO (Municipal Tourism Officers)**: Manage local tourism data and visitor records  
- **PTCAO (Provincial Tourism, Culture & Arts Office)**: Provincial-level oversight and reporting
- **Administrators**: System administration and user management

## 🚀 Features

### Tourist Features
- Browse destinations and accommodations
- View upcoming events and activities
- Interactive map of tourist spots
- Contact and about information

### MTO Features  
- Dashboard with analytics and visitor statistics
- Manage tourism properties and accommodations
- Create and manage events
- Upload visitor records via Excel/CSV
- Generate reports and announcements
- Track DOT accreditation and PTCAO registration

### PTCAO Features
- Provincial dashboard with aggregated data
- Manage destinations across municipalities  
- Property oversight and reporting
- Provincial-level analytics

### Administrator Features
- User management and account activation
- System-wide reporting
- Platform administration

## 🛠️ Technology Stack

**Backend:**
- **Python 3.11.10** (Required for Render deployment)
- **Flask 2.3.3** - Web framework
- **SQLAlchemy 3.0.5** - Database ORM
- **PostgreSQL** - Database (via psycopg2-binary)
- **Flask-JWT-Extended** - Authentication
- **Flask-Bcrypt** - Password hashing
- **Pandas 2.0.3** - Data processing for Excel/CSV uploads

**Frontend:**
- HTML5 with Jinja2 templates
- CSS3 for styling
- JavaScript for interactivity

**Deployment:**
- **Render.com** - Cloud platform
- **Gunicorn** - WSGI server
- **Blueprint** - Infrastructure as code

## 📋 Prerequisites

### Local Development
- Python 3.10+ (3.11 recommended)
- PostgreSQL 12+
- pip (Python package manager)
- Git

### Production Deployment
- GitHub account
- Render.com account
- PostgreSQL database (Render provides free tier)

## 🔧 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AugustosX14/Batangas-PTCAO-Deployment.git
cd Batangas-PTCAO-Deployment
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
cd Batangas_PTCAO
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Install PostgreSQL and create database
createdb batangas_ptcao

# Or use PostgreSQL commands:
psql -U postgres
CREATE DATABASE batangas_ptcao;
\q
```

### 5. Environment Configuration
Create a `.env` file in the `Batangas_PTCAO/src/` directory:
```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost/batangas_ptcao

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### 6. Initialize Database
```bash
cd src
python -c "from app import app; from extension import db; app.app_context().push(); db.create_all()"
```

### 7. Run the Application
```bash
cd src
python app.py
```

The application will be available at `http://localhost:5000`

## 🚢 Production Deployment (Render.com)

### Deployment Configuration Files

The project includes these deployment configuration files:

#### `render.yaml` - Blueprint Configuration
```yaml
databases:
  - name: batangas-ptcao-db
    databaseName: ptcao_db
    user: ptcao_user
    plan: free

services:
  - type: web
    name: batangas-ptcao-app
    runtime: python
    buildCommand: |
      cd Batangas_PTCAO
      pip install -r requirements.txt
    startCommand: |
      cd Batangas_PTCAO/src
      python app.py
    plan: free
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.10
      - key: DATABASE_URL
        fromDatabase:
          name: batangas-ptcao-db
          property: connectionString
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
```

#### `Batangas_PTCAO/runtime.txt` - Python Version
```
python-3.11.10
```

#### `Batangas_PTCAO/requirements.txt` - Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Bcrypt==1.0.1
Flask-WTF==1.1.1
Flask-JWT-Extended==4.5.2
psycopg2-binary==2.9.7
python-dotenv==1.0.0
pandas==2.0.3
gunicorn==21.2.0
Werkzeug==2.3.7
```

### Deployment Steps

1. **Fork the Repository** (if not already done)
   - Fork `https://github.com/AugustosX14/Batangas-PTCAO-Deployment.git`

2. **Connect to Render**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub account

3. **Create Blueprint**
   - In Render Dashboard, click "New" → "Blueprint"
   - Connect to your forked repository
   - Render will read the `render.yaml` file automatically

4. **Deploy**
   - Click "Create" to deploy the blueprint
   - Render will:
     - Create a PostgreSQL database
     - Build and deploy the web service
     - Set up environment variables automatically

5. **Auto-Deploy**
   - Any push to the `master` branch will trigger automatic deployment
   - Monitor deployment in the Render Dashboard

### Environment Variables (Set Automatically)
- `PYTHON_VERSION`: 3.11.10
- `DATABASE_URL`: Generated by Render database
- `FLASK_ENV`: production  
- `SECRET_KEY`: Auto-generated by Render

## 📁 Project Structure

```
Batangas_PTCAO/
├── src/
│   ├── app.py                 # Main Flask application
│   ├── config.py             # Configuration settings
│   ├── extension.py          # Flask extensions (SQLAlchemy, JWT, Bcrypt)
│   ├── model.py              # Database models
│   ├── main.py               # Simple entry point
│   ├── routes/               # Blueprint route handlers
│   │   ├── auth.py           # Authentication routes
│   │   ├── TOURIST_*.py      # Tourist-facing routes
│   │   ├── MTO_*.py          # MTO dashboard routes
│   │   ├── PTCAO_*.py        # PTCAO dashboard routes
│   │   └── ADMIN_*.py        # Admin routes
│   ├── templates/            # Jinja2 HTML templates
│   ├── static/               # CSS, images, uploads
│   │   ├── css/
│   │   ├── img/
│   │   └── uploads/          # User uploaded files
│   ├── resources/            # SQL files and maps
│   └── tests/                # Unit tests
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version for Render
└── uploads/                 # Upload directory
render.yaml                  # Render deployment blueprint
runtime.txt                  # Python version (root level)
README.md                    # This documentation
```

## 🔐 Default User Accounts

After deployment, you'll need to create admin users through the registration system or database seeding.

## 🧪 Testing

Run the test suite:
```bash
cd Batangas_PTCAO/src
python -m pytest tests/
```

## 🛠️ Common Development Tasks

### Adding New Routes
1. Create route file in `src/routes/`
2. Define blueprint and routes
3. Register blueprint in `src/app.py`

### Database Migrations
```bash
# After model changes
cd src
python -c "from app import app; from extension import db; app.app_context().push(); db.drop_all(); db.create_all()"
```

### File Uploads
The system supports Excel/CSV uploads for:
- Visitor records (MTO Dashboard)
- Property reports (MTO Reports)
- Tourist reports (MTO Reports)

## 🐛 Troubleshooting

### Local Development Issues

**Database Connection Error:**
```bash
# Check PostgreSQL is running
pg_isready

# Verify database exists
psql -U postgres -l | grep batangas_ptcao
```

**Import Errors:**
```bash
# Ensure you're in the correct directory
cd Batangas_PTCAO/src
python app.py
```

### Deployment Issues

**Python Version Conflicts:**
- Ensure `runtime.txt` contains `python-3.11.10`
- Check `PYTHON_VERSION` environment variable is set to `3.11.10`

**Pandas Compilation Errors:**
- Using pandas 2.0.3 (compatible with Python 3.11)
- Avoid Python 3.13 (pandas compatibility issues)

**Database Connection Issues:**
- Verify `DATABASE_URL` environment variable
- Check database service is running in Render Dashboard

## 📊 Monitoring and Logs

### Render Dashboard
- Monitor deployment status
- View application logs
- Check resource usage
- Manage environment variables

### Local Logs
```bash
# View Flask development logs
cd Batangas_PTCAO/src
FLASK_ENV=development python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📝 License

This project is proprietary software for Batangas Provincial Tourism, Culture & Arts Office.

## 📞 Support

For technical support or deployment issues:
- Create an issue in the GitHub repository
- Contact the development team
- Check Render documentation: https://render.com/docs

---

**Live Application:** https://batangas-ptcao-app.onrender.com  
**Repository:** https://github.com/AugustosX14/Batangas-PTCAO-Deployment  
**Deployment Platform:** Render.com
