Feature: Get all the tickets
    """
        Get all the tickets
    """

    Scenario: Success test for get empty tickets
        Given I am an Analista de mesa de ayuda
        When I ask to view all the tickets and they don t exists
        Then I receive an empty list of tickets
    
    Scenario: Success test for get tickets
        Given I am an Analista de mesa de ayuda
        When I ask to view all the tickets
        Then I receive a list of tickets
