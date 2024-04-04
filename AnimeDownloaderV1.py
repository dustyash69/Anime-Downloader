import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def click_and_download_links(url):

    driver = webdriver.Edge()

    try:
        driver.get(url)
        links = driver.find_elements(By.XPATH, "//a")
        links = [link for link in links if link != links[0]]
        for link in links:
            link.click()
            while True:
                files_exist = any(file.endswith(".crdownload") for file in os.listdir(r"C:\Users\win\Downloads"))
                if files_exist:
                    time.sleep(5)
                else:
                    break

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        while True:
            files_exist = any(file.endswith(".crdownload") for file in os.listdir(r"C:\Users\win\Downloads"))
            if files_exist:
                time.sleep(5)
            else:
                break
        driver.quit()

if __name__ == "__main__":
    print("Type in an URL like: https://dl.animesp.xyz/Completed/Blend-S/720/ (A click on a link in the webpage should download an episode)")
    start_url = input()
    click_and_download_links(start_url)
