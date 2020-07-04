Feature: Modify client of a ticket
    """
        As an Analista de mesa de ayuda,
        I want to modify the client of ticket
        to be able to correct an error while inserting data to a ticket.
    """

    Scenario: Success modification on a client asigned to ticket
        Given I have a client and a ticket that already has a client loaded
        When I modify the client of the ticket
        Then I can see the name of the new client asigned to the ticket

    Scenario: Unsuccess modification on a client asigned to ticket with another client that doesnt exist
        Given I ticket that already has a client loaded
        When I modify the client of the ticket with another that doesnt exist
        Then I can see a warning because the client doesnt exist