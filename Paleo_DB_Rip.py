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
import os.path
import codecs

# Globals #
listed_dinos = ["Tyrannosaurus", "Stegosaurus"]

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
	if coords == None:
		pass
	else:
		return (coords.latitude, coords.longitude)

def parse_locations(web_page):
	#Get the indexes of country code, state, and county
	header = extract_webpage_header(web_page)
	index_of_country = header.index("cc")
	index_of_state = header.index("state")
	index_of_county = header.index("county")
	coords_list = []

	#For all locations, get the lat/lon coordinates and output to list
	for i in range(1, len(web_page) - 1):
		entry = web_page[i].split("\"")
		entry[:] = [x for x in entry if x != ","]
		country = entry[index_of_country]
		state = entry[index_of_state]
		county = entry[index_of_county]
		location = construct_location_string(county, state, country)
		print location
		#Coords Format: (Lat, Lon)
		coords = construct_GPS_coords(location)
		coords_list.append(coords)

	return coords_list

def output_locations(locations, dino):
	filename = "dinosaur_locs/" + dino + ".txt"
	output_file = open(filename, "w")
	for i in range(0, len(locations)):
		location_str = str(locations[i])
		output_file.write(location_str + "\n")

def check_if_file_exists(dino):
	filename = "dinosaur_locs/" + dino + ".txt"
	if os.path.isfile(filename):
		return 1
	else:
		return 0

for i in range(0, len(listed_dinos)):
	file_bool = check_if_file_exists(listed_dinos[i])
	web_page = retrieve_webpage(listed_dinos[i])
	if file_bool == 0:
		locations = parse_locations(web_page)
		output_locations(locations, listed_dinos[i])
	else:
		print "kek"
		continue