#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
download_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-elo/nbaallelo.csv"
target_csv_path = "nba_all_elo.csv"

response = requests.get(download_url)
response.raise_for_status()    # Check that the request was successful
with open(target_csv_path, "wb") as f:
    f.write(response.content)
print("Download ready.")


# In[7]:


import pandas as pd
nba = pd.read_csv("nba_all_elo.csv")
type(nba)
<class 'pandas.core.frame.DataFrame'>


# In[8]:


import pandas as pd
nba = pd.read_csv("nba_all_elo.csv")
type(nba)
<class 'pandas.core.frame.DataFrame'>


# In[12]:


import pandas as pd
nba = pd.read_csv("nba_all_elo.csv")
type(nba)
len(nba)
nba.shape
nba.head()


# In[16]:


pd.set_option("display.max.columns", None)
pd.set_option("display.precision", 2)
nba.head()


# In[18]:


#displaying last five rows
nba.tail()
#displaying last 3 rows
nba.tail(3)


# In[20]:


#display data types
nba.info()


# In[23]:


import numpy as np
#showing basics statistics just numeric types
nba.describe()
#include other data type
nba.describe(include=np.object)


# In[30]:


#exploring your dataset
#how often specific values occur in a column
nba["team_id"].value_counts()
nba["fran_id"].value_counts()
#date of games
nba.loc[nba["team_id"] == "MNL", "date_game"].min()
nba.loc[nba["team_id"] == "MNL", "date_game"].max()
nba.loc[nba["team_id"] == "MNL", "date_game"].agg(("min", "max"))


# In[34]:


#how many points did BOS have
nba.loc[nba["team_id"]=="BOS","pts"].sum()


# In[39]:


#Understanding series objects
revenues = pd.Series([5555, 7000, 1980]) #contains indexes and values
print(revenues)
print(revenues.values)
print(revenues.index)


# In[52]:


#indexing the series 
city_revenues = pd.Series([4200, 8000, 6500],index=["Amsterdam","Tokyo","Toronto"])
print(city_revenues)


# In[51]:


#constructing series using dictionry> keys are indexes and vlaues are series values
city_employee_count = pd.Series({"Amsterdam": 5, "Tokyo": 8})
print(city_employee_count)
city_employee_count.keys()
#asking your dataset
"Tokyo" in city_employee_count
"Sarajevo" in city_employee_count


# In[57]:


#Understanding dataFrame objects
#combining series into dataFrame
city_data = pd.DataFrame({"revenue": city_revenues,"employee_count": city_employee_count})
print(city_data)


# In[62]:


city_data.index
#accessing 2 dimensions using axes, row and column index
city_data.axes[1]


# In[64]:


#questioning with keys relates to columns
"Amsterdam" in city_data
"revenue" in city_data
"pts" in nba.keys():




#Accessing series elements
city_revenues["Toronto"]
city_revenues[1]

#city_revenues[-1]
city_revenues[2:]
#city_revenues["Toronto":]


# In[96]:


#accessing Series elements with label-loc and positional-iloc index
colors = pd.Series(["red", "purple", "blue", "green", "yellow"],index=[1, 2, 3, 5, 8])
print(colors)
colors[1]
colors.loc[1]
colors.iloc[1]

colors.loc[3:8]
colors.iloc[-2]


# In[104]:


#Accessing DataFrame elements
city_data["revenue"]
type(city_data["revenue"])
city_data.revenue

toys = pd.DataFrame([
    {"name": "ball", "shape": "sphere"},
    {"name": "Rubik's cube", "shape": "cube"}
])

toys["shape"]

toys.shape #does not produce same result as toys["shape"] since shape is the function


# In[113]:


#using loc and iloc for dataframe
city_data.loc["Amsterdam"]
city_data.loc["Tokyo": "Toronto"]
city_data.iloc[1]
nba.iloc[-2] #displaying second-to-last row of nba set

city_data.loc["Amsterdam": "Tokyo", "revenue"] #first parameter is row and second columns

nba.loc[5555:5559,["team_id","pts"]]


# In[124]:


#QUERYING your data
current_decade = nba[nba["year_id"] > 2010]
print(current_decade)
current_decade.shape

games_with_notes = nba[nba["notes"].notnull()] #where specific field is not null value
print(games_with_notes)

ers = nba[nba["fran_id"].str.endswith("ers")] #converting object to string then performing string functions on them
print(ers)

baltimoree=nba[(nba["_iscopy"]==0)&(nba["pts"]>100)&(nba["opp_pts"]>100)&(nba["team_id"]=="BLB")] #presenting baltimore games removing duplicates, where both teams had points bigger than 100
print(baltimoree) 

LosAteams=nba[(nba["_iscopy"]==0)&(nba["team_id"].str.startswith("LA"))&(nba["year_id"]==1992)&(nba["notes"].notnull())]
print(LosAteams)


# In[151]:


#Grouping and Aggregating your dataset
city_revenues.sum()
city_revenues.max()
nba["pts"].max()

nba.groupby("fran_id", sort=False)["pts"].sum()
#counts how many times team won and lost
nba[(nba["fran_id"]=="Spurs")&(nba["year_id"]>2010)].groupby(["year_id", "game_result"])["game_id"].count()
#counts how many times they played home and another court
nba[(nba["fran_id"]=="Warriors")&(nba["year_id"]==2015)].groupby(["year_id","game_location"])["game_id"].count()


# In[167]:


#MANIPULATING Columns
df = nba.copy()
df.shape
#defining new columns based on existing ones
df["difference"]=df.pts-df.opp_pts
df.shape
df["difference"].max()
#renaming
renamed_df=df.rename(columns={"game_result":"result","game_location":"location"})
renamed_df.info()
#deleting
elo_columns = ["elo_i", "elo_n", "opp_elo_i", "opp_elo_n"]
df.drop(elo_columns, inplace=True, axis=1)
df.shape


# In[172]:


#Specifying data types
df["date_game"] = pd.to_datetime(df["date_game"])
df["game_result"].nunique()
df["game_location"].value_counts()
df["game_location"] = pd.Categorical(df["game_location"])
df["game_location"].dtype
df.info()
df["game_result"] = pd.Categorical(df["game_result"])


# In[181]:


#CLEANING DATA
rows_without_missing_data = nba.dropna()
rows_without_missing_data.shape
data_without_missing_columns = nba.dropna(axis=1)
data_without_missing_columns.shape


# In[182]:


data_with_default_notes = nba.copy()
data_with_default_notes["notes"].fillna(
    value="no notes at all",
    inplace=True
)
data_with_default_notes["notes"].describe()


# In[190]:


#Invalid values
nba[nba["pts"] == 0].empty
nba[(nba["pts"] > nba["opp_pts"]) & (nba["game_result"] != 'W')].empty
nba[(nba["pts"] < nba["opp_pts"]) & (nba["game_result"] != 'L')].empty


# In[195]:


#COMBINING MULTIPLE DATASET - concat()
further_city_data = pd.DataFrame(
    {"revenue": [7000, 3400], "employee_count":[2, 2]},
    index=["New York", "Barcelona"]
)
print(further_city_data)
all_city_data = pd.concat([city_data, further_city_data], sort=False)
print(all_city_data)


# In[204]:


city_countries=pd.DataFrame({"country":["Holland","Japan","Canada","Spain"],"capital":[1,1,0,0]},index=["Amsterdam","Tokyo","Toronto","Barcelona"])
print(city_countries)
cities=pd.concat([all_city_data,city_countries],axis=1,sort=False)
print(cities)
#using MERGE option
countries = pd.DataFrame({
    "population_millions": [17, 127, 37],
    "continent": ["Europe", "Asia", "North America"]
}, index= ["Holland", "Japan", "Canada"])
pd.merge(cities, countries, left_on="country", right_index=True)
pd.merge(
    cities,
    countries,
    left_on="country",
    right_index=True,
    how="left"
)




#VISUALIZING your dataset

nba[nba["fran_id"] == "Knicks"].groupby("year_id")["pts"].sum().plot()

nba[(nba["fran_id"]=="Heat")&(nba["year_id"]==2013)]["game_result"].value_counts().plot(kind="pie")

nba.head()





