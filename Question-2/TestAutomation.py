from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

service = Service("chromedriver.exe")
chrome_options = Options()
driver = webdriver.Chrome(service=service, options=chrome_options)

def select_country(country_name):
    country_name_cleaned = country_name.split(" -")[0]

    to_country = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='country']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", to_country)
    to_country.clear()
    to_country.send_keys(country_name_cleaned)

    country_option_xpath = f"//mat-option//small[contains(text(), '{country_name_cleaned}')]"
    country_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, country_option_xpath))
    )
    
    driver.execute_script("arguments[0].scrollIntoView();", country_option)
    country_option.click()

try:
    driver.get("https://pos.com.my/send/ratecalculator")
    driver.maximize_window()
    time.sleep(2)

    from_country = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='flex flex-col ml-1']//span[@class='font-bold' and text()='Malaysia']"))
    )
    from_country_text = from_country.text
    if from_country_text == "Malaysia":
        print("Verified: 'From' country is set to 'Malaysia' and is not editable.")
    else:
        print("Error: 'From' country is either not 'Malaysia' or is editable.")

    from_postcode = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='postcodeFrom']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", from_postcode)
    from_postcode.clear()
    from_postcode.send_keys("35600") # Set postcode "From" Malaysia


    country_to_select = "India - IN"  # Set country here
    select_country(country_to_select)


    try:
        if country_to_select == "Malaysia - MY":
            to_postcode = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='postcodeTo' and @type='number']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", to_postcode)
            to_postcode.clear()
            to_postcode.send_keys("50000")  # Set postcode "To" Malaysia

        else:
            to_postcode = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Postcode (optional)' and @type='text']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", to_postcode)
            to_postcode.clear()
            to_postcode.send_keys("")  # Optional postcode, can be left blank

    except TimeoutException:
        print("Error: 'postcode To' field could not be located for the selected country.")

    weight = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='itemWeight']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", weight)
    weight.clear()
    weight.send_keys("1") # Set weight here

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "floating-bar"))
    )

    calculate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'bg-red-600') and text()=' Calculate ']"))
    )
    calculate_button.click()

    quote_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Your Quote')]"))
    )

    specific_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Get your domestic or international parcel quotation')]"))
    )

    driver.execute_script("arguments[0].scrollIntoView();", specific_element)

    driver.save_screenshot("rate_calculator_input.png")
    print("Screenshot taken from the Postcode, Country, and Weight Information")

    driver.execute_script("arguments[0].scrollIntoView();", quote_header)

    driver.save_screenshot("rate_calculator_quote.png")
    print("Screenshot taken for the quote information.")

finally:
    driver.quit()
    print("Test completed and browser closed.")
