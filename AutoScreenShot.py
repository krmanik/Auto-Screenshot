# Project Name: Auto Screenshot
# Description: Take screenshot of screen when any change take place.
# Author: Mani (Infinyte7)
# Date: 26-10-2020
# License: MIT

from pyscreenshot import grab
from PIL import ImageChops

import os
import time
import subprocess, sys
from datetime import datetime

import tkinter as tk
from tkinter import *
from tkinter import font


class AutoScreenshot:
    def __init__(self, master):
        self.root = root
        
        root.title('Auto Screenshot')
        root.config(bg="white")

        fontRoboto = font.Font(family='Roboto', size=16, weight='bold')

        # project name label     
        projectTitleLabel = Label(root, text="Auto Screenshot v1.0.0")
        projectTitleLabel.config(font=fontRoboto, bg="white", fg="#5599ff")
        projectTitleLabel.pack(padx="10")

        # start button
        btn_start = Button(root, text="Start", command=self.start)
        btn_start.config(highlightthickness=0, bd=0, fg="white", bg="#5fd38d",
                         activebackground="#5fd38d", activeforeground="white", font=fontRoboto)
        btn_start.pack(padx="10", fill=BOTH)

        # close button
        btn_start = Button(root, text="Close", command=self.close)
        btn_start.config(highlightthickness=0, bd=0, fg="white", bg="#f44336",
                         activebackground="#ff7043", activeforeground="white", font=fontRoboto)
        btn_start.pack(padx="10", pady="10", fill=BOTH)
      
    def start(self):
        # Create folder to store images
        directory = "Screenshots"
        self.new_folder = directory + "/" + datetime.now().strftime("%Y_%m_%d-%I_%M_%p")

        # all images to one folder
        if not os.path.exists(directory):
            os.makedirs(directory)

        # new folder for storing images for current session
        if not os.path.exists(self.new_folder):
            os.makedirs(self.new_folder)

        # Run ScreenCords.py and get cordinates
        cords_point = subprocess.check_output([sys.executable, "GetScreenCoordinates.py", "-l"])
        cord_tuple = tuple(cords_point.decode("utf-8").rstrip().split(","))

        # cordinates for screenshots and compare
        self.cords = (int(cord_tuple[0]), int(cord_tuple[1]), int(cord_tuple[2]), int(cord_tuple[3]))

        # save first image
        img1 = grab(bbox=self.cords)
        now = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        fname = self.new_folder + "/ScreenShots" + now + ".png"
        img1.save(fname)
        print("First Screenshot taken")

        # start taking screenshot of next images
        self.take_screenshots()       

    def take_screenshots(self):
        # grab first and second image
        img1 = grab(bbox=self.cords)
        time.sleep(1)
        img2 = grab(bbox=self.cords)

        # check difference between images
        diff = ImageChops.difference(img1, img2)
        bbox = diff.getbbox()
        
        if bbox is not None:
            now = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            fname = self.new_folder + "/ScreenShots" + now + ".png"
            
            img2.save(fname)
            print("Screenshot taken")

        root.after(5, self.take_screenshots)

    def close(self):
        quit()

if __name__ == "__main__":  
    root = Tk()
    gui = AutoScreenshot(root)
    root.mainloop()
