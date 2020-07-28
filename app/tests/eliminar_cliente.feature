Feature: Delete a client
    """
        As an Analista de mesa de ayuda,
        I want to delete a client
        to stop seeing a client.
    """

    Scenario: Success delete of a client not asigned to a ticket
        Given I have a client with razon social: "razon social prueba", CUIT:"123456", descripcion:"descripcion prueba"
        When I delete the client
        Then I can see a message saying that the client was deleted succesfully

    Scenario: Warning when deleteing a client that doesnt exist
        Given I have no clients
        When I delete the client 1
        Then I can see a warning saying that the client doesnt exist




