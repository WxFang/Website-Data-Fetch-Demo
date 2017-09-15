import xml.etree.cElementTree as ET
import urllib2, StringIO
import json
import time
import csv

def loadXML():
    page = urllib2.urlopen(r'http://www.related.com/feeds/ZillowAvailabilities.xml')
    io_xml = StringIO.StringIO()
    io_xml.write(page.read())
    io_xml.seek(0)
    return io_xml

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    lists = []
    for list in root:
        addr = list[0][0].text
        city = list[0][2].text
        state = list[0][3].text
        zip = list[0][4].text
        lists.append([addr, city, state, zip])
    return lists

def googleGeoAPI(lists):
    key = "AIzaSyA31wRTJJyB-BdcxXV3W92xAWzXmfldoX8"
    base = r"https://maps.googleapis.com/maps/api/geocode/json?"
    result = [list + [0] + [0] for list in lists]
    count = 0
    for list in lists:
        addP = "address=" + list[0] + "+" + list[1] + "+" + list[2] + "+" + list[3]
        addP = addP.replace(" ", "+")
        geoUrl = base + addP + "&key=" + key
        response = urllib2.urlopen(geoUrl)
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
    xmlfile = loadXML()
    lists = parseXML(xmlfile)
    result = googleGeoAPI(lists)
    saveToCsv(result, 'location.csv')

if __name__ == "__main__":
    main()
