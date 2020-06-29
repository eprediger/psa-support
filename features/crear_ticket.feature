Feature: Create a ticket
    """
        As an Analista de mesa de ayuda,
        I want to create a ticket
        to be able to register an issue from a client.
    """

    Scenario: Success to create a ticket without estado
        Given I am an Analista de mesa de ayuda
        When I create a ticket with nombre "ticketBDD", descripcion "descripcion BDD", tipo "consulta", severidad "alta"
        Then a ticket is created with estado "nuevo"

    Scenario: Not success to create a ticket because of missing name
        Given I am an Analista de mesa de ayuda
        When I create a ticket with descripcion "descripcion BDD", tipo "consulta", severidad "alta"
        Then I recive a warning because there is information that is missing 

    Scenario: Not success to create a ticket because wrong severidad
        Given I am an Analista de mesa de ayuda
        When I create a ticket with nombre "ticketBDD", descripcion "descripcion BDD", tipo "consulta", severidad "mucha"
        Then I recive a warning because there is a wrong value at severidad

    Scenario: Not success to create a ticket because of wrong tipo
        Given I am an Analista de mesa de ayuda
        When I create a ticket with nombre "ticketBDD", descripcion "descripcion BDD", tipo "queja", severidad "baja"
        Then I recive a warning because there is a wrong value at tipo