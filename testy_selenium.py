import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Import your Flask app
from main import app
# URL to be tested
site_url = 'https:' # replace with url path

username = "test4327498324"
password = "dsahdhdjoi"

def run_flask_app():
    app.run(debug=False, use_reloader=False)

def register_user(driver):
    driver.get(site_url + "/signup")
    user_input = driver.find_element(By.NAME, "username")
    passwd_input = driver.find_element(By.NAME, "password")

    user_input.send_keys(username)
    passwd_input.send_keys(password)

    submitbutton = driver.find_element(By.XPATH, "/html/body/form/div/div/div[2]/input")
    submitbutton.click()
    time.sleep(1)

def test_otworz(driver):
    driver.get(site_url+ "/signup")
    elem = driver.find_element(By.NAME, "username")
    assert elem
    time.sleep(5)
    driver.close()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    time.sleep(5)


    driver = webdriver.Chrome("chromedriver.exe")

    try:
        # Register a user
        register_user(driver)

        # Perform other tests as needed
        test_otworz(driver)
        # sql_injection_test(driver, payloads)

    finally:
        # Quit the WebDriver
        # driver.quit()
        # Join the Flask thread
        flask_thread.join()

  # Allow some time for the injection attempt

# test_otworz()