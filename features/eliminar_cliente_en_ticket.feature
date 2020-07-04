Feature: Delete a client of a ticket
    """
        As an Analista de mesa de ayuda,
        I want to delete the client of ticket
        to be able to leave a ticket without a client.
    """

    Scenario: Success deletion of a client asigned to ticket
        Given I have a ticket that already has a client loaded
        When I delete the client of the ticket
        Then I can see that the ticket has no client asigned
