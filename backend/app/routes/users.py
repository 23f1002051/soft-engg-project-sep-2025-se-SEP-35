from flask import Blueprint, jsonify

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.get("/health")
def users_health():
    return jsonify({"status": "users OK"}), 200

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.get("/health")
def users_health():
    return jsonify({"status": "users OK"}), 200

def serialize_user(u: User):
    return {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "company_name": u.company_name,
        "email": u.email,
        "role": u.role,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }

def bad_request(msg, code=400):
    return jsonify({"error": msg}), code

@users_bp.get("")
def list_users():
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    q = User.query.order_by(User.id.desc())
    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [serialize_user(u) for u in pagination.items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), 200

@users_bp.get("/<int:user_id>")
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return jsonify(serialize_user(u)), 200

@users_bp.post("")
def create_user():
    data = request.get_json(silent=True) or {}
    required = ["first_name", "last_name", "email", "password"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        return bad_request(f"Missing required fields: {', '.join(missing)}")

    email = (data["email"] or "").strip().lower()
    if User.query.filter_by(email=email).first():
        return bad_request("Email already exists", 409)

    u = User(
        first_name=(data["first_name"] or "").strip(),
        last_name=(data["last_name"] or "").strip(),
        company_name=((data.get("company_name") or "").strip() or None),
        email=email,
        role=(data.get("role") or "candidate").strip()
    )
    u.set_password(data["password"])

    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return bad_request("Email already exists", 409)

    return jsonify(serialize_user(u)), 201

@users_bp.patch("/<int:user_id>")
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    u = User.query.get_or_404(user_id)

    if "first_name" in data and data["first_name"]:
        u.first_name = data["first_name"].strip()
    if "last_name" in data and data["last_name"]:
        u.last_name = data["last_name"].strip()
    if "company_name" in data:
        val = (data.get("company_name") or "").strip()
        u.company_name = val or None
    if "role" in data and data["role"]:
        u.role = data["role"].strip()
    if "email" in data and data["email"]:
        new_email = data["email"].strip().lower()
        if new_email != u.email and User.query.filter_by(email=new_email).first():
            return bad_request("Email already exists", 409)
        u.email = new_email
    if "password" in data and data["password"]:
        u.set_password(data["password"])

    db.session.add(u)
    db.session.commit()
    return jsonify(serialize_user(u)), 200

@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({"deleted": True, "id": user_id}), 200
