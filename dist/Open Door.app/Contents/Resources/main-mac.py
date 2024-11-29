from tkinter import *
from PIL import Image, ImageTk
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import sys

# Credentials
account_2 = 'david'
account_pw = '61094436'

def initialize_driver():
    global driver
    try:
        # Configure ChromeDriver options
        options = Options()
        options.add_argument("--ignore-certificate-errors")  # Bypass SSL errors
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")  # Optional: run in headless mode
        options.add_argument("--no-sandbox")

        # Initialize ChromeDriver
        driver = webdriver.Chrome(options=options)
        driver.get("https://192.168.10.108")

        # Log in
        username = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "uname"))
        )
        password = driver.find_element(By.ID, "pswd")
        username.send_keys(account_2)
        password.send_keys(account_pw)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/form[2]/div/div[3]/button'))
        )
        submit_button.click()
        time.sleep(4)

        # Navigate to the monitoring page
        driver.get("https://192.168.10.108/monitoringdoor.htm?1a09623")
        time.sleep(2)  # Ensure the page loads

        # Update button text
        button.config(text="Open Door")
    except Exception as e:
        print(f"An error occurred during initialization: {e}")
        if driver:
            driver.quit()

def click():
    print("Button clicked")

    try:
        # Perform button click actions in the web interface
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/div/table/tbody/tr[4]/td[3]/a'))
        ).click()
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[6]/div/div/div/div[3]/span[2]'))
        ).click()
        time.sleep(3)

        # Update button text
        button.config(text="Door Opened!")
        window.after(7000, reset_button_text)  # Reset after 7 seconds
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def reset_button_text():
    button.config(text="Open Door")
    initialize_driver()

# Set up the GUI
window = Tk()
window.title("Open Door")
window.configure(bg="black")
window.geometry("420x300")
button = Button(window, text="Connecting...")
button.config(command=click)
button.config(font=('Arial', 20, 'bold'))
button.config(bg='yellow')
button.config(fg='black')
button.pack()


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for development and PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Set the window icon
icon_path = resource_path("favicon.ico")
try:
    window.iconbitmap(icon_path)
except Exception as e:
    print(f"Error setting window icon: {e}")

# Load and display the favicon.ico
try:
    img = Image.open(icon_path)
    img = img.resize((64, 64))
    icon = ImageTk.PhotoImage(img)
    icon_label = Label(window, image=icon, bg="black")
    icon_label.pack(pady=10)
except Exception as e:
    print(f"Error loading favicon.ico: {e}")


button = Button(window, text="Connecting...", command=click, font=('Arial', 20, 'bold'),
                bg='yellow', fg='black')
button.pack(pady=10)


# Force GUI to update while connecting
window.update_idletasks()

# Initialize the Selenium WebDriver
initialize_driver()

try:
    window.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user")
    window.destroy()
