Feature: Modify a ticket
    """
        Modify a ticket
        US: HDM7
    """

    Scenario: Success test for edit a ticket
        Given I am an Analista de mesa de ayuda
        When I ask to modify the ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "Error", severidad "Alta", estado "Nuevo", responsable "Gaston Parente", pasos "Paso 1, 2 y 3"
        Then I get a message saying "204"
    
    Scenario: Invalid estado
        Given I am an Analista de mesa de ayuda
        When I ask to modify the ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "Error", severidad "Alta", estado "Falso", responsable "Gaston Parente", pasos "Paso 1, 2 y 3"
        Then I get a message saying "El estado de ticket debe ser Nuevo/Asignado/Cerrado"
    
    Scenario: Invalid tipo
        Given I am an Analista de mesa de ayuda
        When I ask to modify the ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "Falso", severidad "Alta", estado "Nuevo", responsable "Gaston Parente", pasos "Paso 1, 2 y 3"
        Then I get a message saying "El tipo de ticket debe ser Error/Consulta/Mejora"
    
    Scenario: Invalid severidad
        Given I am an Analista de mesa de ayuda
        When I ask to modify the ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "Error", severidad "Falso", estado "Nuevo", responsable "Gaston Parente", pasos "Paso 1, 2 y 3"
        Then I get a message saying "La severidad debe ser Alta, Media o Baja"
    
    Scenario: Success test for edit a ticket and moving estado to Cerrado
        Given I am an Analista de mesa de ayuda
        When I ask to modify the ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "Error", severidad "Alta", estado cerrado "Cerrado", responsable "Gaston Parente", pasos "Paso 1, 2 y 3"
        Then The fecha finalizacion will be the today's date
    
    Scenario: Success test for edit a ticket and changing severity
        Given I am an Analista de mesa de ayuda
        When I ask to modify the ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "Error", new severidad "Baja", estado "Cerrado", responsable "Gaston Parente", pasos "Paso 1, 2 y 3"
        Then The fecha limite will be updated with the today s date plus "90" days

    Scenario: Triying to change estado from cerrado to another
        Given I am an Analista de mesa de ayuda
        When I ask to modify the ticket with nombre "ticketprueba", descripcion "descripcion prueba", tipo "Error", severidad "Baja", estado from cerrado "Nuevo", responsable "Gaston Parente", pasos "Paso 1, 2 y 3" 
        Then I get a message saying "El ticket ya fue cerrado previamente"