
# coding: utf-8

# In[9]:


import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time


# In[2]:


csvPath = os.path.expanduser("~/Desktop")
df = pd.read_csv(f"{csvPath}/FreeAgents.csv", sep=";")


# In[3]:


# Initialize our output column with zeros. Then specify the categories of stats to loop over. Choose the extra weight for the most important columns.
df["FantasyPoints"] = np.zeros(len(df["RANK"]))
categories = ["MIN" , "PTS", "AST", "REB", "BLK", "STL", "TO", "FG%", "3PM", "FT%"]
ExtraWeight = 2

for categorie in categories:
    if categorie == "TO":
        i = 0
        tempStore = []
        df = df.sort_values(categorie, ascending=True)

        while i < len(df["RANK"]):
            tempStore.append(df.iloc[i,16]+ len(df["RANK"]) - i)
            i += 1

        df["FantasyPoints"] = tempStore
        tempStore.clear()   
    if categorie == "MIN":
        i = 0
        tempStore = []
        df = df.sort_values(categorie, ascending=False)

        while i < len(df["RANK"]):
            tempStore.append(df.iloc[i,16]+ ExtraWeight * len(df["RANK"]) - ExtraWeight * i)
            i += 1

        df["FantasyPoints"] = tempStore
        tempStore.clear()
    else:
        i = 0
        tempStore = []
        df = df.sort_values(categorie, ascending=False)

        while i < len(df["RANK"]):
            tempStore.append(df.iloc[i,16]+ len(df["RANK"]) - i)
            i += 1

        df["FantasyPoints"] = tempStore
        tempStore.clear()   

df = df.sort_values("FantasyPoints", ascending=False)


# In[7]:


tempStore = []
maxFantasyPoints = len(categories) * len(df["RANK"])

i = 0
while i <  len(df["RANK"]):
    tempStore.append(round(df.iloc[i,16] / maxFantasyPoints, 3))
    i += 1
    
df["FantasyPoints%"] = tempStore
df = df.sort_values("FantasyPoints", ascending=False)
tempStore.clear()


# In[12]:


height = 7
width = len(categories) * height
fig, axs = plt.subplots(ncols=len(categories), figsize= (width, height))
for index, categorie in enumerate(categories):
    sns.regplot(x=df[categorie], y=df["FantasyPoints"], ax=axs[index])
    


# In[8]:


df


# In[10]:


df.to_csv(path_or_buf=f"{csvPath}/FreeAgents_Output_{time.time()}.csv", sep=";")

