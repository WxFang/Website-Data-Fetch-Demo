import xml.etree.cElementTree as ET
import urllib
from bs4 import BeautifulSoup
import json
import csv

def scrape():
    theurl = "https://www.corcoran.com/nyc/Search/Listings?SaleType=Rent&Page="
    count = 1
    page = 0
    lists = []
    # iterate each page until empty page
    while count > 0:
        thepage = urllib.urlopen(theurl + "%d" % page)
        soup = BeautifulSoup(thepage, "html.parser")
        # count listings on one page
        count = 0
        for listing in soup.findAll('span', {"class": "address"}):
            attrs = listing.find('a').attrs
            id = attrs['data-listingid']
            addr = attrs['title']
            lists.append([id, addr])
            count += 1
        page += 1
    return lists

def googleGeoAPI(lists):
    key = "AIzaSyA31wRTJJyB-BdcxXV3W92xAWzXmfldoX8"
    base = r"https://maps.googleapis.com/maps/api/geocode/json?"
    # add two columns for latitude and longitude
    result = [list + [0] + [0] for list in lists]
    count = 0
    for list in lists:
        addP = "address=" + list[1]
        addP = addP.replace(" ", "+")
        geoUrl = base + addP + "&key=" + key
        response = urllib.urlopen(geoUrl)
        jsonRaw = response.read()
        jsonData = json.loads(jsonRaw)
        if jsonData['status'] == 'OK':
            res = jsonData['results'][0]
            result[count][-2] = res['geometry']['location']['lat']
            result[count][-1] = res['geometry']['location']['lng']
        count += 1
    return result


def saveToCsv(result, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)

def main():
    lists = scrape()
    result = googleGeoAPI(lists)
    saveToCsv(result, 'location.csv')

if __name__ == "__main__":
    main()
