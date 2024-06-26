from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import joblib,random,time

def start_chrome(headless=False):
    #opciones del navegador
    options = Options()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0')
    options.add_argument('--headless') if headless else options.add_argument('--start-maximized')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--no-proxy-server')
    options.add_argument('--disable-blink-features=AutomationContolled')
    options.add_experimental_option('excludeSwitches',['enable-automation','ignore-certificate-errors','enable-logging'])
    options.add_experimental_option('prefs',{'profile.default_content_settings_values.notifications':2,'intl.accept_languages':['es-ES','es'],'credentials_enable_service':False})
    driver = Chrome(options=options)

    return driver

def keys_sender(element,keys):
    #para simular humanidad al introducir texto
    for letter in keys:
        sec = random.choice(range(1,5))/10
        time.sleep(sec)
        element.send_keys(letter)

def password(driver,wait):
    #funcion para no tener que escribir lo mismo dos veces
    #espera a que se cargue la ventana de pass y envia la pass
    try:
        pass_element = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@name="password" and @type="password"]')))
        keys_sender(pass_element,'')
        pass_salir = wait.until(ec.visibility_of_element_located((By.XPATH,'//span[text()="Iniciar sesión"]/../..')))
    except TimeoutException:
        print('No cargo el login de la password')
        driver.close()
        driver.quit()
        exit()
    
    #solo clickea el boton y fuera
    pass_salir.click()
    
def login_from_zero(driver,wait):
    #entrando a la web del login para loguearse desde cero
    #logiando correo
    driver.get('https://twitter.com/i/flow/login')
    try:
        correo_element = wait.until(ec.visibility_of_element_located((By.XPATH,'//input')))
        keys_sender(correo_element,'')
        correo_salir = wait.until(ec.visibility_of_element_located((By.XPATH,'//span[text()="Siguiente"]/../..')))  
    except TimeoutException:
        print('No cargo el login del correo')
        driver.close()
        driver.quit()
        exit()
    correo_salir.click()
    print('Correo: OK')
    
    #usuario y/o pass
    #para si carga el cartel de usuario sospechoso haga ambos
    #de lo contrario pasa al pass
    try:
        user_element = wait.until(ec.visibility_of_element_located((By.XPATH,'//span[text()="Teléfono o nombre de usuario"]/../../..//input')))
        keys_sender(user_element,'Minachante')
        user_salir = wait.until(ec.visibility_of_element_located((By.XPATH,'//span[text()="Siguiente"]/../..'))) 
        user_salir.click()
        password(driver,wait)
    except TimeoutException:
        print('No cargo el cartelito del user')
        password(driver,wait)
    print('Pass: OK')
    
    #checkando que se cargue el perfil
    try:
        wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@data-testid="UserAvatar-Container-Minachante"]')))
    except TimeoutException:
        print('No cargo el perfil')
    print('Perfil: OK')
    cookies = driver.get_cookies()
    with open('cookies_twitter.joblib','wb') as file:
        joblib.dump(cookies,file)
    print('Logiado desde cero')
    time.sleep(2)
    return driver

def login_x(headless=False,zero=False):
    """Funcion que maneja todo, prueba si puede logearse con cookies y de lo contrario desde cero.
    Argumento zero para saber si se quiere hacer una prueba e iniciar desde caro;
    Argumento Head para si se quiere abrir en headless o no"""
    
    #iniciando chrome y el wait
    driver = start_chrome(headless=headless)
    wait = WebDriverWait(driver,10)
    if zero:
        return login_from_zero(driver,wait)
    
    #probando si tengo cookies
    driver.get('https://twitter.com/robots.txt')
    try:
        with open('cookies_twitter.joblib','rb') as file:
            cookies = joblib.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('https://twitter.com')
        wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@data-testid="UserAvatar-Container-Minachante"]')))
        print('Logiado por cookies')
        time.sleep(3)
    #si no tengo o expiraron levanto desde cero y guardo las
    except OSError:
        driver = login_from_zero(driver,wait)
    except TimeoutException:
        driver = login_from_zero(driver,wait)
    
    return driver

if __name__ == '__main__':
    driver = login_x()
    input('Hablate ')
    driver.close()
    driver.quit()
    
    