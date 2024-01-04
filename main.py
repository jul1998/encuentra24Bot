import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
import requests


class Apartments:

    def __init__(self):
        self.page_number = 1
        self.URL = f"https://www.encuentra24.com/costa-rica-es/bienes-raices-alquiler-apartamentos/heredia-provincia.{self.page_number}?q=withcat.bienes-raices-alquiler-apartamentos,bienes-raices-alquiler-casas|f_rent.-300000|f_rooms.1-3|f_currency.CRC"
        self.FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScNUyd1Yy9AvQT-LBlV_SDTWmnDvs43vHVUtehVCfsYU9stVw/viewform?usp=sf_link"
        self.page = requests.get(self.URL)
        self.soup = bs4.BeautifulSoup(self.page.content, "html.parser")
        self.apartment_titles_list = []
        self.apartment_description_list = []
        self.apartment_prices_list = []
        self.apartment_locations = []
        self.apartment_links = []
        self.driver = webdriver.Chrome()

    def is_last_page(self):
        pagination_elements = self.soup.find_all(class_="pagination")

        if not pagination_elements:
            return True  # Assuming there is only one pagination element, and if none is found, it's the last page

        next_page_element = pagination_elements[0].find('li', class_='arrow-next')

        return not next_page_element


    def get_next_page(self):
        self.page_number += 1
        self.URL = f"https://www.encuentra24.com/costa-rica-es/bienes-raices-alquiler-apartamentos/heredia-provincia.{self.page_number}?q=withcat.bienes-raices-alquiler-apartamentos,bienes-raices-alquiler-casas|f_rent.-300000|f_rooms.1-3|f_currency.CRC"
        self.page = requests.get(self.URL)
        self.soup = bs4.BeautifulSoup(self.page.content, "html.parser")
    def get_titles(self):
        raw_apartment_titles = self.soup.find_all(class_="ann-ad-tile__title")
        self.apartment_titles_list = [apartment_title.text.strip() for apartment_title in raw_apartment_titles]
        print(self.apartment_titles_list)


    def get_descriptions(self):
        raw_apartment_descriptions = self.soup.find_all(class_="ann-ad-tile__short-description")
        self.apartment_description_list = [apartment_description.text.strip() for apartment_description in
                                      raw_apartment_descriptions]
        print(self.apartment_description_list)


    def get_prices(self):
        raw_apartment_price = self.soup.find_all(class_="ann-ad-tile__price")
        self.apartment_prices_list = [apartment_price.text.strip().replace(",","") for apartment_price in raw_apartment_price]
        print(self.apartment_prices_list)

    def get_addresses(self):
        raw_aparment_addresses = self.soup.find_all(class_="ann-ad-tile__footer-item")
        apartment_address_list = [address.text.strip() for address in raw_aparment_addresses]
        self.apartment_locations = [location for index, location in enumerate(apartment_address_list) if index % 2 != 0]
        print(self.apartment_locations)

    def get_links(self):
        raw_apartment_links = self.soup.find_all(class_="ann-ad-tile__title")
        self.apartment_links = []
        for title in raw_apartment_links:
            link = title.get("href")
            functional_link = f"https://www.encuentra24.com/{link}"
            self.apartment_links.append(functional_link)
        print(self.apartment_links)



    def autofill_form(self):
        self.driver.get(self.FORM_URL)
        print(len(self.apartment_titles_list))
        print(len(self.apartment_description_list))
        print(len(self.apartment_prices_list))
        print(len(self.apartment_locations))
        print(len(self.apartment_links))

        time.sleep(2)
        while True:
            for index in range(len(self.apartment_titles_list)):
                time.sleep(2)
                title_entry = self.driver.find_element(By.XPATH, "//div[@class='lrKTG']//div[1]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
                title_entry.click()
                title_entry.send_keys(self.apartment_titles_list[index])

                description_entry = self.driver.find_element(By.XPATH, "//div[@role='list']//div[2]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
                description_entry.click()
                description_entry.send_keys(self.apartment_description_list[index])


                location_entry = self.driver.find_element(By.XPATH,"//div[@class='teQAzf']//div[3]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
                location_entry.click()
                try:
                    location_entry.send_keys(self.apartment_locations[index])
                except:
                    location_entry.send_keys("No location")


                price_entry = self.driver.find_element(By.XPATH,"//div[4]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
                price_entry.click()
                price_entry.send_keys(self.apartment_prices_list[index])


                link_entry = self.driver.find_element(By.XPATH,"//div[5]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
                link_entry.click()
                link_entry.send_keys(self.apartment_links[index])
                time.sleep(3)


                submit_button = self.driver.find_element(By.XPATH,"//div[@class='uArJ5e UQuaGc Y5sE8d VkkpIf QvWxOd']//span[@class='l4V7wb Fxmcue']")
                submit_button.click()
                time.sleep(3)

                another_response = self.driver.find_element(By.LINK_TEXT,"Enviar otra respuesta")
                another_response.click()

            if  self.is_last_page():
                print("No more pages")
                break
            else:
                self.get_next_page()
                print("Going to next page")
                print(self.page_number)
                print(self.URL)
                self.get_titles()
                self.get_descriptions()
                self.get_prices()
                self.get_addresses()
                self.get_links()
                time.sleep(3)










data = Apartments()
data.get_titles()
data.get_descriptions()
data.get_prices()
data.get_addresses()
data.get_links()
data.autofill_form()