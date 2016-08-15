#Paleo_DB_Rip.py
#Python script to programmatically web-scrape from paleobiodb.org
#Author: Matt Oakley
#Date: 08/15/2016

# Imports #
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import urllib2
import pycountry
import wget
import sys
import codecs

# Globals #
listed_dinos = ["Tyrannosaurus"]

def retrieve_webpage(dino_name):
	#Retrieve the HTML for the specific dinosaur and return the page in string format
	URL = "https://paleobiodb.org/data1.2/occs/list.txt?base_name=" + dino_name + "&show=loc"
	page = urllib2.urlopen(URL)
	page_str = str(BeautifulSoup(page, "lxml")).splitlines()
	return page_str

def extract_webpage_header(web_page):
	#Extract the header from the list
	header = web_page[0]
	header_elements = header.split("\"")

	#Get rid of delimeter elements (commas)
	header_elements[:] = [x for x in header_elements if x != ","]
	return header_elements

def construct_location_string(county, state, cc):
	#Convert country-code to full-name of country
	country = pycountry.countries.get(alpha2 = cc)
	country = str(country.name)

	#Construct location string usable by geopy
	if county != "":
		location = county + ", " + state + ", " + country
		return location
	else:
		location = state + ", " + country
		return location

def construct_GPS_coords(location):
	#Construct the lat/lon of different locations
	geolocator = Nominatim()
	coords = geolocator.geocode(location)
	return (coords.latitude, coords.longitude)

def parse_locations(web_page):
	#Get the indexes of country code, state, and county
	header = extract_webpage_header(web_page)
	index_of_country = header.index("cc")
	index_of_state = header.index("state")
	index_of_county = header.index("county")

	#For all locations, get the lat/lon coordinates
	for i in range(1, len(web_page) - 1):
		entry = web_page[i].split("\"")
		entry[:] = [x for x in entry if x != ","]
		country = entry[index_of_country]
		state = entry[index_of_state]
		county = entry[index_of_county]
		location = construct_location_string(county, state, country)
		coords = construct_GPS_coords(location)


		


for i in range(0, len(listed_dinos)):
	web_page = retrieve_webpage(listed_dinos[i])
	locations = parse_locations(web_page)
