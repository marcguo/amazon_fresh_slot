from selenium import webdriver
# Allows headless runs.
from pyvirtualdisplay import Display
# Sweet credentials :)
import credentials
# For sending text mails using SMTP.
import smtplib

# Constants.
AVAILABLE_MESSAGE = 'Delivery slot available!'
UNAVAILABLE_MESSAGE = 'Delivery temporarily sold out'

def send_text(content):
    '''
    Sends a text mail to the user with a passed in message.

    @type  content string
    @param content Some text content to send to the user.
    '''

    # Establish a secure session with gmail's outgoing SMTP server.
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(credentials.TEXT_EMAIL, credentials.TEXT_PASSWORD)

    # Send a text message to myself.
    server.sendmail(credentials.TEXT_SENDER, credentials.TEXT_RECEIVER, content)

def get_slot_info():
    '''
    Gets the available slot status banner from the main page of the Amazon
    fresh website. You need to log in with your account in order to use this
    method. You can create a "credentials.py" file and set up your credentials
    there.

    @rtype  string
    @return The banner info string obtained from the Amazon Fresh main page.
    '''

    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = webdriver.Chrome()

    driver.get('https://fresh.amazon.com')
    sign_in_btn = driver.find_element_by_xpath('//*[@id="a-autoid-0-announce"]')
    sign_in_btn.click()
    email_in = driver.find_element_by_xpath('//*[@id="ap_email"]')
    email_in.send_keys(credentials.EMAIL)
    continue_btn = driver.find_element_by_xpath('//*[@id="continue"]')
    continue_btn.click()
    password_in = driver.find_element_by_xpath('//*[@id="ap_password"]')
    password_in.send_keys(credentials.PASSWORD)
    sign_in_btn_2 = driver.find_element_by_xpath('//*[@id="signInSubmit"]')
    sign_in_btn_2.click()

    banner_str = driver.find_element_by_xpath('//*[@id="a-page"]/div[2]/div/div[1]/div').text

    return banner_str

def form_result(slot_info):
    '''
    Forms the output message containing the available/unavailable information.

    @type  slot_info
    @param The banner slot info to parse.

    @rtype  string
    @return A message indicating whether slots are available or not.
    '''

    if UNAVAILABLE_MESSAGE in slot_info:
        message = UNAVAILABLE_MESSAGE
    else:
        message = AVAILABLE_MESSAGE
    
    print(message)

    print('The original message is: {}'.format(slot_info))

    return message

# Get the slot info from the Amazon Fresh site.
slot_info = get_slot_info()
# Parse the data obtained from the Amazon Fresh site.
result = form_result(slot_info)
# If there is an available slot, send the user a text message.
if result == AVAILABLE_MESSAGE:
    send_text(result)
    send_text(slot_info)
