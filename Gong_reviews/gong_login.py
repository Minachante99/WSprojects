from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import random,joblib,time

def keys_sender(element,key):
    """Simular humanidad, cada ciertos segundos envia cada letra."""
    for letter in key:
        time.sleep(random.randint(1,4)/10)
        element.send_keys(letter)

def gong_login_from_zero(driver,wait):
    """Funcion de login desde cero en gong."""
    driver.get('https://www.g2.com/identities/start_login') #url de logearse
    #correo
    try:
        correo_element = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@id="auth_key"]')))
    except TimeoutException:
        print('No cargo la pagina, revisa ahi.')
        return 'Error'
    keys_sender(correo_element,'nelly550ruiz@gmail.com')
    print('Correo: OK')
    #pass
    pass_element = driver.find_element(By.XPATH,'//input[@id="password_input"]')
    keys_sender(pass_element,'Nelly.990423')
    print('Pass: OK')
    #boton de logearse
    try:
        boton = wait.until(ec.element_to_be_clickable((By.XPATH,'//input[@value="Sign In"]')))
    except TimeoutException:
        print('Ese maricon no me quiere dejar pasar el login.')
        return 'Error'
    boton.click()
    print('Boton: OK')
    #banner
    try:
        francisco = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@id="company-domain-banner"]//div[@data-testid="company-domain-banner-dismiss"]/../div[2]'))).text
        if 'Francisco' not in francisco:
            print('Chekea el banner')
            return 'Error'
    except TimeoutException:
        print('No quiso cargar el banner ve a ver ahi.')
        return 'Error'
    #guardando cookies
    with open(r'.\cookies\gong_cookies.joblib','wb') as file:
        joblib.dump(driver.get_cookies(),file)
    print('Logueado desde zero(Gong).\n')
    
    return driver

def gong_login_cookies(driver,wait):
    """Funcion que inicia por cookies, devuelve el driver o str en caso de que sea error."""
    driver.get('https://www.g2.com/robots.txt')
    #Tratando por cookies
    try:
        with open(r'.\cookies\gong_cookies.joblib','rb') as file:
            cookies = joblib.load(file)
        for cookie in cookies: driver.add_cookie(cookie)
        driver.get('https://www.g2.com')
        francisco = wait.until(ec.presence_of_element_located((By.XPATH,'//div[@id="company-domain-banner"]//div[@data-testid="company-domain-banner-dismiss"]/../div[2]'))).text
        if 'Francisco' not in francisco:
            print('Chekea el banner en las cookies.')
            gong_login_from_zero(driver,wait)
        print('Logiado por cookies.')
    except OSError:
        print('No se encontraron cookies, doing it from zero')
        driver = gong_login_from_zero(driver,cookies)
    except TimeoutException:
        print('Se murio esperando, doing it from zero.')
        driver = gong_login_from_zero(driver,cookies)
    
    return driver