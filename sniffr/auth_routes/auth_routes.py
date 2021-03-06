from flask import Blueprint, request
from flask_cors import cross_origin
from sniffr.models import User, db, process_records

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__)

# Login route
@auth_bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    """When a correct email and password is given, provide a success prompt"""
    content = request.json
    email = content["email"]
    passwd = content["password"]

    # Make sure email and password are provided
    if email and passwd:
        result = db.session.query(User).filter_by(email=f"{email}").first()

        # Check that there is a valid result and a correct password
        if result and result.verify_password(password=passwd):
            return {
                "user_id": result.user_id,
                "username": result.username,
                "email": result.email,
            }

        else:
            return {"message": "fail"}, 400

    else:
        return {"message": "fail"}, 400


# Logout route
@auth_bp.route("/logout", methods=["POST"])
@cross_origin()
def logout():
    """Simulates a logout point. Doesn't do much until json webtokens are added"""

    return {"message": "success!"}


# Create user route
@auth_bp.route("/createuser", methods=["POST"])
@cross_origin()
def create_user():
    """Creates a user when a username, password, and email."""

    # Grab json content
    content = request.json
    email = content["email"]
    passwd = content["password"]
    username = content["password"]

    # Create user
    new_user = User(username=username, password=passwd, email=email)
    db.session.add(new_user)
    db.session.commit()

    return {
        "user_id": new_user.user_id,
        "username": new_user.username,
        "email": new_user.email,
    }
