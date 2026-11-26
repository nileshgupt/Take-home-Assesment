
import re
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 1. Take USername from USer
valid_buyer_username = ["buyer1", "buyer2", "buyer3"]
username = input("Enter username (buyer1/buyer2/buyer3/seller1/seller2/seller3): ").strip()
if username not in valid_buyer_username:
    raise Exception("Invalid username ,Please enter valid username")

# 2. Chrome options (insecure warning remove)
options = Options()
options.add_argument("--disable-features=HttpsFirstBalancedModeAutoEnable,HttpsUpgrades")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_experimental_option("detach", True)

prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False,
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# 3. Explicit Wait setup
wait = WebDriverWait(driver, 15)

# 4. Website open

driver.get("http://13.200.185.1/c/nilesh-7cb355/login")

#5. Login in Application
wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Test@123")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']"))).click()

# 6. Print Title aftre Login complete
print("Login successful! Page title:", driver.title)

# To search item in catalogue
wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@name,'q')]"))).send_keys("Moong")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Search']"))).click()
time.sleep(2)

# To select Item
wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Chef\'s Moong Dal"]'))).click()
page_text = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).text
stock_match = re.search(r"In stock:\s*(\d+)", page_text)
case_match = re.search(r"Case of\s*(\d+)", page_text).group(1)
case_price = float(re.search(r"Case of\s*\d+:\s*₹\s*([\d,.]+)", page_text).group(1).replace(",", ""))

available_Stock = int(stock_match.group(1))
per_case_quantity = int(case_match)

min_cases = 1
while (min_cases * case_price) < 2000:
    min_cases = min_cases + 1

print(f"Case Price: Rs {case_price} and Available Stock: {available_Stock} pieces and ({available_Stock // per_case_quantity} cases)")
print(f"For Rs 2,000+, minimum order required: {min_cases} cases or  ({min_cases * per_case_quantity} pieces).")

if available_Stock <= 0 or (min_cases * per_case_quantity) > available_Stock:
    print(f"OUT OF STOCK: Available stock ({available_Stock} pieces) is not enough for minimum order.")
        
else:

    # 8. How many need to order
    user_qty = (input(f"How many need t order? (Enter press automatically take  {min_cases} ): ")).strip()
    if int(user_qty) < min_cases:
        raise Exception ("Quantity must be greter or equal to min_cases")
    else:
        order_cases = int(user_qty)
        total_amount = order_cases * case_price
        total_pieces = order_cases * per_case_quantity
        print(f"Selected: {order_cases} cases | Total Amount: Rs {total_amount} | Total Pieces: {total_pieces}")

if order_cases <=0:
    raise Exception("Not allowed this quantity minimum 1")
elif int(total_pieces) > available_Stock:
    raise Exception("Item is Out of Stock")
elif total_amount < 2000:
    raise Exception("Not allowed below 2000 amount")
else:

    input_quantity = wait.until(EC.presence_of_element_located((By.NAME, "qty")))
    input_quantity.send_keys(Keys.BACKSPACE)
    input_quantity.send_keys(order_cases)
    time.sleep(2)

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add to cart']"))).click()

## Proceed to Checout
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/c/nilesh-7cb355/checkout')]"))).click()
wait.until(EC.visibility_of_element_located((By.XPATH,"//input[contains(@name,'date')]"))).send_keys("11/27/2026")
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "secondary"))).click()

# Slot Availability

print("\nAvailable Slots:")
print("1. 08:00-11:00")
print("2. 11:00-14:00")
print("3. 14:00-17:00")
print("4. 17:00-20:00")

choice = input("Which slot required? Enter Number (1/2/3/4): ")
slots = driver.find_elements(By.XPATH, "//input[@type='radio']")
if choice == "1":
    slots[0].click()
    print("Slot choosen : 08:00-11:00")
elif choice == "2":
    slots[1].click()
    print("Slot choosen : 11:00-14:00")
elif choice == "3":
    slots[2].click()
    print("Slot choosen : 14:00-17:00")
elif choice == "4":
    slots[3].click()
    print("Slot choosen : 17:00-20:00")

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Place order']"))).click()
time.sleep(1)

order_cell = wait.until(EC.visibility_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[1]")))
order_number = order_cell.text.strip()
print("Your Order Number is: ", order_number)

# Log out from buyer account
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log out']"))).click()

# Login from seller account to accept-ship-delivery yhe order
print("Login from Seller Account to Verify order")
valid_seller_username = ["seller1", "seller2", "seller3"]
username = input("Enter username (buyer1/buyer2/buyer3/seller1/seller2/seller3): ").strip()
if username not in valid_seller_username:
    raise Exception("Invalid seller username")
wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Test@123")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']"))).click()

# Print Page title for confirmation
print("Login successful! Page title:", driver.title)

# 7. Accept ,Ship & Delivery Order

wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Accept'])[1]"))).click()
print("Order Accepted!")
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Ship'])[1]"))).click()
print("Order Shipped!")
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Deliver'])[1]"))).click()
print("Order Delivered!")
time.sleep(1)
## Logout from seller and again login to buyer for invoice
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log out']"))).click()

# Login for buyer agian
print("Login for buyer again to check invoice")
valid_buyer_username = ["buyer1", "buyer2", "buyer3"]
username = input("Enter username (buyer1/buyer2/buyer3/seller1/seller2/seller3): ").strip()
if username not in valid_buyer_username:
    raise Exception("Invalid username ,Please enter valid username")
wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Test@123")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']"))).click()

# Click on invoices to check latest invoice

wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Invoices']"))).click()
time.sleep(1)
# click view to open invoice
wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[1]/td[5]"))).click()
invoice_text = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).text
print("GENERATED INVOICE DATA::")

# Check 1: Does exact Order Number showing in invoice
if order_number in invoice_text:
    print(f"Order Number matched on invoice: {order_number}")
else:
    print(f"Order Number {order_number} not found on invoice!")

input("To Close Browser Press Enter...")
driver.quit()





