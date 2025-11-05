from seleniumbase import SB
from datetime import date
import os
import requests


MY_USERNAME = os.environ.get("TP_USERNAME") 
MY_PASSWORD = os.environ.get("TP_PASSWORD")
PANTRY_ID = os.environ.get("PANTRY_ID")

with SB(uc=True, demo=True) as sb:  # demo=True if GUI needed
    url = "https://service.taipower.com.tw/ebpps2/login"
    sb.uc_open_with_reconnect(url, 4)  # UC mode
    sb.uc_gui_click_captcha()  # error in headless mode

    sb.sleep(5)
    sb.save_screenshot("c1.png")
    sb.assert_element('label[for="username"]', timeout=15)
    sb.type('#username', MY_USERNAME)
    sb.assert_element('label[for="password"]', timeout=15)
    sb.type('#password', MY_PASSWORD)
    sb.sleep(15)
    sb.uc_gui_click_captcha()  # error in headless mode
    sb.save_screenshot("c2.png")
    sb.click('button:contains("登入")', timeout=15)
    print("Login Successful")
    
    sb.sleep(15)
    sb.save_screenshot("c3.png")
    key = sb.get_attribute('input[value="智慧電表(AMI)專區"]', "onclick", timeout=15)
    key = key[key.rindex("/")+1:-2]

    # Error handling
    # try:
    #     key = sb.get_attribute('input[value="智慧電表(AMI)專區"]', "onclick", timeout=15)
    # except Exception as e:
    #     print("Login Failed")
    #     sb.save_screenshot("error_screenshot.png")
    #     raise e

    # KEY
    print(key)
    
    today = date.today()
    sb.open(f"https://service.taipower.com.tw/ebpps2/amichart/api/fifteenlist?enkey={key}&day={today}")  
    raw_cookie_json = sb.get_cookies()
    # sb.save_cookies(name="cookies.txt")  # another option is to save raw cookies to a .txt file

    cookie_header_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in raw_cookie_json])
    # COOKIE
    print(cookie_header_string)

    data = {
    'key': key,
    'cookie': cookie_header_string
    }

    r = requests.put(f'https://getpantry.cloud/apiv1/pantry/{os.environ.get('PANTRY_ID')}/basket/update_key', json=data)

    # UPDATE STATUS
    print(r.status_code)