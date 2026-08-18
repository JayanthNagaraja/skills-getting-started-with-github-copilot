import pytest


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """
        Arrange: Prepare activity name and test email
        Act: Make POST request to signup endpoint
        Assert: Verify status code is 200 and response message contains success text
        """
        # Arrange
        activity_name = "Chess Club"
        test_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={test_email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert test_email in data["message"]

    def test_signup_adds_participant(self, client):
        """
        Arrange: Prepare activity name and test email
        Act: Make POST request to signup, then GET activities
        Assert: Verify new participant appears in participants list
        """
        # Arrange
        activity_name = "Programming Class"
        test_email = "newstudent@mergington.edu"

        # Act
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert test_email in data[activity_name]["participants"]

    def test_signup_increments_participant_count(self, client):
        """
        Arrange: Prepare activity name and test email, get initial count
        Act: Make POST request to signup
        Assert: Verify participant count increased by 1
        """
        # Arrange
        activity_name = "Basketball"
        test_email = "newstudent@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        response = client.get("/activities")

        # Assert
        new_count = len(response.json()[activity_name]["participants"])
        assert new_count == initial_count + 1

    def test_signup_duplicate_registration_error(self, client):
        """
        Arrange: Sign up a student, then attempt to sign them up again
        Act: Make POST request to signup endpoint with same email
        Assert: Verify status code is 400 and error message is present
        """
        # Arrange
        activity_name = "Chess Club"
        test_email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={test_email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_activity_not_found(self, client):
        """
        Arrange: Prepare non-existent activity name
        Act: Make POST request to signup for non-existent activity
        Assert: Verify status code is 404
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        test_email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={test_email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_signup_activity_full_error(self, client):
        """
        Arrange: Get an activity and fill it to max participants
        Act: Try to sign up when activity is full
        Assert: Verify status code is 400 and error message about full activity
        """
        # Arrange
        activity_name = "Art Studio"
        test_email = "student@mergington.edu"
        
        # Get current participants count
        response = client.get("/activities")
        activity = response.json()[activity_name]
        max_participants = activity["max_participants"]
        current_count = len(activity["participants"])
        
        # Fill the activity to capacity
        for i in range(max_participants - current_count):
            client.post(
                f"/activities/{activity_name}/signup?email=filler{i}@mergington.edu"
            )

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={test_email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "full" in data["detail"].lower()

    def test_signup_multiple_students_same_activity(self, client):
        """
        Arrange: Prepare two different emails for same activity
        Act: Sign up both students to the same activity
        Assert: Verify both are in participants list
        """
        # Arrange
        activity_name = "Tennis Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"

        # Act
        client.post(f"/activities/{activity_name}/signup?email={email1}")
        client.post(f"/activities/{activity_name}/signup?email={email2}")
        response = client.get("/activities")

        # Assert
        participants = response.json()[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants
