from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import time


def scraper_twitter(driver,total):
    """Funcion que scrapea las paginas, selecciona si el perfil esta asociado a las crypto y guarda
    todos sus siguiendo y sigue iterando hasta llegar a 50 perfiles"""
    
    #configurando el wait, dataframe, terminos asociados a crypto, y los dos sets que contienen los perfiles
    wait = WebDriverWait(driver,5)
    terms = ['CRYPTO','BTC','NFT','WEB3','ALTCOINS','Crypto','Btc','Web3','Altcoins','crypto','btc','web3','altcoins','ETH','Eth','eth']
    df = pd.DataFrame(columns=['account_handle','account_name','number_of_followers','number_of_following','links','description','joined_date','post_count'])
    normal_accounts,negative_accounts,positive_accounts = [],[],[]
    normal_accounts.append('https://twitter.com/cburniske')

    #bucle principal
    #itera hatsa que haya n perfiles filtrados
    position = 0
    while 1:
        if len(positive_accounts) == total: break
        for perfil in normal_accounts[position:]:
            if len(positive_accounts) == total: break
            position += 1
            green = 0
            if perfil in positive_accounts or perfil in negative_accounts: continue
            driver.get(perfil)
            #espera a que aparezca la descripcion, y si no tienen o no contiene los terminos brinca al proximo perfil
            #y de tenerlo lo guarda
            try:
                description = wait.until(ec.visibility_of_element_located((By.XPATH,'html/body//main//div[@data-testid="UserDescription"]'))).text
            except TimeoutException:
                continue
            for term in terms:
                if term in description: green+=1
            if not green: 
                negative_accounts.append(perfil)
                continue
            #guardando perfil filtrado
            positive_accounts.append(perfil)
            time.sleep(3)

            #ya habiendo filtrado que la cuenta es positiva guarda los datos
            try:
                links = wait.until(ec.visibility_of_element_located((By.XPATH,'html/body//main//a[@data-testid="UserUrl"]'))).text
            except TimeoutException:
                links = 'Unknown'
            elementos = {
                'account_handle' : driver.find_element(By.XPATH,'html/body//main//div[@data-testid="UserName"]/div[1]/div[1]/div[2]').text,
                'account_name' : driver.find_element(By.XPATH,'html/body//main//div[@data-testid="UserName"]/div[1]/div[1]/div[1]').text,
                'number_of_followers' : driver.find_element(By.XPATH,'html/body//main//div[@data-testid="primaryColumn"]//span[text()="Seguidores"]/../../span').text,
                'number_of_following' : driver.find_elements(By.XPATH,'html/body//main//div[@data-testid="primaryColumn"]//span[text()="Siguiendo"]/../../span[1]')[-1].text,
                'links' : links,
                'description' : description,
                'joined_date' : driver.find_element(By.XPATH,'html/body//main//span[@data-testid="UserJoinDate"]').text,
                'post_count' : driver.find_element(By.XPATH,'html/body//main//div[@data-testid="primaryColumn"]/div[1]/div[1]//h2/../div').text,
            }

            #agregar elementos al dataframe
            datos = np.array([
                elementos['account_handle'],
                elementos['account_name'],
                elementos['number_of_followers'],
                elementos['number_of_following'],
                elementos['links'],
                elementos['description'],
                elementos['joined_date'],
                elementos['post_count']
            ])
            new = pd.DataFrame(data=[datos],columns=df.columns)
            df = pd.concat([new,df])
            
            #obteniendo siguiendos
            driver.get('https://twitter.com/' + str(elementos['account_handle'][1:]) + '/following')
            time.sleep(2)
            for x in range(1,100):
                try:
                    driver.find_element(By.XPATH,'//div[@data-testid="cellInnerDiv"]/../div[last()]//div[contains(@data-testid,"UserAvatar")]')
                except:
                    break
                enlaces = driver.find_elements(By.XPATH,'//div[@data-testid="cellInnerDiv"]//div[contains(@data-testid,"UserAvatar")]//a')
                for enlace in enlaces: normal_accounts.append(enlace.get_attribute('href'))
                altura = 700*x
                driver.execute_script(f'window.scrollTo(0, {altura});')
                time.sleep(0.5)

    return df,len(negative_accounts),len(positive_accounts),len(set(normal_accounts))
            