# Created by Yassine Hammadi at 9:46 p.m. 2023-02-07

import requests
import os.path
from bs4 import BeautifulSoup


#Get URL for each parsticipant
def url_num(number):
    return ("http://stimmdb.coli.uni-saarland.de/details.php4?SprecherID=" + str(number))


url = 'http://stimmdb.coli.uni-saarland.de'

session = requests.Session()

res = session.post(url, data={'sb_search': 'Datenbankanfrage', 'sb_lang': 'English'})

res = session.post(url, data={'sb_sent': 'Accept', 'n': '1'})

def download_dataset():
# 2741 is the ID numbre of the last participant.

    for i in range(0, 2742):
        session = requests.Session()
        session.post(url, data={'sb_search': 'Datenbankanfrage', 'sb_lang': 'English'})
        session.post(url, data={'sb_sent': 'Accept'})

        #Check the connection status
        print(res.status_code)
        response = session.get(url_num(i))

        soup = BeautifulSoup(response.text, 'html.parser')

        for gender in soup.find('div', attrs={'class', 'title'}):
            if(gender.find('female')!=-1):
                gend = "female"
            else:
                gend = "male"

        print('ID   :', i, "Gender", gend)
        for group in soup.findAll('table', attrs={'class', 'sessiondetails'}):
            for t in group.findAll('td', {'class': 'detailstd', 'colspan': '2'}):

                if t.text.find('healthy') == 0:
                    for link in group.findAll('a', attrs={'target': 'PLAY'}):
                        file_link = "http://stimmdb.coli.uni-saarland.de/" + link.get('href')
                        file_name = str(i)+"_"+ file_link[54:]
                        path = "dataset/healthy/" + gend
                        print("ID  :" , i, "File Link  : ", file_link)

                        file_path = os.path.join(path, file_name + ".wav")
                        doc = requests.get(file_link)
                        with open(file_path, 'wb') as f:
                            f.write(doc.content)

                    break

                if t.text.find('pathological') == 0:
                    for link in group.findAll('a', attrs={'target': 'PLAY'}):
                        file_link = "http://stimmdb.coli.uni-saarland.de/" + link.get('href')
                        file_name = str(i)+"_"+ file_link[54:]
                        path = "dataset/pathological/"+gend
                        print("ID  :" , i, "File Link  : ", file_link)

                        file_path = os.path.join(path, file_name+".wav")
                        doc = requests.get(file_link)
                        with open(file_path, 'wb') as f:
                            f.write(doc.content)
                break
            print("Data User "+str(i) +" is Saved")

download_dataset()