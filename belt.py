import pandas as pd
import numpy as np
import csv
from beltfuncs import *



# load data with first row as field names
engleague = pd.read_csv('data/england.csv')
engfacup = pd.read_csv('data/facup.csv')
engleaguecup = pd.read_csv('data/leaguecup.csv')
champos = pd.read_csv('data/champs.csv')
germany = pd.read_csv('data/germany.csv')
spain = pd.read_csv('data/spain.csv')
italy = pd.read_csv('data/italy.csv')
turkey = pd.read_csv('data/turkey.csv')
soviet1975 = pd.read_csv('data/soviet1975.csv')
sovietcup1975 = pd.read_csv('data/sovietcup1975.csv')


#convert engleague date to date format
engleague['Date'] = pd.to_datetime(engleague['Date']).dt.date
#add countrycode
engleague['countrycode'] = 'EN'

sovietcup1975['Date'] = pd.to_datetime(sovietcup1975['Date']).dt.date
sovietcup1975['totgoal'] = sovietcup1975['hgoal'] + sovietcup1975['vgoal']
sovietcup1975['goaldif'] = sovietcup1975['hgoal'] - sovietcup1975['vgoal']
sovietcup1975['countrycode'] = 'SU'

soviet1975['Date'] = pd.to_datetime(soviet1975['Date']).dt.date
soviet1975['totgoal'] = soviet1975['hgoal'] + soviet1975['vgoal']
soviet1975['goaldif'] = soviet1975['hgoal'] - soviet1975['vgoal']
soviet1975['result'] = soviet1975.apply(lambda x: "H" if x['hgoal'] > x['vgoal'] else "A" if x['hgoal'] < x['vgoal'] else "D", axis=1)
sovietcup1975['countrycode'] = 'SU'

#convert spanish league date to date format
spain['Date'] = pd.to_datetime(spain['Date']).dt.date
#create new fields
spain['totgoal'] = spain['hgoal'] + spain['vgoal']
spain['goaldif'] = spain['hgoal'] - spain['vgoal']
spain['result'] = spain.apply(lambda x: "H" if x['hgoal'] > x['vgoal'] else "A" if x['hgoal'] < x['vgoal'] else "D", axis=1)
spain['countrycode'] = 'ES'

#convert italian league date to date format
italy['Date'] = pd.to_datetime(italy['Date']).dt.date
#create new fields
italy['totgoal'] = italy['hgoal'] + italy['vgoal']
italy['goaldif'] = italy['hgoal'] - italy['vgoal']
italy['result'] = italy.apply(lambda x: "H" if x['hgoal'] > x['vgoal'] else "A" if x['hgoal'] < x['vgoal'] else "D", axis=1)
italy['countrycode'] = 'IT'

#convert turkish league date to date format
turkey['Date'] = pd.to_datetime(turkey['Date']).dt.date
turkey['countrycode'] = 'TR'

#convert german league date to date format
germany['Date'] = pd.to_datetime(germany['Date']).dt.date
#create new fields
germany['totgoal'] = germany['hgoal'] + germany['vgoal']
germany['goaldif'] = germany['hgoal'] - germany['vgoal']
germany['result'] = germany.apply(lambda x: "H" if x['hgoal'] > x['vgoal'] else "A" if x['hgoal'] < x['vgoal'] else "D", axis=1)
germany['countrycode'] = 'DE'

#remove fa cup games with no date
engfacup = engfacup[engfacup['Date'].notna()]
#convert engfacup date to date format
engfacup['Date'] = pd.to_datetime(engfacup['Date']).dt.date
#keep relevant fields
engfacup = engfacup[['Date','Season','home','visitor','FT','hgoal','vgoal']]
#create new fields
engfacup['division'] = 'FA'
engfacup['tier'] = 0
engfacup['totgoal'] = engfacup['hgoal'] + engfacup['vgoal']
engfacup['goaldif'] = engfacup['hgoal'] - engfacup['vgoal']
engfacup['result'] = engfacup.apply(lambda x: "H" if x['hgoal'] > x['vgoal'] else "A" if x['hgoal'] < x['vgoal'] else "D", axis=1)
engfacup['countrycode'] = 'EN'

#convert engleaguecup date to date format
engleaguecup['Date'] = pd.to_datetime(engleaguecup['Date']).dt.date
#keep relevant fields
engleaguecup = engleaguecup[['Date','Season','home','visitor','FT','hgoal','vgoal']]
#create new fields
engleaguecup['division'] = 'LC'
engleaguecup['tier'] = 0
engleaguecup['totgoal'] = engleaguecup['hgoal'] + engleaguecup['vgoal']
engleaguecup['goaldif'] = engleaguecup['hgoal'] - engleaguecup['vgoal']
engleaguecup['result'] = engleaguecup.apply(lambda x: "H" if x['hgoal'] > x['vgoal'] else "A" if x['hgoal'] < x['vgoal'] else "D", axis=1)
engleaguecup['countrycode'] = 'EN'

#convert champs date to date format
champos['Date'] = pd.to_datetime(champos['Date']).dt.date
#keep relevant fields
champos = champos[['Date','Season','home','visitor','FT','hgoal','vgoal']]
#create new fields
champos['division'] = 'CL'
champos['tier'] = 0
champos['totgoal'] = champos['hgoal'] + champos['vgoal']
champos['goaldif'] = champos['hgoal'] - champos['vgoal']
champos['result'] = champos.apply(lambda x: "H" if x['hgoal'] > x['vgoal'] else "A" if x['hgoal'] < x['vgoal'] else "D", axis=1)
#name conversions
#if the home team is called bayern munich, change to bayern munchen
champos['home'] = champos['home'].replace('Bayern Munich','Bayern Munchen')
champos['visitor'] = champos['visitor'].replace('Bayern Munich','Bayern Munchen')
champos['countrycode'] = 'EU'

#concatenate
master = pd.concat([engleague,engfacup,engleaguecup,champos,germany,spain,italy,turkey,soviet1975,sovietcup1975],ignore_index=True)

#sort and reindex master by date
master.sort_values('Date', inplace = True)
#reset index
master.reset_index(drop=True, inplace=True)

print(master.head(20))

#Determine Initial Champion
champion = "Wanderers"
reigns = []
clubs = {}
current_reign = Reign(master.iloc[5])

print(current_reign.champion)

for index,match in master.iterrows():
    if is_defense(champion,match):
        if defense(champion,match)[1] == 1:
            #handle end of reign
            current_reign.lost(match)
            #print(f"{current_reign.champion} lost the belt to {current_reign.lost_to} on {current_reign.end_date}.")
            reigns.append(current_reign)
            champion = defense(champion,match)[0]
            #print(f"{current_reign.champion} held the belt for {(current_reign.end_date - current_reign.start_date).days} days and defended it {current_reign.defenses} times.\n")    
            #update club stats
            if current_reign.champion in clubs:
                clubs[current_reign.champion].add_reign(current_reign)
            else:
                clubs[current_reign.champion] = Club(current_reign.champion)
                clubs[current_reign.champion].add_reign(current_reign)

            #init new reign
            current_reign = Reign(match)
        else:
            current_reign.defended()
    else:
        pass

reigns.append(current_reign)
print(f"{current_reign.champion} are the current holders having held the belt from {current_reign.start_date} and defended it {current_reign.defenses} times.")


