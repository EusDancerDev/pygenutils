#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 10:53:39 2024

@author: jonander
"""

from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Specify the path to the GeckoDriver executable
# gecko_driver_path = '/path/to/geckodriver'  # Update with the actual path to geckodriver

wd = webdriver.Firefox(options=options)
