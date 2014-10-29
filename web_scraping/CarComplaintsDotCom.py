from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import urllib.request as request
import re

def getMakes():
    """Function to get all the makes available at carcomplaints.com"""
    
    url = 'http://www.carcomplaints.com/'
    html = request.urlopen(url)
    
    soup = BeautifulSoup(html)
    sections = soup.find_all('section', id=re.compile('makes'))
    
    make_list = []
    for section in range(len(sections)):
        for li in sections[section].find_all('li'):
            make_list.append(li.get_text())
    
    return make_list


def getYearCounts(make, model):
    """Function that returns a Python dict that contains model years and their complaint qty"""
    
    url = 'http://www.carcomplaints.com/'+make+'/'+model+'/'
    html = request.urlopen(url)

    soup = BeautifulSoup(html)
    li = soup.find_all('li', id=re.compile('bar*'))

    year_counts_dict = {}
    for item in li:
        year_counts_dict[int(item.find('span',class_='label').get_text())]=int(item.find('span',class_='count').get_text().replace(",",""))
    
    return year_counts_dict


def getCountsByModel(make):
    """Method that returns the number of complaints for each model based on vehicle make
    Applicable make values are: 'Honda','Acura','Ford','GM',etc
    Method returns a dictionary where the key is the model, value is the qty of complaints"""
    
    url = 'http://www.carcomplaints.com/'
    url_make = url+make+'/'
    html_make = request.urlopen(url_make)
    
    soup = BeautifulSoup(html_make)
    ul = soup.find_all('ul', class_='column bar',id=re.compile('c*'))
    
    make_model_counts_dict = OrderedDict()
    num_column_data = len(ul)  # The data is divided up in arbitrary number of columns per HTML page source
    for i in range(num_column_data):  # For each column of data...
        for row in ul[i].find_all('li'):
            make_model_counts_dict[row.a.get_text()] = int(row.span.get_text().replace(",",""))
            
    return make_model_counts_dict


def getTopSystemsQty(make, model, year):
    """Function that returns an OrderedDict containing system problems and their complaint qty"""
    
    url = 'http://www.carcomplaints.com/'+make+'/'+model+'/'+str(year)+'/'
    html = request.urlopen(url)

    soup = BeautifulSoup(html)
    li = soup.find_all('li', id=re.compile('bar*'))
    
    problem_counts_dict = OrderedDict()  # We want to maintain insertion order
    for item in li:
        try:
            problem_counts_dict[item.a['href'][:-1]]=int(item.span.get_text().replace(",",""))
        except:
            pass
        
    return problem_counts_dict


def getNhtsaSystemsQty(make, model, year):
    """Function that returns an OrderedDict containing qty of NHTSA complaints by system"""
    
    url = 'http://www.carcomplaints.com/'+make+'/'+model+'/'+str(year)+'/'
    html = request.urlopen(url)

    soup = BeautifulSoup(html)

    nhtsa = soup.find_all('em', class_='nhtsa')

    nhtsa_counts = []
    for item in nhtsa:
        try:
            # There are 3 string tokens separated by whitespace, i want the 3rd token which is the qty
            nhtsa_counts.append(int(item.span.get_text().split()[2]))
        except:
            # Unfortunately, some only have 2 tokens
            nhtsa_counts.append(int(item.span.get_text().split()[1]))

    systems = soup.find_all('li', id=re.compile('bar*'))

    systems_list = []
    for item in systems:
        systems_list.append(item.a['href'][:-1]) # Remove the ending forward slash

    nhtsa_systems_counts = list(zip(systems_list,nhtsa_counts))
    
    nhtsa_systems_qty_dict = OrderedDict()
    for item in nhtsa_systems_counts:
        nhtsa_systems_qty_dict[item[0]]=item[1]
    
    return nhtsa_systems_qty_dict


def getSubSystemsQty(make, model, year, system):
    """Function that will return an OrderedDict of # of complaints by sub-system"""
    
    url = 'http://www.carcomplaints.com/'+make+'/'+model+'/'+str(year)+'/'+system+'/'
    html = request.urlopen(url)
    soup = BeautifulSoup(html)

    li = soup.find_all('li', id=re.compile('bar*'))

    subsystem_counts_dict = OrderedDict()  # We want to maintain insertion order
    for item in li:
        subsystem_counts_dict[item.a['href'].split(".")[0]]=int(item.span.get_text().replace(",",""))
        
    return subsystem_counts_dict


def getReviews(make, model, year, system, subsystem):
    """Function that returns a list of all (maybe) customer reviews
    NOTE: If there are more than 50 reviews, then the reviews are spread out over multiple pages."""
    
    url = 'http://www.carcomplaints.com/'+make+'/'+model+'/'+str(year)+'/'+system+'/'+subsystem+'.shtml'
    html = request.urlopen(url)
    soup = BeautifulSoup(html)

    reviews = soup.find_all('div', itemprop="reviewBody")
    
    complaints = []
    for complaint in reviews:
        complaints.append(complaint.p.get_text())
    
    #####  Read the first page, now check if there are 2 or more pages  #####
    # Get the subtitle so we can then figure out if there are multiple pages
    page_count_text = soup.find('div', id="subtitle").span.get_text()

    # If 'Page 1 of' exists, then there must be more than one page to read...loop thru all available pages
    if 'Page 1' in page_count_text:
        # Get total number of pages
        num_pages = int(page_count_text.split()[3].replace(")",""))
        print("Page 1 of",num_pages,"parsed")
        for page in range(2,num_pages+1):
            url = 'http://www.carcomplaints.com/'+make+'/'+model+'/'+str(year)+'/'+system+'/'+subsystem+'-'+str(page)+'.shtml'
            html = request.urlopen(url)
            try:  # Thru testing, found page(s) that BeautifulSoup could not parse due to page having bad markup syntax
                soup = BeautifulSoup(html)
                reviews = soup.find_all('div', itemprop="reviewBody")
                for complaint in reviews:
                    complaints.append(complaint.p.get_text())
                print("Page",page,"of",num_pages,"parsed")
                time.sleep(5)  # Need to add delay to prevent Connection Refused error
            except:
                print("Page", page,"has severely bad markup!","No data from this page was parsed.")
                pass
        print("Retrieval of review text completed")
    else:
        print("There was only 1 page to parse.  Retrieval of review text completed.")
        
    return complaints
