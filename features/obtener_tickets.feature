Feature: Get all the tickets
    """
        Get all the tickets
    """

    Scenario: Success test for get tickets
        Given The app is running
        When I ask to view all the tickets
        Then I receive an empty list of tickets
