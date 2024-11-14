#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 10:53:39 2024

@author: jonander
"""

from selenium import webdriver
# import sys

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Specify the path to the GeckoDriver executable
# sys.path.insert(0,'/usr/local/bin/geckodriver')

wd = webdriver.Firefox(options=options)
wd.quit()