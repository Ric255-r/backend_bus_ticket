from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# fungsi untuk scrape data
def scraper(url):
  driver = None
  try:
    # Config webdriver untuk pake headless firefox
    options = Options()
    # options.add_argument('-headless')
    options.set_preference("javascript-enabled", False)
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Firefox(options=options)

    # ambil url
    driver.get(url)

    # Selenium will wait for a maximum of 20 seconds for an element matching the given criteria to be found. 
    # If no element is found in that time, Selenium will raise an error.
    try:
      wait = WebDriverWait(driver, timeout=20)
      wait.until(EC.visibility_of_element_located(By.CLASS_NAME, 'css-1dbjc4n'))
    except:
      raise LookupError("Tidak Ada Elemen yg Spesifik")
    
    # BeautifulSoup bakal ngeparse urlnya
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Siapkan variable untuk data json
    scrapedData = []

    all_data = soup.find_all('div', class_='css-1dbjc4n')

    for index, data in enumerate(all_data):
       # Start from the 10th element (index 9)
      if index >= 9:
        # ambil teks dari spesifik element
        judul = data.find('h2').text
        deskripsi = data.find('p').text

        try:
          gambar = data.find('img', attrs={'loading': 'lazy'})
          gambar = gambar['src'] if gambar else ''
          
        except IndexError:
          gambar = ''

        # Append Scraped Datanya
        scrapedData.append({
          "judul": judul,
          "deskripsi": deskripsi,
          "gambar": gambar
        })

    return scrapedData

  except Exception as e:
    # Print the error message
    print('An error occurred: ', e)

  finally:
    if driver:
      driver.quit()
