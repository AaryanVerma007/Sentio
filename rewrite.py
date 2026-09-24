import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert imports and DB setup
import_block = """from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth
from functools import wraps
import uuid

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "fallback_dev_secret_key_change_in_prod")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)
    auth_provider = db.Column(db.String(50), default='email')
    provider_user_id = db.Column(db.String(150), nullable=True)
    role = db.Column(db.String(50), default='USER')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'ADMIN':
            return jsonify({"status": "error", "message": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function

with app.app_context():
    db.create_all()

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "mock_google_id"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "mock_google_secret"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='facebook',
    client_id=os.environ.get("FACEBOOK_APP_ID", "mock_facebook_id"),
    client_secret=os.environ.get("FACEBOOK_APP_SECRET", "mock_facebook_secret"),
    access_token_url='https://graph.facebook.com/v11.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v11.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v11.0/',
    client_kwargs={'scope': 'email public_profile'}
)
"""
content = content.replace("app = Flask(__name__)\nCORS(app)", import_block)

# 2. Add New Auth API Endpoints
auth_endpoints = """
@app.route('/api/auth/signup', methods=['POST'])
def auth_signup():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required"}), 400
        
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"status": "error", "message": "Email already registered"}), 400
        
    new_user = User(
        email=email,
        name=name,
        password_hash=generate_password_hash(password),
        auth_provider='email',
        role='ADMIN' if email == 'sentio1508@gmail.com' else 'USER'
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Signup successful"}), 201

@app.route('/api/auth/login', methods=['POST'])
def auth_login_local():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    user = User.query.filter_by(email=email).first()
    if user and user.password_hash and check_password_hash(user.password_hash, password):
        if not user.is_active:
            return jsonify({"status": "error", "message": "Account is deactivated"}), 403
        
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        login_user(user)
        return jsonify({
            "status": "success", 
            "user": {"email": user.email, "role": user.role, "name": user.name}
        }), 200
        
    return jsonify({"status": "error", "message": "Invalid email or password"}), 401

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def auth_logout():
    logout_user()
    return jsonify({"status": "success", "message": "Logged out successfully"}), 200

@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    if current_user.is_authenticated:
        return jsonify({
            "status": "success",
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
                "role": current_user.role,
                "provider": current_user.auth_provider
            }
        }), 200
    return jsonify({"status": "error", "message": "Not authenticated"}), 401

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def admin_users():
    users = User.query.all()
    users_data = []
    for u in users:
        users_data.append({
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "role": u.role,
            "provider": u.auth_provider,
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None
        })
    return jsonify({"status": "success", "users": users_data}), 200

"""

# 3. Replace old OAuth Routes
oauth_replacement = """
@app.route('/auth/<provider>/login')
def auth_login(provider):
    if provider not in ['google', 'facebook']:
        return jsonify({"status": "error", "message": "Invalid provider"}), 400
        
    client = oauth.create_client(provider)
    redirect_uri = url_for('auth_callback', provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri)

@app.route('/auth/<provider>/callback')
def auth_callback(provider):
    if provider not in ['google', 'facebook']:
        return redirect("/?error=oauth_invalid_provider")
        
    client = oauth.create_client(provider)
    try:
        token = client.authorize_access_token()
        
        if provider == 'google':
            user_info = client.parse_id_token(token)
            email = user_info.get('email')
            name = user_info.get('name')
            provider_id = user_info.get('sub')
        elif provider == 'facebook':
            resp = client.get('me?fields=id,name,email')
            user_info = resp.json()
            email = user_info.get('email')
            name = user_info.get('name')
            provider_id = user_info.get('id')
            
        if not email:
            return redirect("/?error=oauth_missing_email")
            
        # Account Linking or Creation
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                name=name,
                auth_provider=provider,
                provider_user_id=provider_id,
                role='ADMIN' if email == 'sentio1508@gmail.com' else 'USER'
            )
            db.session.add(user)
        else:
            # Update provider info if needed (naive account linking)
            user.auth_provider = provider
            user.provider_user_id = provider_id
            
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        if not user.is_active:
            return redirect("/?error=account_deactivated")
            
        login_user(user)
        return redirect("/")
        
    except Exception as e:
        print(f"OAuth Callback Error: {e}")
        return redirect("/?error=oauth_callback_failed")
"""

# Regex to replace the old /auth/<provider>/login and callback completely
import re
pattern = re.compile(r"@app\.route\('/auth/<provider>/login'\).*?Error exchanging code.*?return redirect\(\"/\?error=oauth_callback_failed\"\)", re.DOTALL)
content = pattern.sub(auth_endpoints + oauth_replacement, content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app.py")
