import pytest


class TestGetActivities:
    """Test GET /activities endpoint"""

    def test_get_all_activities_returns_200(self, client):
        """
        Arrange: Prepare test client
        Act: Make GET request to /activities
        Assert: Verify status code is 200
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """
        Arrange: Prepare test client
        Act: Make GET request to /activities
        Assert: Verify response is a dictionary
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_activities(self, client):
        """
        Arrange: Prepare test client
        Act: Make GET request to /activities
        Assert: Verify response contains expected activities
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball",
            "Tennis Club",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Science Club",
        ]
        for activity in expected_activities:
            assert activity in data

    def test_activity_has_required_fields(self, client):
        """
        Arrange: Prepare test client
        Act: Make GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert (
                    field in activity_data
                ), f"Missing field '{field}' in activity '{activity_name}'"

    def test_participants_is_list(self, client):
        """
        Arrange: Prepare test client
        Act: Make GET request to /activities
        Assert: Verify participants field is a list
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(
                activity_data["participants"], list
            ), f"participants in '{activity_name}' is not a list"

    def test_max_participants_is_integer(self, client):
        """
        Arrange: Prepare test client
        Act: Make GET request to /activities
        Assert: Verify max_participants is an integer
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(
                activity_data["max_participants"], int
            ), f"max_participants in '{activity_name}' is not an integer"
