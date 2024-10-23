from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time

account_2 = 'david'
account_pw = '61094436'

def initialize_driver():
    global driver
    options = Options()
    options.use_chromium = True
    options.add_argument("--ignore-certificate-errors")
    #options.add_argument("--headless")
    driver = webdriver.Edge(options=options)
    driver.get("https://192.168.10.108")

    try:
        # Wait for the username field to be interactable
        username = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "uname"))
        )
        password = driver.find_element(By.ID, "pswd")
        username.send_keys(account_2)
        password.send_keys(account_pw)

        # Click the submit button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/form[2]/div/div[3]/button'))
        )
        submit_button.click()
        time.sleep(4)

        # Navigate to the specified URL
        driver.get("https://192.168.10.108/monitoringdoor.htm?1a09623")
        time.sleep(2)  # Optional: wait for 2 seconds to ensure the page loads

        # Change button text to "Open Door"
        button.config(text="Open Door")

    except Exception as e:
        print(f"An error occurred during initialization: {e}")
        driver.quit()

def click():
    print("Button clicked") # This will print to the console        

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/div/table/tbody/tr[4]/td[3]/a'))
        ).click()
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[6]/div/div/div/div[3]/span[2]'))
        ).click()
        time.sleep(3)

        # Change button text to "Door Opened!"
        button.config(text="Door Opened!")

        # Schedule the button text to change back to "Open Door" after 7 seconds
        window.after(7000, reset_button_text)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def reset_button_text():
    button.config(text="Open Door")
    initialize_driver()

window = Tk()
button = Button(window, text="Connecting...")
button.config(command=click)    
button.config(font=('Arial', 20,'bold')) 
button.config(bg='yellow') 
button.config(fg='black')  
button.pack()

# Force the GUI to update the button text to "Connecting..."
window.update_idletasks()

# Initialize the driver and load the page
initialize_driver()

try:
    window.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user")
    window.destroy()