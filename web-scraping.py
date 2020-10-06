#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Python Web Scraping


# In[2]:


from bs4 import BeautifulSoup
import urllib.request
import numpy as np


# In[3]:


base_url = 'http://www.acb.com/partido/estadisticas/id/'


# In[4]:


# 18128 - 18433


# In[5]:


base_url = 'http://www.acb.com/partido/estadisticas/id/'
num = 1
stage = 1

# all the matches during season 18-19
for e in range(18128, 18433):
    url = base_url + str(e)
    print(url)
    our_url = urllib.request.urlopen(url)
    soup = BeautifulSoup(our_url, 'html.parser')
    players = []
    headers = ['dorsal','nombre','minutos','puntos','t2','t2%','t3','t3%','t1','t1%','rebotes','defensivos+ofensivos','asist','robos','perdidas','contraataques','tapones_favor','tapones-contra',',mates','falta_favor','falta_contra','+/-','Valoracion']
    
    #find all visitant teams
    for i in soup.find_all('section', 'partido visitante'):
        rows = i.find_all('tr')
        team = i.find('h6')
        team = team.text.replace('&nbsp;', '').replace('\xa0', ' ')
        team = team.split(' ')
        team = team[0:2]
        
        # find all table rows of visitant team 
        for row in rows:
            data = row.find_all('td')
            player = []
            for d in data:
                player.append(d.text)
            players.append(player)
        players = players[2:len(players)-2]
        players = [headers] + players
        
        # 9 matches per stage so if num is higher than 9 we are in the next stage and then reestart the cycle
        if num > 9:
            num = 1
            stage += 1
            
        # save file with file name: teamName_stageNumber.csv
        file_name = team[0].lower() + '_' + team[1].lower() + '_' + str(stage) + '.csv'
        np.savetxt(file_name,  
           players, 
           delimiter =", ",  
           fmt ='% s') 
        num += 1

