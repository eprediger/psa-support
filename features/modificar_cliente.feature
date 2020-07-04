Feature: Modify a client
    """
        As an Analista de mesa de ayuda,
        I want to modify a cliente
        to be able to correct or change the atributes of a cliente
    """


    Scenario: Success to modify a cliente
        Given I am an Analista de mesa de ayuda and i have a client with razon social: "razon social prueba", CUIT:"123456", descripcion:"descripcion prueba", fecha desde que es cliente:"12022020"
        When I modify the razon social por "razon social 2", CUIT:"654321", descripcion: "descripcion modificada" y fecha desde que es cliente por "123123123"
        Then I can see a cliente With CUIT "654321" and the rest of its atributes modified.

    Scenario: Unuccess to modify a cliente
        Given I am an Analista de mesa de ayuda and i have a client with razon social: "razon social prueba", CUIT:"123456", descripcion:"descripcion prueba", fecha desde que es cliente:"12022020"
        When I modify the razon social por "", CUIT:"", descripcion: "" y fecha desde que es cliente por ""
        Then I see a warning that all the fields must be filled.
