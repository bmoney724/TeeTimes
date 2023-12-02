import winsound
import smtplib
import selenium
from time import sleep
from time import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from emailFactory import emailFactory
import time

# Config
###########################################################

# Set the maximum time to attempt the operation (in seconds)
max_duration = 60*60*1  # 1 hour in this example

# Set the interval between attempts (in seconds)
interval = 5

# this sets the sound to be made upon finding a valid tee time
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 5000  # Set Duration To 1000 ms == 1 second

from_address = "bmolloy724@gmail.com"
to_address = "bmolloy724@gmail.com"
emailService = emailFactory()

# this will be the time that it will stop looking for times at (ex: "04:00 pm")
unAcceptableTime = "01:00 pm"
# number of golfers
golfers = 4

# day of the month (ex. "july")
month = "december"
day = "2"

###########################################################

start_time = time.time()

while time.time() - start_time < max_duration:
    try:

        # Using Chrome (can be whatever browser)
        service = Service()
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        # Open the website
        driver.get('https://sterling.chelseareservations.com/golf/bookingadmin.aspx')

        # Select the num of golfers
        numberOfGolfers = driver.find_element(By.ID, "ddlQuantity")
        numberOfGolfers.send_keys(golfers)
        sleep(1)

        # Select the month
        numberOfGolfers = driver.find_element(By.NAME, "ddlMonth")
        numberOfGolfers.send_keys(month)
        numberOfGolfers.click()
        sleep(1)

        # ensure the calendar is displaying
        displayCalendar = driver.find_element(By.NAME, "btnDisplay")
        displayCalendar.click()
        sleep(1)

        # select the desired day
        element = driver.find_element(By.LINK_TEXT, day)
        element.click()

        sleep(5)

        allTimes = ["06:00 am  Hole-01", "06:10 am  Hole-01""06:20 am  Hole-01", "06:30 am  Hole-01",
                    "06:40 am  Hole-01", "06:50 am  Hole-01", "07:00 am  Hole-01", "07:10 am  Hole-01",
                    "07:20 am  Hole-01", "07:30 am  Hole-01", "07:40 am  Hole-01", "07:50 am  Hole-01",
                    "08:00 am  Hole-01", "08:10 am  Hole-01", "08:20 am  Hole-01", "08:30 am  Hole-01",
                    "08:40 am  Hole-01",
                    "08:50 am  Hole-01", "09:00 am  Hole-01", "09:10 am  Hole-01", "09:20 am  Hole-01",
                    "09:30 am  Hole-01", "09:40 am  Hole-01", "09:50 am  Hole-01", "10:00 am  Hole-01",
                    "10:10 am  Hole-01", "10:20 am  Hole-01", "10:30 am  Hole-01", "10:40 am  Hole-01",
                    "10:50 am  Hole-01", "11:00 am  Hole-01", "11:10 am  Hole-01", "11:20 am  Hole-01",
                    "11:30 am  Hole-01", "11:40 am  Hole-01", "11:50 am  Hole-01", "12:00 pm  Hole-01",
                    "12:10 pm  Hole-01", "12:20 pm  Hole-01", "12:30 pm  Hole-01", "12:40 pm  Hole-01",
                    "12:50 pm  Hole-01", "01:00 pm  Hole-01", "01:10 pm  Hole-01", "01:20 pm  Hole-01",
                    "01:30 pm  Hole-01", "01:40 pm  Hole-01", "01:50 pm  Hole-01", "02:00 pm  Hole-01",
                    "02:10 pm  Hole-01", "02:20 pm  Hole-01", "02:30 pm  Hole-01", "02:40 pm  Hole-01",
                    "02:50 pm  Hole-01", "03:00 pm  Hole-01", "03:10 pm  Hole-01", "03:20 pm  Hole-01",
                    "03:30 pm  Hole-01", "03:40 pm  Hole-01", "03:50 pm  Hole-01", "04:00 pm  Hole-01",
                    "04:10 pm  Hole-01", "04:20 pm  Hole-01", "04:30 pm  Hole-01", "04:40 pm  Hole-01",
                    "04:50 pm  Hole-01", "05:00 pm  Hole-01", "05:10 pm  Hole-01", "05:20 pm  Hole-01",
                    "05:30 pm  Hole-01", "05:40 pm  Hole-01", "05:50 pm  Hole-01", "06:00 pm  Hole-01",
                    "06:10 pm  Hole-01", "06:20 pm  Hole-01", "06:30 pm  Hole-01", "06:40 pm  Hole-01",
                    "06:50 pm  Hole-01", "07:00 pm  Hole-01"
                    ]
        while time.time() - start_time < max_duration:
            for teeTime in allTimes:
                if teeTime[0:8] == unAcceptableTime:
                    break
                currentTimeLocation = driver.page_source.find(teeTime)
                if currentTimeLocation != -1:
                    time_found = driver.page_source[currentTimeLocation:currentTimeLocation + 17]
                    emailService.compose_email(from_address, to_address, "Sterling Tee Time!",
                                               "we found this time: " + time_found)
                    print(time_found)
                    winsound.Beep(frequency, duration)
                    sleep(15*60)
            sleep(5)
            displayTimes = driver.find_element(By.ID, "btnDisplayTimes")
            displayTimes.click()
            print("refreshed times: " + str(datetime.now()))
            sleep(1)
        driver.quit()

    except Exception as e:
        # Handle the exception (optional)
        print(f"Error: {e}")

    # Wait for the specified interval before the next attempt
    time.sleep(interval)
    continue
else:
    print('times up!')

