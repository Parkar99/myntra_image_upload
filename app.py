import os
import json
from time import sleep
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

# Read README for more information
import config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Update XPATH's if the UI changes... Does not support drastic changes to the UI of Myntra
UPLOAD_IMAGES_INPUT = '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div/button/input'
BRAND_INPUT = '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div/div[2]/div[2]/div/div/span[1]/div[2]/input'
VAN_INPUT = (
    '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div/div[3]/input'
)
COLOR_INPUT = (
    '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div/div[4]/input'
)
SUBMIT_BUTTON = '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div/div[5]/button'

COLOR_JSON_PATH = os.path.join(CURRENT_DIR, 'color_list.json')


def json_dump_colors(colors: list) -> None:
    ''' Helper function to dump list object to json and write to file '''
    with open(COLOR_JSON_PATH, 'w') as f:
        f.write(json.dumps(colors))


def json_load_colors() -> list:
    ''' Helper function to read from json file and return contents parsed in list '''
    if os.path.isfile(COLOR_JSON_PATH):
        with open(COLOR_JSON_PATH, 'r') as f:
            cl = f.read()
            return json.loads(cl)
    else:

        return []


options = webdriver.ChromeOptions()
# options.binary_location = '/usr/bin/brave-browser'
# chrome_driver_binary = '/home/nabeel/bin/chromedriver'

driver = webdriver.Chrome(chrome_driver_binary, options=options)
driver.delete_all_cookies()
driver.get('http://partners.myntrainfo.com/')
sleep(2)

# Login Button
driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div/div/a').click()
# Sign in with email button
driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/a').click()
# Email input
driver.find_element(
    By.XPATH, '/html/body/div/div[2]/div[2]/form/div[1]/input'
).send_keys(config.EMAIL)
# Password input
driver.find_element(
    By.XPATH, '/html/body/div/div[2]/div[2]/form/div[2]/input'
).send_keys(config.PASS)
# Log in button
driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div[3]/button').click()

driver.get('http://partners.myntrainfo.com/DiyCataloguing/ImageCapturing')
sleep(2)

upload_images_element = driver.find_element(By.XPATH, UPLOAD_IMAGES_INPUT)
brand_element = driver.find_element(By.XPATH, BRAND_INPUT)
van_element = driver.find_element(By.XPATH, VAN_INPUT)
color_input = driver.find_element(By.XPATH, COLOR_INPUT)
submit_button = driver.find_element(By.XPATH, SUBMIT_BUTTON)

CURRENT_WORKING_DIR = os.path.join(CURRENT_DIR, config.DIR)
all_skus = os.listdir(CURRENT_WORKING_DIR)
color_list = json_load_colors()

all_skus = list(
    filter(lambda d: os.path.isdir(os.path.join(CURRENT_WORKING_DIR, d)), all_skus)
)

for sku in all_skus:
    sku_dir = os.path.join(CURRENT_WORKING_DIR, sku)
    images_list = os.listdir(sku_dir)
    for img in images_list:
        img_path = os.path.join(sku_dir, img)
        upload_images_element.send_keys(img_path)
    brand_element.send_keys(f'{config.BRAND}\n')
    van_element.send_keys(sku)

    while True:
        print('n: New color')
        print('r: Remove color')
        for i, color in enumerate(color_list):
            print(f'{i + 1}: {color}')

        choice = input("Enter Choice: ")
        if choice == 'n':
            color_list.append(input("Enter Color: "))
            json_dump_colors(color_list)
        elif choice == 'r':
            for i, color in enumerate(color_list):
                print(f'{i + 1}: {color}')
            try:
                color_list.pop(int(input("Enter Color to Remove: ")) - 1)
                json_dump_colors(color_list)
            except:
                print('Try Again')
                continue
        else:
            try:
                color_choice = color_list[int(choice) - 1]
                color_input.send_keys(color_choice)
                break
            except:
                print('Try Again')
                continue

    submit_button.click()
    with open(os.path.join(CURRENT_DIR, 'progress.log'), 'a') as f:
        f.write(f'{CURRENT_WORKING_DIR}:{sku}\n')

    Path(os.path.join(f'{CURRENT_WORKING_DIR}_done', sku)).mkdir(
        parents=True, exist_ok=True
    )

    for img in images_list:
        img_path = os.path.join(sku_dir, img)

        os.rename(
            img_path, os.path.join(f'{CURRENT_WORKING_DIR}_done', sku, img),
        )
    os.rmdir(os.path.join(CURRENT_WORKING_DIR, sku))

    sleep(2)
