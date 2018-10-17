
# coding: utf-8

# In[20]:


import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[21]:


csvPath = os.path.expanduser("~/Desktop")
df = pd.read_csv(f"{csvPath}/NBA2017.csv", sep=";")


# In[22]:


df = df.drop(df.columns[[0, 2, 3]], axis=1)


# In[23]:


# Initialize our output column with zeros. Then specify the categories of stats to loop over. Choose the extra weight for the most important columns.
df["FantasyPoints"] = np.zeros(len(df["PLAYER"]))
categories = ["MIN" , "PTS", "AST", "REB", "BLK", "STL", "TOV", "FG%", "3PM", "FT%"]
ExtraWeight = 2

for categorie in categories:
    if categorie == "TOV":
        i = 0
        tempStore = []
        df = df.sort_values(categorie, ascending=True)

        while i < len(df["PLAYER"]):
            tempStore.append(df.iloc[i,27]+ len(df["PLAYER"]) - i)
            i += 1

        df["FantasyPoints"] = tempStore
        tempStore.clear()   
    if categorie == "MIN":
        i = 0
        tempStore = []
        df = df.sort_values(categorie, ascending=False)

        while i < len(df["PLAYER"]):
            tempStore.append(df.iloc[i,27]+ ExtraWeight * len(df["PLAYER"]) - ExtraWeight * i)
            i += 1

        df["FantasyPoints"] = tempStore
        tempStore.clear()
    else:
        i = 0
        tempStore = []
        df = df.sort_values(categorie, ascending=False)

        while i < len(df["PLAYER"]):
            tempStore.append(df.iloc[i,27]+ len(df["PLAYER"]) - i)
            i += 1

        df["FantasyPoints"] = tempStore
        tempStore.clear()   

df = df.sort_values("FantasyPoints", ascending=False)


# In[24]:


tempStore = []
maxFantasyPoints = len(categories) * len(df["PLAYER"])

i = 0
while i <  len(df["PLAYER"]):
    tempStore.append(round(df.iloc[i,27] / maxFantasyPoints, 3))
    i += 1
    
df["FantasyPoints%"] = tempStore
df = df.sort_values("FantasyPoints", ascending=False)
tempStore.clear()


# In[26]:


df.to_csv(path_or_buf=f"{csvPath}/NBA2017_Output.csv", sep=";")


# In[16]:


height = 7
width = len(categories) * height
fig, axs = plt.subplots(ncols=len(categories), figsize= (width, height))
for index, categorie in enumerate(categories):
    sns.regplot(x=df[categorie], y=df["FantasyPoints"], ax=axs[index])
    


# In[25]:


df

