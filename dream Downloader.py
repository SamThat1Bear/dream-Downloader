import os
import os.path
from datetime import datetime
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import tkinter as tk
from tkinter import ttk
import webbrowser

#UI Config
root = tk.Tk() 
root.title("dream Downloader")
top_menu = tk.Menu()
root.config(menu=top_menu)
root.geometry("300x200")

#Variables
styles = ["Pandora", "Daydream", "Toasty", "Bad Trip", "Rose Gold", "Mystical", "Dark Fantasy", "Psychic", "Steampunk", "Vibrant"]
download_type = tk.IntVar()
user = os.getlogin()
download_path = f"C:/Users/{user}/Desktop/Custom WomboAi/Generated Images"

#Functions
def look_for(element_xpath, driver):
    try:
        driver.find_element(By.XPATH, element_xpath)
    except NoSuchElementException:
        return False
    return True

def open_github():
    webbrowser.open("https://github.com/SamThat1Bear")

def default_settings():
    propmt_input.delete(0, tk.END)
    propmt_input.insert(tk.INSERT, "Car")
    num_img_input.delete(0, tk.END)
    num_img_input.insert(tk.INSERT, 1)
    style_input.set(value="Pandora")
    download_type.set(value=0)

def new_settings():
    propmt_input.delete(0, tk.END)
    num_img_input.delete(0, tk.END)
    num_img_input.insert(tk.INSERT, 1)
    style_input.set(value="")
    download_type.set(value=0)  

def generate_button():
    if (not propmt_input.get() == "") and (not int(num_img_input.get()) < 1) and (not int(num_img_input.get()) > 250) and ((style_input.get() in styles) or (style_input.get().isnumeric())):
        threading.Thread(target=generate_images, args=(num_img_input.get(), propmt_input.get(), style_input.get(), download_type.get(),)).start()
        style_input.configure(state= "disabled")
        num_img_input.configure(state= "disabled")
        propmt_input.configure(state= "disabled")
        download_type_both.configure(state= "disabled")
        download_type_card.configure(state= "disabled")
        download_type_image.configure(state= "disabled")
        generate_button_input.configure(state="disabled")

def generate_images(images_count, prompt_to_generate, style, download_type):
    global root
    global message
    message.configure(text=f"0/{images_count} prompts generated.")
    for i in range(int(images_count)):
        message.configure(text=f"{i}/{images_count} prompts generated.|Setting up drivers...")
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": rf"C:\Users\{user}\Desktop\Custom WomboAi\Generated Images", "profile.default_content_setting_values.automatic_downloads": 1}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        actions = ActionChains(driver)
        driver.get("https://dream.ai/create")
        assert "Dream by WOMBO" in driver.title

        message.configure(text=f"{i}/{images_count} prompts generated.|Inputting prompt.")
        prompt = driver.find_element(By.XPATH, "//*[@id=\"blur-overlay\"]/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/input")
        prompt.send_keys(prompt_to_generate)

        for j in range(1, 58):
            message.configure(text=f"{i}/{images_count} prompts generated.|Finding: style ({j}/57)")
            try:
                style_button_label = driver.find_element(By.XPATH, f"//*[@id=\"blur-overlay\"]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[{j}]/div[2]/div").get_attribute("textContent")
            except NoSuchElementException:
                continue
            if style_button_label == style or str(j) == style:
                style_button_label = j
                break
        message.configure(text=f"{i}/{images_count} prompts generated.|Finding STYLE BUTTON")
        style_button = driver.find_element(By.XPATH, f"//*[@id=\"blur-overlay\"]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[{style_button_label}]/div[1]/div/div/img")
        actions.move_to_element(style_button)
        style_button.click()

        message.configure(text=f"{i}/{images_count} prompts generated.|Finding GENERATE BUTTON")
        generate_button = driver.find_element(By.XPATH, "//*[@id=\"blur-overlay\"]/div/div/div[1]/div[2]/button")
        generate_button.click()

        while not look_for("//*[@id=\"blur-overlay\"]/div/div/div[2]/div[2]/div/button[2]", driver):
            message.configure(text=f"{i}/{images_count} prompts generated.|Finding: FINALIZE BUTTON")
            if driver.find_element(By.XPATH, "//*[@id=\"blur-overlay\"]/div/div/div[1]/div[2]/button").is_enabled():
                if not look_for("//*[@id=\"blur-overlay\"]/div/div/div[2]/div[2]/div/button[2]", driver):
                    message.configure(text="An Error occured while generating image. Trying again...")
                    driver.find_element(By.XPATH, "//*[@id=\"blur-overlay\"]/div/div/div[1]/div[2]/button").click()
        finalize_button = driver.find_element(By.XPATH, "//*[@id=\"blur-overlay\"]/div/div/div[2]/div[2]/div/button[2]")
        finalize_button.click()

        while not look_for("//*[@id=\"blur-overlay\"]/div/div/div[1]/div[2]/div[1]/div[3]/div[2]/div/div[2]", driver):
            message.configure(text=f"{i}/{images_count} prompts generated.|Finding: TOGGLE BUTTON")
        toggle_button = driver.find_element(By.XPATH, "//*[@id=\"blur-overlay\"]/div/div/div[1]/div[2]/div[1]/div[3]/div[2]/div/div[2]")
        toggle_button.click()

        while not look_for("//*[@id=\"blur-overlay\"]/div/div/div[2]/div/div/div/div/div[2]/button/div/div", driver):
            message.configure(text=f"{i}/{images_count} prompts generated.|Finding: DOWNLOAD BUTTON")
        download_button = driver.find_element(By.XPATH, "//*[@id=\"blur-overlay\"]/div/div/div[2]/div/div/div/div/div[2]/button/div/div")
        download_button.click()

        current_date = datetime.now()
        current_date = datetime.strftime(current_date,"%Y-%m-%d")

        match download_type:
            case 0:
                while not look_for("//*[@id=\"__next\"]/div/div[2]/div/div/div[2]/div/div/div[1]/button/div[2]", driver):
                    message.configure(text=f"{i}/{images_count} prompts generated.|Finding: FINAL DOWNLOAD BUTTON")
                finalize_download_button_trading = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div/div[2]/div/div/div[2]/div/div/div[1]/button/div[2]")
                finalize_download_button_trading.click()
                while not os.path.exists(download_path + "/Dream_TradingCard.jpg"):
                    message.configure(text=f"{i}/{images_count} prompts generated.|Downloading File.")
                message.configure(text=f"{i+1}/{images_count} prompts generated.|Formatting Files...")
                os.rename(download_path + "/Dream_TradingCard.jpg", f"{download_path}/{current_date} {prompt_to_generate} {style_input.get()} {i} TradingCard.jpg")
            case 1:
                while not look_for("//*[@id=\"__next\"]/div/div[2]/div/div/div[2]/div/div/div[2]/button/div[2]", driver):
                    message.configure(text=f"{i}/{images_count} prompts generated.|Finding: FINAL DOWNLOAD BUTTON")
                finalize_download_button_image = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div/div[2]/div/div/div[2]/div/div/div[2]/button/div[2]")
                finalize_download_button_image.click()
                while not os.path.exists(download_path + "/Dream_Background.jpg"):
                    message.configure(text=f"{i}/{images_count} prompts generated.|Downloading File.")
                message.configure(text=f"{i+1}/{images_count} prompts generated.|Formatting Files...")
                os.rename(download_path + "/Dream_Background.jpg", f"{download_path}/{current_date} {prompt_to_generate} {style_input.get()} {i} Image.jpg")
            case 2:
                while not look_for("//*[@id=\"__next\"]/div/div[2]/div/div/div[2]/div/div/div[1]/button/div[2]", driver):
                    message.configure(text=f"{i}/{images_count} prompts generated.|Finding: FINAL DOWNLOAD BUTTONS")
                finalize_download_button_trading = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div/div[2]/div/div/div[2]/div/div/div[1]/button/div[2]")
                finalize_download_button_trading.click()
                finalize_download_button_image = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div/div[2]/div/div/div[2]/div/div/div[2]/button/div[2]")
                finalize_download_button_image.click()
                while not (os.path.exists(download_path + "/Dream_TradingCard.jpg")) or not (os.path.exists(download_path + "/Dream_Background.jpg")):
                    message.configure(text=f"{i}/{images_count} prompts generated.|Downloading Files.")
                message.configure(text=f"{i+1}/{images_count} prompts generated.|Formatting Files...")
                os.rename(download_path + "/Dream_TradingCard.jpg", f"{download_path}/{current_date} {prompt_to_generate} {style_input.get()} {i} TradingCard.jpg")
                os.rename(download_path + "/Dream_Background.jpg", f"{download_path}/{current_date} {prompt_to_generate} {style_input.get()} {i} Image.jpg")

        driver.close()

        message.configure(text=f"{i+1}/{images_count} prompts generated.|Images generated successfully.")
    
    style_input.configure(state="enabled")
    propmt_input.configure(state="normal")
    style_input.configure(state="enabled")
    num_img_input.configure(state="normal")
    download_type_image.configure(state="normal")
    download_type_card.configure(state="normal")
    download_type_both.configure(state="normal")
    generate_button_input.configure(state="normal")

#Menus
about_menu = tk.Menu(top_menu, tearoff=False)
file_menu = tk.Menu(top_menu, tearoff=False)
top_menu.add_cascade(label="File", menu=file_menu)
top_menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="GitHub", command=open_github)
file_menu.add_command(label="New", command=new_settings)
file_menu.add_command(label="Save")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Default", command=default_settings)


#User Interface
prompt_text = tk.Label(text="Prompt to use for Generating:")
prompt_text.grid(column=0, row=0)

propmt_input = tk.Entry()
propmt_input.grid(column=1, row=0)

num_img_text = tk.Label(text="Images to Generate:")
num_img_text.grid(column=0, row=1)

num_img_input = tk.Spinbox(from_=1, to = 250, width=18)
num_img_input.grid(column=1, row=1)

style_text = tk.Label(text="Style to use:")
style_text.grid(column=0, row= 2)

style_input = ttk.Combobox(values=styles, width=17)
style_input.grid(column=1, row=2)

download_type_text = tk.Label(text="Image Download Type:")
download_type_text.grid(column=0, row=4)

download_type_card = tk.Radiobutton(text="Trading Card Only", value=0, variable=download_type)
download_type_image = tk.Radiobutton(text="Image Only", value = 1, variable=download_type)
download_type_both = tk.Radiobutton(text="Both", value = 2, variable=download_type)
download_type_card.grid(column=1, row=3, sticky=tk.W)
download_type_image.grid(column=1, row=4, sticky=tk.W)
download_type_both.grid(column=1, row=5, sticky=tk.W)

generate_button_input = tk.Button(text="Generate", command=generate_button)
generate_button_input.grid(column=0, row=8, columnspan=2)

message = tk.Message(text="Debug Messages are shown here", width= 300)
message.grid(column=0, row=9, columnspan=2, sticky=tk.N)

root.mainloop()
