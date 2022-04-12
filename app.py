import pickle
import os,sys,time,json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.kucoin.com/ucenter/signup"


for i in sys.argv:
    print(i)

if len(sys.argv) < 5:
    sys.exit("Usage: python3 app.py refer mail code cookies")


refer = str(sys.argv[1])
mail = str(sys.argv[2])
code = str(sys.argv[3])
cookies = str(sys.argv[4])
d_path = os.getcwd()+"/path"

# check folder existence

def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

make_folder(d_path)

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument('--headless')
op.add_argument('--no-sandbox')
op.add_argument('--disable-dev-shm-usage')
prefs = {'download.default_directory' : d_path}
op.add_experimental_option('prefs', prefs)

print("[+] Starting Chrome...")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=op)
# driver = webdriver.Chrome(chrome_options=op)


driver.set_window_size(1536 , 900)
print("[+] Chrome started")
driver.get(cookies)
print("[+] URL of Cookies loaded")


print("[+] Searching For Download Button...")
wait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//button[text()="Download File"]')))
print("[+] Download Button Found")
driver.find_element(By.XPATH,'//button[text()="Download File"]').click()
print("[+] Download Button Clicked")



time.sleep(20)
print("[+] Download Completed...")


print("[+] Loading Cookies...")
cookies = pickle.load(open(d_path+"/cookies.pkl", "rb"))
print("[+] Loading KuCoin Website")
driver.get(URL)
print("[+] KuCoin Website Loaded")

for cookie in cookies:
    driver.add_cookie(cookie)

print("[+] Cookies Loaded")

    
time.sleep(2)
print("[+] Refreshing Page")
driver.refresh()
print("[+] Page Refreshed")



print("[+] Searching For Email Label...")
wait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//div[text()="Email"]')))
driver.find_element(By.XPATH,'//div[text()="Email"]').click()
print("[+] Email Label Clicked...")


print("[+] Searching For Email Input...")
wait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//input[@placeholder="Email"]')))
print("[+] Email Input Found")


driver.find_element(By.XPATH,"//input[@placeholder='Email']").send_keys(mail)
print("[+] Email Input Filled")


driver.find_element(By.XPATH,'//label[text()="Email verification code"]/parent::div/div/input').send_keys(code)
print("[+] Email Verification Code Filled")

driver.find_element(By.XPATH,"//input[@type='password']").send_keys("Sanaur@#$123")
print("[+] Password Filled")

driver.find_element(By.XPATH,'//span[contains(text(),"Referral Code (Optional)")]/parent::div/following-sibling::div/div/input').send_keys(refer)
print("[+] Referral Code Filled")

driver.find_element(By.XPATH,'//span[text()="Sign Up"]/parent::button').click()
print("[+] Sign Up Button Clicked")

print("[+] Waiting For Sign Up  To Be Completed...")
try:
    wait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[contains(text(),"Success")]')))
    print("Success")
except:
    print("Failed")
