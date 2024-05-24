from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time,json,random,datetime,os
import gong_login as gg

def results_saver(book,linkedin_profiles,page):
    """Para salvar los resultados al final de cada pagina parseada."""
    with open(f'.\\Results\\Page{page}.json','w') as file:
        json.dump(book,file,indent=2)
    if linkedin_profiles:
        if os.path.isfile('.\\Results\linkedin_profiles.json'):
            with open('.\\Results\linkedin_profiles.json','r') as file:
                linkedin = json.load(file)
        else:
            linkedin= {}
        for name,valores in linkedin_profiles.items():
            if name in list(linkedin.keys()):
                name= name+ str(random.randint(1,100))
            linkedin[name] = valores
        with open('.\\Results\linkedin_profiles.json','w') as file:
            json.dump(linkedin,file,indent=2)

def main(page,count):
    """Funcion que maneja todo."""
    #inizializando driver y variables
    driver = Driver(uc=True)
    wait = WebDriverWait(driver,15)
    link = 'https://www.g2.com/products/gong/reviews?page=' 
    #logiando en gong
    driver = gg.gong_login_cookies(driver,wait)
    if isinstance(driver,str):
        print('Revisa la consola hay algo malo.')
        exit()
    #empezando el business
    paginas_scrapeadas = 0
    page = page
    driver.get(link + page) #va a la pagina
    #loop que mientras no se hayan escrapeado la cant de paginas pedidas en count sigue moviendose
    #dentro de cada pagina va a todos los perfiles y ve si tienen compañia y de lo contrarios lo guarda para luego buscarlo con linkedin
    while paginas_scrapeadas != int(count):
        print(f'Inicio en page {page}: {datetime.datetime.now().strftime("%H:%M")}') #para saber cuando emepzo
        book = {}
        linkedin_profiles = {}
        time.sleep(3)
        #encontrando links de perfiles ya sin perfiles verificados y los guarda
        white_boxes = driver.find_elements(By.XPATH,'//div[contains(@class,"paper paper--white paper--box")]//div[@class="inline-block"]//div[@data-poison-name]/span//a')
        profile_links = []
        for elemento in white_boxes:
            profile_links.append(elemento.get_attribute('href'))
        # buscando compañia y salvando datos en cada perfil gaurdado anteriormente
        for perfil in profile_links:
            driver.get(perfil)
            time.sleep(2)
            basic_path = '//div[@class="page page--base mt-2"]//div[@data-poison]/../div[2]'
            try:
                wait.until(ec.visibility_of_element_located((By.XPATH,basic_path)))
            except TimeoutException: #hay algunos perfiles que estan jodidos y no se cargan
                continue
            name = driver.find_element(By.XPATH,basic_path+'/div[1]').text #nombre del perfil
            try:
                company = driver.find_element(By.XPATH,basic_path+'/span[@class="x-company"]').text #si tiene compañia
            except:
                #si no entonces busca a ver si tiene linkedin para luego parsearlo,
                #si tampoco entonces devuelve que no tiene
                try:
                    linkedin_link = driver.find_element(By.XPATH,basic_path + '//div[@data-clipboard-text]').get_attribute('data-clipboard-text')
                    linkedin_profiles[name] = {'gong_link': perfil,'linkedin_link': linkedin_link}
                    continue
                except:
                    company = 'No tiene'
            #guarda lo scrapeado en el dicc
            book[name] = {'gong_link': perfil,'company':company}
            time.sleep(2)
        results_saver(book,linkedin_profiles,page) #para salvar resultados
        print(f'!!!Pagina {page} escrapeada!!!')
        paginas_scrapeadas+= 1
        print(f'Inicio en page {page}: {datetime.datetime.now().strftime("%H:%M")}\n')
        driver.get(link+page)
        try:
            next_button = wait.until(ec.presence_of_element_located((By.XPATH,'//div[@class="nested-ajax-loading"]/div[@data-poison-omit]//a[contains(text(),"Next")]'))) #boton de siguiente
            driver.get(next_button.get_attribute('href'))
        except TimeoutException:
            print(f'!!!Ultima pagina alcanzada!!!\nPinga s{"i"*20}')
            break
        page = str(int(page)+1)
        time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    page = input('Bienvenido al scraper de reviews de Gong, dime con cual pagina de reviews empezar: ')
    count = input('Cuantas paginas a scrapear: ')
    main(page,count)
    print('Terminado')