import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

loadTime = 1
checkTime = 10
season_links = []
episode_links = []
move_list = []

def ChooseLocation():

    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    if len(Folder_Name) > 1:
        Debug.config(text="Click The Download Button",fg="green")
    else:
        Debug.config(text="Selecting Default Download Folder...",fg="white")
        Folder_Name = r"C:\Users\win\Downloads"
        time.sleep(1)
        Debug.config(text="Click The Download Button",fg="green")

def Move():

    try:
        if len(Folder_Name) > 1:
            Debug.config(text="Moving files...", fg="white")
            print("Moving files...")
            for file_name in move_list:
                try:
                    print("Moving: " + file_name)
                    shutil.move("C:/Users/win/Downloads/"+file_name, Folder_Name+"/"+file_name)
                except Exception as e:
                    print(e)
            Debug.config(text="Files Moved", fg="green")
            time.sleep(1)
            Debug.config(text="Enjoy!", fg="green")
            print("Downloaded " + str(len(move_list)) + " episodes.")
    except Exception as e:
        print(e)

def Download():

    if dropdown2.get() == "All seasons (i.e., The Complete Anime)":
        DownloadAnime()
    elif dropdown2.get() != "All seasons (i.e., The Complete Anime)":
        if dropdown3.get() == "All episodes (i.e., The Complete Season)":
            DownloadSeason(dropdown2.current(), True)
        elif dropdown3.get() == "Select Episode:":
            DownloadRange()
        else:
            DownloadEpisode(dropdown3.current(), True)
    else:
        Debug.config(text="Please check all dropdowns properly!", fg="red")

def DownloadAnime():
    
    print("Downloading: The complete anime.")
    for i in range(len(season_links)):
        Driver = webdriver.Edge() # Or whatever browser you have
        Driver.get(season_links[i])
        Driver.implicitly_wait(loadTime)
        episode_links.clear()
        all_links = Driver.find_elements(By.XPATH, "//a[@href]")
        links = [link for link in all_links if "https://episodes.animeflix" in link.get_attribute("href")]
        for link in links:
            episode_links.append(link.get_attribute("href"))
        if i == len(season_links) - 1:
            DownloadSeason(i, True)
            Driver.quit()
        else:
            DownloadSeason(i, False)

def DownloadSeason(season_index, close):

    print("Downloading: Season " + str(season_index+1))
    if season_index < len(season_links):
        for i in range(len(episode_links)):
            if i == len(episode_links) - 1:
                if close == True:
                    DownloadEpisode(i, True)
                else:
                    DownloadEpisode(i, False)
            else:
                DownloadEpisode(i, False)

def DownloadRange():
    first_value = int(range_entry.get().split("-")[0]) - 1 # Assuming that the user inputs first episode as 1 and not 0
    lower_limit = int(range_entry.get().split("-")[1]) - first_value - 1
    upper_limit = int(range_entry.get().split("-")[2]) - first_value
    
    i = lower_limit
    while i < upper_limit:
        if i == upper_limit-1:
            DownloadEpisode(i, True)
        else:
            DownloadEpisode(i, False)
        i+=1

def DownloadEpisode(episode_index, close):
    
    if episode_index < len(episode_links):
        episode_link = episode_links[episode_index]
        new_tab(driver, episode_link)

        all_links = driver.find_elements(By.XPATH, "//a[@href]")
        links = [link for link in all_links if "https://driveleech" in link.get_attribute("href")]
        link = links[0].get_attribute("href")
        new_tab(driver, link)

        all_links = driver.find_elements(By.XPATH, "//a[@href]")
        links = [link for link in all_links if "https://video" in link.get_attribute("href")]
        link = links[0].get_attribute("href")
        file_name = driver.find_element(By.CSS_SELECTOR, "#cf_captcha > div.card-body > div.mb-4 > ul > li:nth-child(1)")
        move_list.append(file_name.text.strip().replace("Name : ", ""))
        print("Downloading: " + file_name.text.strip().replace("Name : ", ""))
        new_tab(driver, link)

        button = driver.find_element(By.ID, "generate")
        action = ActionChains(driver)
        action.click(button).perform()
        close_ads(driver)
        action.click(button).perform()
        time.sleep(loadTime)
        keep_tab_open(close)

def Search():

    global links
    global driver
    global name
    name = name_entry.get()

    if len(name) > 0:
    
        Debug.config(text="Searching for anime...", fg="white")
        search_URL = "https://animeflix.pm/?s=" + name.replace(" ", "+")
        
        driver = webdriver.Edge() # Or whatever browser you have
        driver.get(search_URL)
        driver.implicitly_wait(loadTime)

        all_links = driver.find_elements(By.XPATH, "//a[@href]")
        links = [link for link in all_links if name.lower().replace(" ", "") in link.text.strip().lower().replace(" ", "")]

        if len(links) < 1:
            Debug.config(text="NO Anime series have been found!", fg="red")
        else:
            Debug.config(text="Select required anime from the dropdown",fg="white")

        link_list = []
        for link in links:
            link_list.append(link.text.strip())
        dropdown1['values'] = link_list
    
    else:
        Debug.config(text = "Please enter the name of the anime!", fg="red")

def on_anime_select(event):

    URL = ""
    selected = dropdown1.get()
    for link in links:
        if link.text.strip() == selected:
            URL = link.get_attribute("href")
            Debug.config(text="Anime Selected Successfully", fg="green")
    new_tab(driver, URL)
    
    Debug.config(text="Searching for seasons...", fg="white")

    all_seasons = driver.find_elements(By.TAG_NAME, "h3")
    seasons = [season for season in all_seasons if name.lower().replace(" ", "") in season.text.strip().lower().replace(" ", "")]
    seasons = [season for season in all_seasons if "480p" in season.text.strip() or "720p" in season.text.strip() or "1080p" in season.text.strip() or "||" in season.text.strip()]
    season_list = []
    for season in seasons:
        season_list.append(season.text.strip())
    season_list.append("All seasons (i.e., The Complete Anime)")
    dropdown2['values'] = season_list

    Debug.config(text="Select required season from the dropdown\n(Quality & Size are in the name)", fg="white")

def on_season_select(event):

    all_links = driver.find_elements(By.XPATH, "//a[@href]")
    links = [link for link in all_links if "https://episodes.animeflix" in link.get_attribute("href")]
    for link in links:
        season_links.append(link.get_attribute("href"))
    URL = links[dropdown2.current()].get_attribute("href")
    Debug.config(text="Season selected successfully", fg="green")
    new_tab(driver, URL)
    Debug.config(text="Searching for episodes...", fg="white")

    all_episodes = driver.find_elements(By.TAG_NAME, "h3")
    episodes = [episode for episode in all_episodes if "episode" in episode.text.strip().lower().replace(" ", "")]
    episode_list = []
    for episode in episodes:
        episode_list.append(episode.text.strip())
    episode_list.append("All episodes (i.e., The Complete Season)")
    dropdown3['values'] = episode_list
    Debug.config(text="Select required episode from the dropdown\nOR Enter first episode number and range of episodes seperated by -\nExample: 1-6-9 or 13-17-24 Here, both episodes are included", fg="white")
    
    all_links = driver.find_elements(By.XPATH, "//a[@href]")
    links = [link for link in all_links if "https://episodes.animeflix" in link.get_attribute("href")]
    for link in links:
        episode_links.append(link.get_attribute("href"))

def on_episode_select(event):

    Debug.config(text="Choose Download Folder if you want to move files else click Download", fg="white")

def close_ads(Driver):
    
    time.sleep(1)
    if len(Driver.window_handles) > 1:
        Driver.switch_to.window(Driver.window_handles[1]) 
        Driver.close()
        Driver.switch_to.window(Driver.window_handles[0])

def new_tab(Driver, URL):

    Driver.execute_script("window.open('');")
    Driver.switch_to.window(Driver.window_handles[1]) 
    Driver.get(URL)
    Driver.switch_to.window(Driver.window_handles[0])
    Driver.close()
    Driver.switch_to.window(Driver.window_handles[0])
    Driver.implicitly_wait(loadTime)

def keep_tab_open(close):
    Debug.config(text="Downloading...", fg="orange")
    while True:
        files_exist = any(file.endswith(".crdownload") for file in os.listdir(r"C:\Users\win\Downloads"))
        if files_exist == False:
            time.sleep(checkTime/2)
        else:
            break
    while True:
        files_exist = any(file.endswith(".crdownload") for file in os.listdir(r"C:\Users\win\Downloads"))
        if files_exist == True:
            time.sleep(checkTime/2)
        else:
            break
    Debug.config(text="Download Completed", fg="green")
    if close == True:
        driver.quit()
        if dropdown4.get=="Yes":
            Move()
        else:
            Debug.config(text="Enjoy!", fg="green")

def on_name_click(event):

    if name_entry.get() == "Name of Anime":
        name_entry.delete(0, tk.END)
        name_entry.config(fg='orange')

def on_range_click(event):

    if range_entry.get() == "Range of episodes (Check episodes dropdown)":
        range_entry.delete(0, tk.END)
        range_entry.config(fg='black')

# Create the main window
app = tk.Tk()
app.title("Anime Downloader")
app.configure(bg='black')

# Title
title_label = tk.Label(app, text="Anime Downloader", font=("Helvetica", 16), fg = "gold", bg = "black")
title_label.pack(pady=10)

# Input field
name_entry = tk.Entry(app, width=30, fg='orange', font=('Helvetica', 12))
name_entry.insert(0, "Name of Anime")
name_entry.bind('<FocusIn>', on_name_click)
name_entry.pack(pady=5)

# A Button
button1 = tk.Button(app, text="Search for Anime", fg = "blue", command=Search)
button1.pack(pady=5)

# Dropdowns
dropdown1 = ttk.Combobox(app, width = 40, values=[])
dropdown1.set("Select Anime:")
dropdown1.bind("<Key>", lambda e: "break")
dropdown1.bind("<<ComboboxSelected>>", on_anime_select)
dropdown1.pack(pady=5)

dropdown2 = ttk.Combobox(app, width=40, values=[])
dropdown2.set("Select Season:")
dropdown2.bind("<Key>", lambda e: "break")
dropdown2.bind("<<ComboboxSelected>>", on_season_select)
dropdown2.pack(pady=5)

dropdown3 = ttk.Combobox(app, values=[])
dropdown3.set("Select Episode:")
dropdown3.bind("<Key>", lambda e: "break")
dropdown3.bind("<<ComboboxSelected>>", on_episode_select)
dropdown3.pack(pady=5)

# Input field
range_entry = tk.Entry(app, width=39, fg='black', font=('Helvetica', 10))
range_entry.insert(0, "Range of episodes (Check episodes dropdown)")
range_entry.bind('<FocusIn>', on_range_click)
range_entry.pack(pady=5)

#Dropdown
dropdown4 = ttk.Combobox(app, width=45, values=["Yes","No"])
dropdown4.set("Move files after downloading? (ONLY for windows)")
dropdown4.bind("<Key>", lambda e: "break")
dropdown4.pack(pady=5)

# Buttons
button2 = tk.Button(app, text="Choose Location", fg = "blue", command=ChooseLocation)
button2.pack(pady=10)

button3 = tk.Button(app, text="Download", fg = "blue", command=Download)
button3.pack(pady=10)

# Debug text
Debug = tk.Label(app, text="Type in the name of Anime", font=("Helvetica", 10), bg = "black", fg = "white")
Debug.pack(pady=10)

# Run the application
app.mainloop()
