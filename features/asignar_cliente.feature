Feature: Asign client to a ticket
    """
        As an Analista de mesa de ayuda,
        I want to asign a client to a tocket
        to be able to know who generated that ticket.
    """

    Scenario: Success to asign a client to a ticket
        Given I have a client and a ticket
        When I asign the client to the ticket
        Then I can see the name of the client asigned to the ticket

    Scenario: Unsuccess to asign an unexisting client to a ticket
        Given I have a ticket
        When I asign an unexisting client to the ticket
        Then I can see a warning because the client doesnt exist