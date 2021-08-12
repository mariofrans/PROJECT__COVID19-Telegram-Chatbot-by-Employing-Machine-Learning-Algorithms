from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import random

# Bad attempt at web scraping
# Get chromedriver from https://chromedriver.chromium.org/downloads and put it in the same dir 
# install beautiful-soup
# install selenium


symptoms = 'https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html'
covidDesc = 'https://www.cdc.gov/dotw/covid-19/index.html'
treatmentInfo = 'https://www.cdc.gov/coronavirus/2019-ncov/your-health/treatments-for-severe-illness.html'
quarantine = 'https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/isolation.html'
protect = 'https://www.cdc.gov/dotw/covid-19/index.html'

def get_symptoms():
    # Symptoms
    # Scraping
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(symptoms)
    wait = WebDriverWait(driver, 10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    output = ''

    head = soup.find('h2', text='Watch for Symptoms')
    para = head.find_next_siblings('p', limit=1)
    ul = head.find_next_siblings('ul', limit=1)
    for p in para:
        output = output + '\n' + p.get_text()
    for li in ul:
        output = output + '\n' + li.get_text()

    output = output + '\n' + 'For more information please visit ' + symptoms
    return output

def get_whoAreYou():
    # 13.1.About_Anezka_WhoAreYou
    response = ["I am Bot", "You can call me Bot"]
    return random.choice(response)

def get_covidDesc():
    # COVID_Description
     # Scraping
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(covidDesc)
    wait = WebDriverWait(driver, 10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    div = soup.find('div', class_='col-md-12')
    output = ''
    header = div.find_all('p')
    output = str(header[1].get_text())

    output = output + '\n' + 'For more information please visit ' + covidDesc
    return output

def get_generalHelp():
    # general_help
    response = ["If you are still unsure, please seek professional help", "Can you ask the question more in detail?"]
    return random.choice(response)

def get_treatmentInfoTest():
    # 4.2.Treatment_info
     # Scraping
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(treatmentInfo)
    wait = WebDriverWait(driver, 10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    h1 = soup.find('h2', text='Drugs Approved or Authorized for Use')
    h2 = soup.find('h2', text='Treatment Outside of the Hospital')
    output = ''
    for head in (h1.find_previous_siblings('p', limit=1)):
        output = output + head.get_text() + '\n'
    # output = output + h2.get_text()
    ul = (h2.find_next_siblings('ul', limit=1))
    p = (h2.find_next_siblings('p', limit=1))
    for para in p:
        output = output + '\n' + para.get_text()
    for li in ul:
        output = output + '\n' + li.get_text()

    output = output + '\n' + 'For more information please visit ' + treatmentInfo
    return output 


def get_quarantine():
    # 5.1.Quarantine_what_to_do
     # Scraping
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(quarantine)
    wait = WebDriverWait(driver, 10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    output = ''

    header1 = soup.find('p', text='Stay home except to get medical care')
    output = output + header1.get_text()

    ul = header1.find_next_siblings('ul', limit=1)
    for li in ul:
        output = output + '\n' + li.get_text()

    header2 = soup.find('p', text='You can be with others after')
    output = output + '\n' + header2.get_text()

    ul2 = header2.find_next_siblings('ul', limit=1)
    for li in ul2:
        output = output + '\n' + li.get_text()

    output = output + '\n' + 'For more information please visit ' + quarantine
    return output

def get_protect():
    # Protecting_Against_Infection
    # Scraping
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(protect)
    wait = WebDriverWait(driver, 10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    output = ''

    header1 = soup.find('h3', text='Prevention Tips')
    ul = header1.find_next_siblings('ul', limit=1)
    output = output + '\n' + header1.get_text()
    
    for li in ul:
        output = output + '\n' + li.get_text()

    output = output + '\n' + 'For more information please visit ' + protect
    
    return output

def get_hate():
    # 13.4.About_Anezka_hate
    response = ["Can you tell more about it?", "What do you hate exactly"]
    return random.choice(response)

def get_gratitude():
    # Gratitude
    response = ["Happy to help!", "Any time!", "My pleasure"]
    return random.choice(response)

def get_caseCount(country):
    # copy from the NN file
    # Case_Count
    output = ''
    if len(country) > 0:
        for x in country:
            output = output + x + '\n'
            response = requests.get('https://covid19.mathdro.id/api/countries/' + x)
            if (response.status_code == 200):
                data = response.json()
                output = output + 'Confirmed: ' + str(data['confirmed']['value']) + '\n'
                output = output + 'Recovered: ' + str(data['recovered']['value']) + '\n'
                output = output + 'Deaths: ' + str(data['deaths']['value']) + '\n'
                output = output + 'Taken from: https://covid19.mathdro.id/api/countries/' + x + '\n'

            else:
                data.response.json()
                output = output + str(data['error']['message']) 
    else:
        response = requests.get('https://covid19.mathdro.id/api')
        if (response.status_code == 200):
            data = response.json()
            output = output + 'Confirmed: ' + str(data['confirmed']['value']) + '\n'
            output = output + 'Recovered: ' + str(data['recovered']['value']) + '\n'
            output = output + 'Deaths: ' + str(data['deaths']['value']) + '\n'
            output = output + 'Taken from:https://covid19.mathdro.id/api' + '\n'

    return output

def get_greeting():
    # 13.3.About_Anezka_Greeting
    response = ["Hello", "Hey!", "What can i do for you?"]
    return random.choice(response)

switcher = {
        '13.1.About_Anezka_WhoAreYou': get_whoAreYou,
        '13.3.About_Anezka_Greeting': get_greeting,
        '13.4.About_Anezka_hate': get_hate,
        'Protecting_Against_Infection': get_protect,
        '5.1.Quarantine_what_to_do': get_quarantine,
        '4.2.Treatment_info': get_treatmentInfoTest,
        'general_help': get_generalHelp,
        'COVID_Description': get_covidDesc,
        'Symptoms': get_symptoms,
        'Case_Count': get_caseCount,
        'Gratitude': get_gratitude
    }

def handler(intent, country=[]):
    func = switcher.get(intent, '?')
    if intent == 'Case_Count':
        return func(country)
    else:
        return func()


    
