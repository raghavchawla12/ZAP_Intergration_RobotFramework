*** Settings ***
Library         SeleniumLibrary
Library         Process
Library         OperatingSystem
Library         Collections
Resource        ../resources/keywords.robot
Suite Setup     Start ZAP And Browser
Suite Teardown  Stop ZAP And Browser

*** Test Cases ***
Login And Browse Juice Shop
    Go To    https://juice-shop.herokuapp.com/#/
    Maximize Browser Window
    Sleep    3s
    Click Element    css=button[aria-label="Close Welcome Banner"]
    Click Element    css=button[aria-label="Show the login page"]
    Input Text       id=email    test@juice-sh.op
    Input Text       id=password    test123
    Click Element    id=loginButton
    Wait Until Page Contains Element    css=mat-toolbar
    Sleep    3s
