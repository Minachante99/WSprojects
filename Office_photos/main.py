"""Este script hace una peticion a una api del sitio https://www.regus.com para obtener un link a cada una
    de las oficinas en un area seleccionada para luego scrapear 3 fotos de cada oficina"""

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import  TimeoutException
import wget,time,os,requests

def office_getter():
    """Funion que guarda todos los links de las oficinas"""
    links = []#para salvar los links de las oficinas
    headers = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
'Accept-Language' : 'es-419,es;q=0.9,en-US;q=0.8,en;q=0.7','Accept-Encoding' : 'gzip, br'}#setteando some headers
    base_url =  'https://www.regus.com'
    #peticion a la api
    geo_locations = requests.get(r'https://www.regus.com/api/v2/geo-resultsv2?lat=54.86886319162308&lng=-129.94270706176758&radius=1735.25036052001&northeastLat=69.56052676640829&northeastLng=-118.25325393676759&southwestLat=31.86612897946877&southwestLng=-141.63216018676758&search=United+States&ws=office-space&lang=es-es&trigger=map&sort=near&place_id=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
                                 ,headers=headers).json()
    #obteniendo links
    for res in geo_locations['GeoResults']:
        links.append(base_url + res['CtaLinks'][0]['locationHref'])

    return links
   
def pictures_getter(links):
    """Funcion que se encarga de scrapear las fotos utilizando los links a las oficinas"""
    #estableciendo driver y otros parametros
    driver = Driver(uc=True)
    wait = WebDriverWait(driver,10)
    driver.maximize_window()
    #para aceptar cookies de una sola vez
    driver.get(
        'https://www.regus.com/es-es/results?lat=54.86886319162303&lng=-129.94270706176758&radius=3055.7430815667412&northeastLat=71.01258165293922&northeastLng=-77.38411331176759&southwestLat=28.13763667368957&southwestLng=177.49869918823242&search=United+States&ws=office-space&lang=es-es&trigger=map&sort=near&place_id=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
               )#gettiando pagina de las oficinas
    try:
        wait.until(ec.visibility_of_element_located((By.XPATH,'//h2[@id="ot-pc-title"]')))
        time.sleep(1)
        aceptar_cookies = driver.find_element(By.XPATH,'//button[@id="accept-recommended-btn-handler"]')
        aceptar_cookies.click()
    except:
        print('No aparecio el cartel de las cookies')
    #escrapeando cada oficina
    for link in links:
        driver.get(link)#yendo a la pagina
        #obteniendo el id de la oficina
        office_id = link.split('/')[-1]
        office_id = office_id[:office_id.find('?')].split('-')[-1]
        #print(office_id)
        time.sleep(1.5)
        pictures = driver.find_elements(By.XPATH,'//section[@data-hero]//div[contains(@class,"secondary")]//..//picture//img')#obteniendo los links
        pictures = [foto.get_attribute('src') for foto in pictures]#sacando los links
        #creando si no existe la carpeta de descarga donde se ejecute este archivo
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        if not os.path.isdir('Descargas'):
            os.mkdir('Descargas')
        descargas_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'Descargas' + os.sep
        #descargando las fotos
        for i,picture in enumerate(pictures):
            wget.download(picture,descargas_path + f'{office_id}-{i+1}.jpg')
        time.sleep(2)

    driver.quit()

def main():
    """Funcion que maneja todo"""
    links = office_getter()#scrapeando los links de las oficinas
    if not links: links.append('https://www.regus.com/es-es/canada/vancouver/1500-west-georgia-1286?ws=office-space')
    pictures_getter(links)#scrapeando las fotos
    print('!!!Terminado Pape!!!')
    
if __name__ == '__main__':
    main()