from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

response = requests.get('https://www.rsssf.org/tabless/su75.html')

soup = BeautifulSoup(response.text, 'html.parser')

#print everything between "Supreme League" and "First League"
p_tag = soup.find('p')

lines = p_tag.text.split('\n')

entries = []

gamedate = ""

read = 0

#import supreme league
for line in lines:
    if "Round 1" in line:
        read = 1
    if read == 0:
        continue
    if "Final Table:" in line:
        break
    elif "Jan " in line or "Feb " in line or "Mar " in line or "Apr " in line or "May " in line or "Jun " in line or "Jul " in line or "Aug " in line or "Sep " in line or "Oct " in line or "Nov " in line or "Dec " in line:
        gamedate = line.replace("[","").replace("]","") + "1975"
        #print(gamedate)
    elif "-" in line and "Ali-Zade" not in line:
        print(line)
        result = line.split()
        result.append(gamedate)
        entries.append(result)

cup_entries = []

read = 0

#import cup
for line in lines:
    if "Soviet Union Cup 1975" in line:
        read = 1
    if read == 0:
        continue
    elif "Jan " in line or "Feb " in line or "Mar " in line or "Apr " in line or "May " in line or "Jun " in line or "Jul " in line or "Aug " in line or "Sep " in line or "Oct " in line or "Nov " in line or "Dec " in line:
        gamedate = line.replace("[","").replace("]","") + "1975"
        #print(gamedate)
    elif "-" in line and "Ali-Zade" not in line:
        print(line)
        result = line.split()
        result.append(gamedate)
        cup_entries.append(result)


for game in entries[:]:
    #handle weird names
    if game[0] == "SKA":
        game[0] = "SKA R/D"
        game.pop(1)
    if game[1] == "Tb":
        game[0] = "Dinamo Tblisi"
        game.pop(1)
    if game[1] == "M":
        game[0] = "Dinamo Moskva"
        game.pop(1)
    if game[1] == "K":
        game[0] = "Dinamo Kiev"
        game.pop(1)
    if game[0] == "Ararat":
        game[0] = "FC Ararat"

    if game[2] == "SKA":
        game[2] = "SKA R/D"
        game.pop(3)
    if game[3] == "Tb":
        game[2] = "Dinamo Tblisi"
        game.pop(3)
    if game[3] == "M":
        game[2] = "Dinamo Moskva"
        game.pop(3)
    if game[3] == "K":
        game[2] = "Dinamo Kiev"
        game.pop(3)
    if game[2] == "Ararat":
        game[2] = "FC Ararat"

    #convert date[4] from date string to date format
    game[3] = pd.to_datetime(datetime.strptime(game[3], '%b %d %Y').date())

    #create home goals as first part of score variable
    game.append(int(game[1].split("-")[0]))
    game.append(int(game[1].split("-")[1]))


soviet1975 = pd.DataFrame(entries, columns=['home','FT','visitor','Date','hgoal','vgoal'])


soviet1975.to_csv('./data/soviet1975.csv',index=False)

for game in cup_entries:
    game[0] = game[0] + " " + game[1]
    game.pop(1)
    if game[2] == "Krylya":
        game[2] = game[2] + " " + game[3] + " " + game[4]
        game.pop(3)
        game.pop(4)
    else:
        game[2] = game[2] + " " + game[3]
        game.pop(3)
    game[3] = game[3].replace("Preliminary Round ","")
    if "Att:" not in game:
        print(game)

#small dset - sort out in google sheets
    
    

