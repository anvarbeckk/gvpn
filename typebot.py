from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pyautogui

# Path to the ChromeDriver executable
CHROME_DRIVER_PATH = '/opt/homebrew/bin/chromedriver'

# Constants for coordinates and delays
ACCEPT_COOKIES_COORDS = (827, 818)
LOGIN_LOGO_COORDS = (1223, 268)
EMAIL_FIELD_COORDS = (942, 470)
PASSWORD_FIELD_COORDS = (942, 523)
SIGN_IN_BUTTON_COORDS = (942, 607)
MONKEYTYPE_START_COORDS = (222, 258)
INITIAL_DELAY = 3
MODE_SELECTION_DELAY = 4

# Initialize WebDriver
chrome_service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_service)

def login():
    driver.get('https://monkeytype.com/')
    driver.set_window_position(0, 0)
    pyautogui.FAILSAFE = True

    user = pyautogui.prompt("Enter the username:")
    pasw = pyautogui.password("Enter the password:")

    time.sleep(2)
    pyautogui.click(*ACCEPT_COOKIES_COORDS)  # Accept cookies
    time.sleep(2)
    pyautogui.click(*LOGIN_LOGO_COORDS)  # Click login logo
    time.sleep(1)
    pyautogui.click(*EMAIL_FIELD_COORDS)  # Click email field
    pyautogui.write(user)
    time.sleep(1)
    pyautogui.click(*PASSWORD_FIELD_COORDS)  # Click password field
    pyautogui.write(pasw)
    time.sleep(1)
    pyautogui.click(*SIGN_IN_BUTTON_COORDS)  # Click sign in button
    time.sleep(1)

def write_words(delay):
    try:
        while len(driver.find_elements(By.CLASS_NAME, "word")) != 0:
            active_word = driver.find_element(By.CSS_SELECTOR, ".word.active")
            letters = [letter.text for letter in active_word.find_elements(By.TAG_NAME, "letter")] + [' ']
            pyautogui.write(letters, interval=delay)
    except Exception as e:
        print(f"Error during typing: {e}")

def start_typing_test(delay):
    time.sleep(INITIAL_DELAY)
    pyautogui.doubleClick(*MONKEYTYPE_START_COORDS)  # Start Monkeytype
    pyautogui.doubleClick(*MONKEYTYPE_START_COORDS)  # Start Monkeytype again

    time.sleep(1)
    pyautogui.alert("Please select the mode and the time you want and THEN press OK!")

    time.sleep(MODE_SELECTION_DELAY)
    driver.set_window_position(0, 0)
    write_words(delay)

def display_data(data):
    keys = list(data.keys())
    print(*keys, sep='\t')
    for i in range(len(next(iter(data.values())))):
        values = [str(data[key][i]) for key in keys]
        print(*values, sep='\t\t')
    print("--------------------------------------")

def main():
    ans = "YES"
    login()
    data = {"wpm": [], "accuracy": [], "consistency": [], "delay": []}

    while ans == "YES":
        pyautogui.scroll(1000)
        pyautogui.scroll(1000)
        pyautogui.doubleClick(*MONKEYTYPE_START_COORDS)

        delay = float(pyautogui.prompt(text='Enter the delay (seconds)\n0 is instantaneous', default='0.1'))
        start_typing_test(delay)

        # Retrieve and store WPM, accuracy, and consistency values
        try:
            wpm = driver.find_element(By.CSS_SELECTOR, ".group.wpm .bottom").text
            accuracy = driver.find_element(By.CSS_SELECTOR, ".group.acc .bottom").text
            consistency = driver.find_element(By.CSS_SELECTOR, ".group.flat.consistency .bottom").text
            data["wpm"].append(wpm)
            data["consistency"].append(consistency)
            data["accuracy"].append(accuracy)
            data["delay"].append(delay)
        except Exception as e:
            print(f"Error retrieving typing results: {e}")

        display_data(data)
        ans = pyautogui.confirm(text='Wanna type again?', title='Continue?', buttons=['YES', 'NO'])

    driver.quit()

if __name__ == "__main__":
    main()
