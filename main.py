from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import os


# webdriver setup


options = Options()

options.headless = False
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("window-size=1280,800")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
options.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(executable_path=r'C:\Users\Dell\Desktop\bot\geckodriver.exe', options=options)



driver.get('STRONA_LOGOWANIA')
time.sleep(1)



driver.find_element(By.XPATH, '//*[@id="user_login"]').send_keys('LOGIN')
driver.find_element(By.XPATH, '//*[@id="user_pass"]').send_keys(f'PASSWORD')
driver.find_element(By.XPATH, '//*[@id="wp-submit"]').click()
time.sleep(2)

driver.get('STRONA ZE ZBIOREM ZDJĘĆ - wyświetlane w liscie po 200 elementów')

time.sleep(5)

size = 0
image = 2
ile=""


lista = driver.find_elements(By.CLASS_NAME, 'status-inherit')
counter = 1
lista1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div[2]/div[2]/span[2]/span[3]/span/span').text
counter1 =1

print("Ilość stron "+lista1)


while counter1 != (lista1):
    driver.get('STRONA ZE ZBIOREM ZDJĘĆ - wyświetlane w liscie po 200 elementów z numerem strony &paged='+str(counter1)+'&action2=-1&affected&_ajax_nonce=0b0bd487ed&ps')
    lista = driver.find_elements(By.CLASS_NAME, 'status-inherit')
    print("Ilośc produktów na stronie "+str(len(lista)))

    print("Strona "+str(counter1))
    while counter != (len(lista)+1):
        try:
            print("Produkt "+str(counter))
            el = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/table/tbody/tr[{}]/td[1]/div/span[1]/a'.format(counter))
            href = el.get_attribute('href')
            driver.get(href)

            # pozmieniaj co trzeba na karcie i zaktualizuj
            wgrano = driver.find_element(By.CSS_SELECTOR, '#misc-publishing-actions > div.misc-pub-section.misc-pub-uploadedto > a > strong')
            print(wgrano.text)
            alt = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[1]/div[3]/p[1]/input').text
            input_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[1]/div[3]/p[1]/input').get_attribute('value')
            print(input_field)
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[1]/div[3]/p[1]/input').clear()
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[1]/div[3]/p[1]/input').send_keys(wgrano.text)
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[1]/div[1]/div[1]/input').clear()
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[1]/div[1]/div[1]/input').send_keys(wgrano.text)
            time.sleep(1)
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/input[2]').click()
            time.sleep(7)
            driver.get('STRONA ZE ZBIOREM ZDJĘĆ - wyświetlane w liscie po 200 elementów z numerem strony &paged='+str(counter1)+'&action2=-1&affected&_ajax_nonce=0b0bd487ed&ps')
            time.sleep(7)
            counter += 1
        except NoSuchElementException:
            try:
                size+=int("".join(filter(str.isdigit,driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/form/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[6]/strong').text)))
                image+=1
            except NoSuchElementException:
                print("brak rozmiaru")
            print("Rozmiar nieprzydzielonych zdjęć (KB): "+str(size))
            driver.get('STRONA ZE ZBIOREM ZDJĘĆ - wyświetlane w liscie po 200 elementów z numerem strony &paged='+str(counter1)+'&action2=-1&affected&_ajax_nonce=0b0bd487ed&ps')
            time.sleep(5)
            counter += 1
    else:
        counter1 += 1
        driver.get('STRONA ZE ZBIOREM ZDJĘĆ - wyświetlane w liscie po 200 elementów z numerem strony &paged='+str(counter1)+'&action2=-1&affected&_ajax_nonce=0b0bd487ed&ps')
        counter=1
else:
    if(size<1024):
        ile=(str(size)+" KB")
    elif(size>1024):
        size=size/1024
        ile=(str(size)+" MB")
    elif(size>1048576):
        size=size/1048576
        ile=(str(size)+" GB")
    print("Ilość nieprzydzielonych zdjęć wynosi "+str(image)+", które zajmują: "+ile)
    print("Koniec")
