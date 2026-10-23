
from app import app
from models import db, User, AuditLog
import uuid


def create_test_user(role="user"):
    email = f"test_{uuid.uuid4().hex}@example.com"
    user = User(
        name="Test User",
        email=email,
        role=role
    )
    user.set_password("TestPassword123")
    db.session.add(user)
    db.session.commit()
    return user


def test_normal_user_cannot_view_audit_logs():
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            user = create_test_user("user")
            user_id = user.id

        with client.session_transaction() as session:
            session["user_id"] = user_id

        response = client.get("/admin/audit-logs")
        assert response.status_code == 403

        with app.app_context():
            AuditLog.query.filter_by(user_id=user_id).delete()
            user = db.session.get(User, user_id)
            if user:
                db.session.delete(user)
            db.session.commit()


def test_admin_can_view_audit_logs():
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            user = create_test_user("admin")
            user_id = user.id

        with client.session_transaction() as session:
            session["user_id"] = user_id

        response = client.get("/admin/audit-logs")
        assert response.status_code == 200

        with app.app_context():
            AuditLog.query.filter_by(user_id=user_id).delete()
            user = db.session.get(User, user_id)
            if user:
                db.session.delete(user)
            db.session.commit()
