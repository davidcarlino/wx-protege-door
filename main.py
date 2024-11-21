from tkinter import *
from PIL import Image, ImageTk  # Pillow library for image handling
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time
import threading

# Account credentials
account_2 = 'david'
account_pw = '61094436'

# Initialize Selenium WebDriver in headless mode
def initialize_driver():
    global driver
    options = Options()
    options.use_chromium = True
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")  # Run in headless mode (no browser window)
    options.add_argument("--disable-gpu")  # Optional: Useful for compatibility
    options.add_argument("--log-level=3")  # Suppress most browser logs
    driver = webdriver.Edge(options=options)
    driver.get("https://192.168.10.108")

    try:
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

        driver.get("https://192.168.10.108/monitoringdoor.htm?1a09623")
        time.sleep(2)
        button.config(text="Open Door")
        start_reloading_thread()

    except Exception as e:
        print(f"An error occurred during initialization: {e}")
        driver.quit()

# Periodically reload the page
def reload_page_periodically():
    while True:
        try:
            print("Reloading webpage to prevent timeout...")
            driver.get("https://192.168.10.108/monitoringdoor.htm?1a09623")
            time.sleep(300)
        except Exception as e:
            print(f"An error occurred during page reload: {e}")
            break

def start_reloading_thread():
    reloading_thread = threading.Thread(target=reload_page_periodically, daemon=True)
    reloading_thread.start()

def click():
    print("Button clicked")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/div/table/tbody/tr[4]/td[3]/a'))
        ).click()
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[6]/div/div/div/div[3]/span[2]'))
        ).click()
        time.sleep(3)

        button.config(text="Door Opened!")
        window.after(7000, reset_button_text)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def reset_button_text():
    button.config(text="Open Door")
    initialize_driver()

# Main window setup
window = Tk()
window.title("Control Panel")
window.configure(bg="black")
window.geometry("320x180")

# Set the window icon
try:
    window.iconbitmap("favicon.ico")
except Exception as e:
    print(f"Error setting window icon: {e}")

# Load and display the favicon.ico
try:
    img = Image.open("favicon.ico")
    img = img.resize((64, 64))
    icon = ImageTk.PhotoImage(img)
    icon_label = Label(window, image=icon, bg="black")
    icon_label.pack(pady=10)
except Exception as e:
    print(f"Error loading favicon.ico: {e}")

# Add the button below the icon
button = Button(window, text="Connecting...", command=click, font=('Arial', 20, 'bold'),
                bg='yellow', fg='black')
button.pack(pady=10)

# Force the GUI to update the button text to "Connecting..."
window.update_idletasks()

# Initialize the driver and load the page
initialize_driver()

# Start the Tkinter event loop
try:
    window.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user")
    window.destroy()
