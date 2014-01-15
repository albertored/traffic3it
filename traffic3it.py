#!/usr/bin/env python

import sys
import gtk
import appindicator

import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException as TOE
from selenium.common.exceptions import NoSuchElementException as NSEE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display

from time import gmtime, strftime

import NetworkManager

INTERVAL = 10 # minutes between interrogations
SSID = "YOUR_SSID" # ssid network tre
DIR = os.getcwd()
DIR = os.path.abspath(__file__).replace("traffic3it.py","")

class AppIndicatorExample:
	def __init__(self):
		self.ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appindicator.STATUS_ACTIVE)
		self.ind.set_attention_icon(DIR + "/tre-italia.png")
		self.ind.set_icon(DIR + "/tre-italia.png")
		
		self.menu = gtk.Menu()
		
		self.date1 = gtk.MenuItem("Last correct " + strftime("%H:%M:%S", gmtime()))
		self.date1.show()
		self.menu.append(self.date1)
		
		self.date2 = gtk.MenuItem("Last wrong " + strftime("%H:%M:%S", gmtime()))
		self.date2.show()
		self.menu.append(self.date2)
		
		image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		image.connect("activate", self.quit)
		image.show()
		self.menu.append(image)
		
		self.menu.show()

		self.ind.set_menu(self.menu)
		
		self.label = "1GB"
		self.ind.set_label(self.label)

	def quit(self, widget, data=None):
		gtk.main_quit()
		
	def update_label(self):
		self.display = Display(visible=0, size=(800, 600))
		self.display.start()
		self.driver = webdriver.Chrome(DIR + '/chromedriver')
		self.driver.get('http://internet.tre.it')
		try:
			self.element = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.ID, "remaining_credit")))
			self.traffico = self.driver.find_element_by_css_selector(".piano")	
			self.label=self.traffico.text
			self.date1.set_label("Last correct" + strftime("%H:%M:%S", gmtime()))
		except TOE, NSEE:
			self.date2.set_label("Last wrong" + strftime("%H:%M:%S", gmtime()))
		finally:
			self.driver.quit()
			self.display.stop()
		self.ind.set_label(self.label)
		return True

	def main(self):
		self.update_label()
		gtk.timeout_add(INTERVAL * 60 * 1000, self.update_label)   
		gtk.main()
		
def get_ssid():
	conn = NetworkManager.NetworkManager.ActiveConnections[0]
	settings = conn.Connection.GetSettings()
	return settings['connection']['id']
	
if __name__ == "__main__": 
	if get_ssid() == SSID:
		indicator = AppIndicatorExample()
		indicator.main()


