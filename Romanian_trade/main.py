from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time,calendar,bs4,warnings,datetime
import pandas as pd
import numpy as np

def main(year):
    """Funcion principal"""
    #creando variables principales y accediendo a la pagina
    driver = Driver(browser='Firefox')
    wait = WebDriverWait(driver,15)
    dataset = pd.DataFrame()
    calendario = calendar.Calendar()
    driver.get('https://www.opcom.ro/grafice-ip-raportPIP-si-volumTranzactionat/en')
    #acceptando cookies
    try:
        cookie_button = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@id="cookie_consent_popup"]//button')))
    except TimeoutException:
        print('No salio el cartel de cookies')
        pass
    cookie_button.click()
    #business
    #selecting year
    year_element = driver.find_element(By.XPATH,'//input[@name="year"]')
    year_element.clear()
    year_element.send_keys(year)
    #selecciona el mes
    for mes in range(1,13):
        mes= str(mes)
        if len(mes)==1 : mes = '0'+ mes
        print(f'\nMes {mes} empezado a las: {datetime.datetime.now().strftime("%H:%M")}')
        month_element = driver.find_element(By.XPATH,'//input[@name="month"]')
        month_element.clear()
        month_element.send_keys(mes)
        #coge el dia correcto del mes, lo mete en la caja, refresca la pagina y espera a que cargue la tabal
        for day in calendario.itermonthdays(int(year),int(mes)):
            if day == 16 and mes=='05': break
            if day == 0: continue
            day=str(day)
            if len(day)== 1 : day = '0'+ day
            #metiendo el dia
            try:
                day_element = wait.until(ec.presence_of_element_located((By.XPATH,'//input[@name="day"]')))
            except TimeoutException:
                print('Se produjo un error al cargar la pagina.')
                driver.quit()
                exit()
            day_element.clear()
            day_element.send_keys(day)
            day_element.send_keys(Keys.ENTER)
            time.sleep(3)
            try:
                wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@id="tab_PIP_Vol"]')))
            except TimeoutException:
                print('Se pordujo un error al cargar la pagina.')
                driver.quit()
                exit()
            #para obtener la tabla y guardarla
            table = bs4.BeautifulSoup(driver.page_source,'html.parser').find('div',{'id':"tab_PIP_Vol"}).find('table')
            df = pd.read_html(str(table))[0]
            date = f'{year}-{mes}-{day}'
            df['Date'] = np.array(([date])*(df.shape[0]))
            if len(dataset)== 0 :
                dataset = df
            else:
                dataset= pd.concat([dataset,df])
        print(f'!!! Mes {mes} escrapeado !!!\nMes {mes} terminado a las: {datetime.datetime.now().strftime("%H:%M")}')
        if day == 16 and mes=='05': break
    #salvando el dataset segun el año que sea
    dataset = dataset.reset_index(drop=True)
    dataset.to_csv(f'Results\\Trade_in_{year}.csv')
    driver.quit()
    exit()

if __name__ == '__main__':
    warnings.simplefilter(action='ignore', category=FutureWarning)
    main(input('Cual año hago?: '))