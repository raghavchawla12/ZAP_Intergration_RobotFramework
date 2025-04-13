*** Settings ***
Library         SeleniumLibrary
Library         OperatingSystem
Library         Process
Library         Collections
Library         ../zap_scan.py

*** Variables ***
${ZAP_PATH}      C:/Program Files/ZAP/Zed Attack Proxy/zap.bat
${ZAP_API_KEY}   "enter_your_api_key"
${ZAP_HOST}      http://127.0.0.1:8080

*** Keywords ***
Start ZAP And Browser
    Start ZAP Server  ${ZAP_PATH}  ${ZAP_API_KEY}
    Sleep    15s
    Open Browser    https://juice-shop.herokuapp.com    chrome
    Create Webdriver    Chrome   options=add_argument("--proxy-server=${ZAP_HOST}")
    Go To    https://juice-shop.herokuapp.com

Stop ZAP And Browser
    Close Browser
    Run ZAP Scan    https://juice-shop.herokuapp.com    ${ZAP_API_KEY}

Suite Setup Keyword
    ${result}  Run Keyword And Ignore Error  Start ZAP And Browser
    Log  ${result}
