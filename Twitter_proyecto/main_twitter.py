from login_twitter import login_x
from scraper_twitter import scraper_twitter as st
import pandas

def main():
    driver = login_x()
    df,negative_accounts,positive_accounts,normal_accounts = st(driver,2)
    print(f'\nCuentas analizadas: {positive_accounts + negative_accounts}')
    print(f'Links obtenidos: {normal_accounts}')
    print(f'Cuentas analizadas sin contenido crypto: {negative_accounts}')
    print(f'Cuentas analizadas con contenido crypto: {positive_accounts}\n\n')
    print(df[['account_handle','account_name','number_of_followers','number_of_following','links','joined_date','post_count']])
    df.to_csv(r'D:\Programacion\Proyectos\WebScraping\Twitter_proyecto\crypto_df.csv')
    input('listo ')
    driver.close()
    driver.quit()
    
if __name__ == '__main__':
    main()