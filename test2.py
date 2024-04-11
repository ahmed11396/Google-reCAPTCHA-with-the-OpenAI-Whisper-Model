from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests

driver = None

def transcribe(url):
    with open('.temp', 'wb') as f:
        f.write(requests.get(url).content)
    return "Transcribed Text"  # Placeholder for actual transcription logic

def click_checkbox(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    driver.switch_to.default_content()

def request_audio_version(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.ID, "recaptcha-audio-button").click()

def solve_audio_captcha(driver):
    text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute('src'))
    driver.find_element(By.ID, "audio-response").send_keys(text)
    driver.find_element(By.ID, "recaptcha-verify-button").click()

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
      
        driver.get("https://www.google.com/recaptcha/api2/demo")
        click_checkbox(driver)
        time.sleep(1)
        request_audio_version(driver)
        time.sleep(1)
        solve_audio_captcha(driver)
        time.sleep(10)
    finally:
        if driver is not None:
            driver.quit()
