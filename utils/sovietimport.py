from bs4 import BeautifulSoup
import requests
from datetime import datetime

response = requests.get('https://www.rsssf.org/tabless/su75.html')

soup = BeautifulSoup(response.text, 'html.parser')

#print everything between "Supreme League" and "First League"
p_tag = soup.find('p')

lines = p_tag.text.split('\n')

entries = []

gamedate = ""

read = 0

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

    #convert date[4] from date string to date format
    game[3] = datetime.strptime(game[3], '%b %d %Y').date()


    #print(game)

played = {}

for i, game in enumerate(entries[:]):
    print(i, game)
    if game[0] not in played:
        played[game[0]] = 0
    if game[2] not in played:
        played[game[2]] = 0
    played[game[0]] += 1
    played[game[2]] += 1

print(played)



    


