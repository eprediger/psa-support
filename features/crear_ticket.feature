Feature: Create a ticket
    """
        Create a ticket
    """

    Scenario: Success test for create tickets
        Given The app is running
        When I ask to create a ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "ticketError", severidad "alta", fecha de creacion "29-05-2020", fecha de actualizacion "29-05-2020", estado "Nuevo"
        Then I get the ticket with an id "1" of the database
