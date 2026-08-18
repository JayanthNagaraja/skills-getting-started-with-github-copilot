import pytest


class TestUnregisterFromActivity:
    """Test POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client):
        """
        Arrange: Prepare activity and participant that exists
        Act: Make POST request to unregister endpoint
        Assert: Verify status code is 200 and response message contains success text
        """
        # Arrange
        activity_name = "Chess Club"
        test_email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={test_email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert test_email in data["message"]

    def test_unregister_removes_participant(self, client):
        """
        Arrange: Prepare participant to unregister
        Act: Make POST request to unregister, then GET activities
        Assert: Verify participant removed from participants list
        """
        # Arrange
        activity_name = "Programming Class"
        test_email = "emma@mergington.edu"  # Already registered

        # Act
        client.post(f"/activities/{activity_name}/unregister?email={test_email}")
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert test_email not in data[activity_name]["participants"]

    def test_unregister_decrements_participant_count(self, client):
        """
        Arrange: Get initial participant count
        Act: Make POST request to unregister
        Assert: Verify participant count decreased by 1
        """
        # Arrange
        activity_name = "Gym Class"
        test_email = "john@mergington.edu"  # Already registered
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/unregister?email={test_email}")
        response = client.get("/activities")

        # Assert
        new_count = len(response.json()[activity_name]["participants"])
        assert new_count == initial_count - 1

    def test_unregister_not_registered_error(self, client):
        """
        Arrange: Prepare email that is not registered for activity
        Act: Make POST request to unregister non-existent participant
        Assert: Verify status code is 400 and error message is present
        """
        # Arrange
        activity_name = "Chess Club"
        test_email = "notregistered@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={test_email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"].lower()

    def test_unregister_activity_not_found(self, client):
        """
        Arrange: Prepare non-existent activity name
        Act: Make POST request to unregister from non-existent activity
        Assert: Verify status code is 404
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        test_email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={test_email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_unregister_then_signup_again(self, client):
        """
        Arrange: Prepare participant registered for activity
        Act: Unregister and then sign up again
        Assert: Verify participant is registered and count is correct
        """
        # Arrange
        activity_name = "Basketball"
        test_email = "alex@mergington.edu"

        # Act - unregister
        client.post(f"/activities/{activity_name}/unregister?email={test_email}")
        response1 = client.get("/activities")
        count_after_unregister = len(response1.json()[activity_name]["participants"])

        # Act - sign up again
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        response2 = client.get("/activities")

        # Assert
        assert test_email in response2.json()[activity_name]["participants"]
        count_after_signup = len(response2.json()[activity_name]["participants"])
        assert count_after_signup == count_after_unregister + 1

    def test_unregister_frees_activity_slot(self, client):
        """
        Arrange: Fill an activity to capacity, then unregister one participant
        Act: Try to sign up new participant after unregistering
        Assert: Verify new participant can sign up (slot was freed)
        """
        # Arrange
        activity_name = "Art Studio"
        new_student = "newstudent@mergington.edu"
        
        # Get current state
        response = client.get("/activities")
        activity = response.json()[activity_name]
        max_participants = activity["max_participants"]
        participants = activity["participants"].copy()
        
        # Fill to capacity if not already full
        for i in range(max_participants - len(participants)):
            client.post(
                f"/activities/{activity_name}/signup?email=filler{i}@mergington.edu"
            )
        
        # Unregister one participant to free a slot
        student_to_unregister = participants[0]
        client.post(
            f"/activities/{activity_name}/unregister?email={student_to_unregister}"
        )

        # Act - try to sign up new participant
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_student}"
        )

        # Assert
        assert response.status_code == 200
        assert new_student in response.json()["message"]
