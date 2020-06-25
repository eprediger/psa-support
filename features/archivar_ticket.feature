Feature: Archive the tickets
    """
        Archive the tickets
    """

    Scenario: Success test for Archive tickets
        Given I am an Analista de mesa de ayuda
        When I ask to Archive an existing ticket
        Then I get a message saying "Ticket archivado con exito!"
    
    Scenario: Archive a ticket with estado not cerrado
        Given I am an Analista de mesa de ayuda
        When I ask to Archive an existing ticket with estado not cerrado
        Then I get a message saying "Los tickets deben estar cerrados para poder archivarse!"