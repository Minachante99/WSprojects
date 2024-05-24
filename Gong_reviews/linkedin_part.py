from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import random,joblib,time,json

def keys_sender(element,keys):
    """Para simular humanidad al introducir texto"""
    for letter in keys:
        sec = random.choice(range(1,5))/10
        time.sleep(sec)
        element.send_keys(letter)

def linkedin_from_zero(driver,wait):
    """Logiarse desde zero paso a paso"""
    driver.get('https://www.linkedin.com/login?_l=es')
    #correo o telefono
    try:
        correo_element = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@id="username"]')))
    except TimeoutException:
        print('No llego a cargar la pagina')
        exit()
    keys_sender(correo_element,'leon99oficial@gmail.com')
    print('Correo: OK')
    #pass
    pass_element = driver.find_element(By.XPATH,'//input[@id="password"]')
    keys_sender(pass_element,'leon.9904')
    print('Password: OK')
    #boton iniciar sesion click
    iniciar_button = driver.find_element(By.XPATH,'//button[@data-litms-control-urn="login-submit"]')
    iniciar_button.click()
    print('Iniciar sesion: OK')
    #logiando
    try:
        wait.until(ec.presence_of_element_located((By.XPATH,'//nav[@class="global-nav__nav"]//img[@alt="Paulo Leon"]')))
    except TimeoutException:
        print('Ve a ver que paso que no cargo el logueo final')
        exit()
    print('Logiado desde zero(LinkedIn).')
    #cookies
    with open(r'.\cookies\linkedin_cookies.joblib','wb') as file:
        joblib.dump(driver.get_cookies(),file) 
    input('Tiza ')
    time.sleep(3)
    return driver       

def linkedin_login(driver,wait,zero=False):
    """Para logiarse que decida entre cookies o desde zero."""
    #si se quiere empezar desde cero:
    if zero:
        linkedin_from_zero(driver,wait)
        input('Tiza ')
        exit()
    #tratando por cookies
    driver.get('https://www.linkedin.com/robots.txt')
    try:
        with open(r'.\cookies\linkedin_cookies.joblib','rb') as file:
            cookies = joblib.load(file)
        for cookie in cookies: driver.add_cookie(cookie)
        driver.get('https://www.linkedin.com/feed/')
        wait.until(ec.visibility_of_element_located((By.XPATH,'//nav[@class="global-nav__nav"]//img[@alt="Paulo Leon"]')))
        print('Logiado por cookies(LinkedIn)')
    #si no encuentra cookies
    except OSError:
        print('No se encontraron cookies, doing it from zero.')
        driver = linkedin_from_zero(driver,wait)
    #si no se llego a loguear cookies caducaron o algo
    except TimeoutException:
        print('No sirvieron las cookies, doing it from zero.')
        driver = linkedin_from_zero(driver,wait)

    return driver

def linkedin_profile(driver,wait):
    """Carga los archivos que contienen los perfiles que solo se puede buscar compañia en linkedin y los procesa."""
    with open(r'.\Results\linkedin_profiles.json','r') as file:
        profiles = json.load(file)
    for key,value in profiles.items():
        driver.get(value['linkedin_link'])
        #extrayendo compañia
        try:
            wait.until(ec.visibility_of_element_located((By.XPATH,'//ul//button[contains(@aria-label,"Empresa actual:")]')))
        except TimeoutException:
            profiles[key]['company'] = 'No tiene'
        company = driver.find_element(By.XPATH,'//ul//button[contains(@aria-label,"Empresa actual:")]//div').text
        profiles[key]['company']= company
    with open(r'.\Results\linkedin_profiles.json','w') as file:
        json.dump(profiles,file,indent=2)
    print('Procesados los perfiles')


if __name__ == '__main__':
    driver = Driver(uc=True)
    wait = WebDriverWait(driver,15)
    driver = linkedin_login(driver,wait)
    linkedin_profile(driver,wait)