import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load credentials
load_dotenv(dotenv_path="/Users/aayush/Projects/court_bot/.env")
COURT_URL= os.getenv("COURT_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
AMENITY_ID = os.getenv("AMENITY_ID")

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")  # Optional: run in background

print("[INIT] Launching Chrome browser...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

def wait_until(target_time: datetime.datetime):
    print(f"[WAIT] Waiting until {target_time.strftime('%H:%M:%S.%f')[:-3]}...")
    last_logged_second = -10
    while True:
        now = datetime.datetime.now()
        if now >= target_time:
            print(f"[WAIT] Hit target: {now.strftime('%H:%M:%S.%f')[:-3]}")
            break
        if now.second % 10 == 0 and now.second != last_logged_second:
            print(f"[WAIT] Time now: {now.strftime('%H:%M:%S')} — still waiting...")
            last_logged_second = now.second
        time.sleep(0.001)

def login():
    print("[LOGIN] Navigating to login page...")
    driver.get(COURT_URL)
    wait.until(EC.presence_of_element_located((By.ID, "UserName"))).send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "submit-sign-in").click()
    time.sleep(3)
    print("[LOGIN] Logged in successfully.")

def navigate_to_basketball_reservation():
    print("[NAVIGATE] Opening Basketball Court reservation form...")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "reserve-amenity-btn")))
    buttons = driver.find_elements(By.CLASS_NAME, "reserve-amenity-btn")
    for btn in buttons:
        if btn.get_attribute("data-amenity") == AMENITY_ID:
            btn.click()
            print("[NAVIGATE] Clicked 'Reserve Online' for Basketball Court.")
            break
    else:
        print("[ERROR] Reserve button not found.")
        driver.quit()
        exit()
    wait.until(EC.presence_of_element_located((By.ID, "resv-date")))
    print("[NAVIGATE] Reservation form loaded.")

def refresh_and_fill():
    print("[ACTION] Refreshing at 12:00:00.000...")
    t0 = time.perf_counter()
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.ID, "resv-date")))
    t1 = time.perf_counter()
    print(f"[PERF] Page refreshed in {(t1 - t0)*1000:.2f} ms")

    t_fill_start = time.perf_counter()

    # Prepare values
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_str = tomorrow_date.strftime("%-m/%-d/%Y")
    day_name = tomorrow_date.strftime("%A")
    time_slot_value = f"{day_name}-7:00 PM-8:00 PM "

    print(f"[FORM] Target slot: {time_slot_value.strip()} for {tomorrow_str}")

    # Pre-locate fields
    date_field = driver.find_element(By.ID, "resv-date")
    dropdown = Select(driver.find_element(By.ID, "SelStartTime"))
    num_field = driver.find_element(By.ID, "NumberOfPeople")
    name_field = driver.find_element(By.ID, "ReservationNames")

    # Fill fields using JavaScript (instant)
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_field)
    driver.execute_script("arguments[0].value = arguments[1]", date_field, tomorrow_str)
    dropdown.select_by_value(time_slot_value)
    driver.execute_script("arguments[0].value = arguments[1]", num_field, "1")
    driver.execute_script("arguments[0].value = arguments[1]", name_field, "AAYUSH VERMA")

    t_fill_end = time.perf_counter()
    print(f"[PERF] Form filled in {(t_fill_end - t_fill_start)*1000:.2f} ms")

def submit_reservation():
    t_submit_start = time.perf_counter()
    now = datetime.datetime.now()
    print(f"[SUBMIT] Clicking Reserve at {now.strftime('%H:%M:%S.%f')[:-3]}")
    submit_btn = driver.find_element(By.ID, "submit-new-reservation")
    driver.execute_script("arguments[0].removeAttribute('disabled')", submit_btn)
    submit_btn.click()
    t_submit_end = time.perf_counter()
    print(f"[PERF] Submit clicked in {(t_submit_end - t_submit_start)*1000:.2f} ms")
    print("✅ Reservation submitted successfully!")

if __name__ == "__main__":
    try:
        login()
        navigate_to_basketball_reservation()

        # Set target times
        midnight = datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=1),
            datetime.time(0, 0, 0)
        )
        refresh_time = midnight
        submit_time = midnight + datetime.timedelta(milliseconds=200)

        wait_until(refresh_time)
        refresh_and_fill()

        wait_until(submit_time)
        submit_reservation()

    except Exception as e:
        print("[FATAL ERROR]", e)
    finally:
        print("[EXIT] Closing browser.")
        time.sleep(3)
        driver.quit()