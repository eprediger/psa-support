Feature: Create a client
    """
        As an Analista de mesa de ayuda,
        I want to create a cliente
        to be able to see which clients have products in maintenance
    """


    Scenario: Success to create a cliente
        Given I am an Analista de mesa de ayuda
        When I create a client with razon social:"razon social prueba", descripcion:"descripcion prueba", CUIT:"12345654"
        Then a client is created with a CUIT:"12345654"

    Scenario: Unsuccess to create a cliente
        Given I am an Analista de mesa de ayuda
        When I create a client without razon social:"razon social prueba", descripcion:"descripcion prueba", CUIT:"12345654"
        Then I see a warning that all the fields must be filled.
