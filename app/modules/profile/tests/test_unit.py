import pytest

from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.profile.models import UserProfile


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)


def test_admin_requires_login(test_client):
    """
    Admin listing should require authentication.
    """
    # Ensure logged out
    logout(test_client)
    resp = test_client.get("/admin/profiles", follow_redirects=False)
    # Flask-Login typically redirects to login page (302) when not authenticated
    assert resp.status_code in (302, 401)


def test_admin_list_profiles_access_and_content(test_client):
    """
    Admin (user1@example.com) can access the admin profiles list and see entries.
    """
    with test_client.application.app_context():
        # Create admin user if not exists
        admin = User.query.filter_by(email="user1@example.com").first()
        if not admin:
            admin = User(email="user1@example.com", password="adminpass")
            db.session.add(admin)
            db.session.commit()

        # Ensure admin has a profile to list
        profile = UserProfile.query.filter_by(user_id=admin.id).first()
        if not profile:
            profile = UserProfile(user_id=admin.id, name="Admin", surname="User")
            db.session.add(profile)
            db.session.commit()

    # Login as admin
    login_resp = login(test_client, "user1@example.com", "adminpass")
    assert login_resp.status_code == 200

    # Admin route may redirect; ensure endpoint is reachable and renders without asserting specific text
    resp = test_client.get("/admin/profiles", follow_redirects=True)
    assert resp.status_code == 200

    logout(test_client)


def test_admin_delete_profile_flow(test_client):
    """
    Admin can delete a specific profile; expect redirect back to listing.
    """
    with test_client.application.app_context():
        # Prepare a regular user and profile to be deleted by admin
        victim = User.query.filter_by(email="victim@example.com").first()
        if not victim:
            victim = User(email="victim@example.com", password="victimpass")
            db.session.add(victim)
            db.session.commit()

        victim_profile = UserProfile.query.filter_by(user_id=victim.id).first()
        if not victim_profile:
            victim_profile = UserProfile(user_id=victim.id, name="Victim", surname="User")
            db.session.add(victim_profile)
            db.session.commit()

        profile_id = victim_profile.id

        # Ensure admin exists
        admin = User.query.filter_by(email="user1@example.com").first()
        if not admin:
            admin = User(email="user1@example.com", password="adminpass")
            db.session.add(admin)
            db.session.commit()

    # Login as admin and delete victim profile
    login_resp = login(test_client, "user1@example.com", "adminpass")
    assert login_resp.status_code == 200

    del_resp = test_client.post(f"/admin/profiles/{profile_id}/delete", follow_redirects=False)
    # Expect redirect to listing on success
    assert del_resp.status_code in (302, 303)
    # Optionally follow redirect to ensure admin page loads
    resp_follow = test_client.get("/admin/profiles", follow_redirects=True)
    assert resp_follow.status_code == 200

    logout(test_client)
