from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User, db

bp = Blueprint('auth', __name__)

#___REGISTER

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400
    
    if User.query.filter_by(email=email).first(): # Checking if the email already exists
        return jsonify({"msg": "Email already exists"}), 400
    
    user = User(
        name=name,
        email=email
    )

    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'result': 'Register success'}), 201


#___Login

@bp.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()

    if not data:
        return jsonify({"msg":"No JSON data"}),400
    
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    
    if user is None or not user.check_password(password):  # Password verification
        return jsonify({"msg": "Bad username or password"}), 401

    # Convert the ObjectId to a string
    user_id_str = str(user.user_id)
    
    return jsonify({
        "access_token": create_access_token(identity=str(user.user_id)),
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email
    }), 200

#___Check Auth

@bp.route('/checkAuth', methods=['GET'])
@jwt_required()  # Verify that the user is logged in

def check_auth():
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "notify_days_before": user.notify_days_before
    }), 200

#__log out


@bp.route('/logout', methods=['POST'])
@jwt_required()  # Verify that the user is logged in
def logout():
    
    return jsonify({"msg": "Successfully logged out"}), 200

#__Update Profile

@bp.route('/updateProfile', methods=['PATCH'])
@jwt_required()
def update_profile():
    data = request.get_json()
    
    if not data:
        return jsonify({
            "msg":"No JSON data"
    }),400

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if "name" in data:
        user.name = data["name"]

    if "notify_days_before" in data:
        user.notify_days_before = data["notify_days_before"]

    db.session.commit()

    return jsonify({
        "msg": "Profile updated successfully"
    }), 200

