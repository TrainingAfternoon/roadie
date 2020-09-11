from bs4 import BeautifulSoup, SoupStrainer
import requests
import os.path

#Leylines: (0) last page_url

#Initialize leyline config opts
leyines = ["https://www.royalroad.com/fiction/11209/the-legend-of-randidly-ghosthound/chapter/127131/chapter-1"]

def load_nexus():
	global leylines
	nexus = open(".nexus.txt","r")
	
	#TODO  tune this up once nexus has def purpose
	leylines = nexus.readlines()
	
	nexus.close()

def serialize_nexus():
	nexus = open(".nexus.txt","w")
	for line in leylines:
		nexus.write(line)
	nexus.close()

def create_init_files():
	#bot info file creation
	init_file = open(".nexus.txt","w")
	init_file.write("https://www.royalroad.com/fiction/11209/the-legend-of-randidly-ghosthound/chapter/127131/chaper-1")
	init_file.close()

	book = open("book.html","a")
	book.write("<html><body>")#top part of the sandwich
	book.close()

def have_init_files():
	if (os.path.isfile("book.html") and os.path.isfile(".nexus.txt")):
		return True;
	return False;

def create_soup():
	page = requests.get(leylines[0]).text
	soup = BeautifulSoup(page, features="html.parser")
	soup.prettify()
	return soup;

def has_more_pages(soup):
	next_btn = soup.find("i",{"class": "far fa-chevron-double-right ml-3"}).parent
	
	if (next_btn.has_attr("href")):
		global leylines 
		leylines[0] = "https://www.royalroad.com" + next_btn["href"]
		return True;
	return False;

def scrape(soup,book):
	#returns list of strings containing text
	
	chapter_number = soup.find("h1",{"style": "margin-top: 10px"})
	chapter = soup.find("div",{"class": "chapter-inner chapter-content"})
	
	book.write(str(chapter_number))

	for child in chapter:
		#remove .string to get html <p>s\
			book.write(str(child))


def main():
	if (not have_init_files()):
		create_init_files()
	load_nexus()
	soup = create_soup()
	book = open("book.html","a")

	while(has_more_pages(soup)):
		scrape(soup,book)
		soup = create_soup()
	scrape(soup,book)#covers last case


	book.write("</body></html>")#close book tags
	book.close()
	
main()
