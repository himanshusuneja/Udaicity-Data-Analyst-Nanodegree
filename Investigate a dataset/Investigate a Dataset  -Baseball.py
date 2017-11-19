
# coding: utf-8

# # Database - Baseball

# I used "Salaries.csv" and "AwardsSharePlayers.csv" for my project and my question to this database is "What factors have an effect on team salaries?" There are total 5 columns and I am going to analyze yearID, teamID and igID to investigate how these columns are related to salaries.
# 

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# In[3]:


import matplotlib.pyplot as plt


# In[4]:


import seaborn as sns


# In[5]:


Salaries_filename = 'C:/users/Guhy/Salaries.csv'
AwardSharePlayers_filename = 'C:/users/Guhy/AwardSharePlayers.csv'


# In[6]:


# import Salaries data
Salaries_filename = 'Salaries.csv'
salariesDF = pd.read_csv(Salaries_filename)

# import Players data
AwardSharePlayers_filename = 'AwardsSharePlayers.csv'
playersDF = pd.read_csv(AwardSharePlayers_filename)

salariesDF.head()


# In[7]:


playersDF.head()


# Checking, is there any null value in the data. First salaries data.

# In[8]:


pd.isnull(salariesDF)


# In[9]:


pd.isnull(salariesDF).sum()


# Checking all the zeors in the columns

# In[10]:


salariesDF[salariesDF["yearID"] == 0]


# In[11]:


salariesDF[salariesDF["teamID"] == 0]


# In[12]:


salariesDF[salariesDF["salary"] == 0]


# In[13]:


salariesDF[salariesDF["lgID"] == 0]


# In[14]:


salariesDF[salariesDF["playerID"] == 0]


# Seems to be there are two players with 0 salaries. Ltes investigate them

# In[15]:


salariesDF[salariesDF["playerID"] =="jamesdi01"]


# It seems to be there is some missing data. let us assume that james salary in the year 1993 is the average of the year 1992 and 1995. 

# In[17]:


salariesDF["salary"].iloc[6179] = (387500 + 350000) / 2
salariesDF[salariesDF["playerID"] == "jamesdi01"]

# Taken the average of above and below salary


# In[18]:


# Checking for Martija02

salariesDF[salariesDF["playerID"] =="martija02"]


# Since the data volume is low, hence let us ignore these columns

# In[19]:


salariesDF = salariesDF[salariesDF["playerID"] != "martija02"]


# In[20]:


salariesDF.describe()


# Now checking with AwardsShareData

# In[21]:


# checking null values

pd.isnull(playersDF).sum()


# VotersFirts column has 358 null values. But in my investigation, there is no use of thi column. So i am going to focus on remaining columns where there is no null values.

# In[22]:


playersDF.describe()


# Investigating Salaries with 1D explation (single-variale)

# In[23]:


# Plotting Histogram

get_ipython().magic(u'matplotlib inline')
plt.hist(salariesDF["salary"]/1000000, bins = 10)
plt.ylabel("Frequency")
plt.xlabel("Salary in millions")
plt.title('salaries Frequency')


# In Histogram above, we can clearly see that most of the salaries are below 2.5 million and there are very few in above 2.5 millon range

# Now, i will look into relationship between teamID and salary by finding sum, mean, min and max through them.

# In[24]:


# Creating Database

salariesDF_teamID = salariesDF[["teamID","salary"]]

salariesDF_summary_by_teamID = salariesDF_teamID.groupby("teamID").agg([np.sum,np.max,np.min,np.mean])
salariesDF_summary_by_teamID.columns = ["sum", "max", "min", "mean"]
salariesDF_summary_by_teamID.head()


# In[25]:


def bargraph(column): # column = sum, max, min, mean
    frequency = salariesDF_summary_by_teamID[column].sort_values(axis=0, ascending = False).head(10)
    objects = frequency.index
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, frequency, align='center')
    plt.xticks(y_pos, objects)
    plt.ylabel('Salary')
    plt.title("Top 10 {} of salaries by teamID".format(column))
    print "Top 10 {} of salaries by teamID".format(column)
    print frequency
    plt.show()


# In[26]:


get_ipython().magic(u'matplotlib inline')
bargraph("sum")
bargraph("max")
bargraph("min")
bargraph("mean")


# Now i am going to investsigate 2D exploration
# 
# I found that the pointswon and pointsmax both have affects on salaries.But i will investigate pointswon by setting up pointswon as independent variable and dalaries as dependent  variable

# Reindexing the salary dataframe with a key value set (year, player ID) 

# In[40]:


keyValue = ("{}, {}".format(salariesDF["yearID"].iloc[i],salariesDF["playerID"].iloc[i]) for i in range(len(salariesDF)))

salariesDFkv = pd.DataFrame(salariesDF.values, columns = list(salariesDF.columns.values), index = list(keyValue))
salariesDFkv


# Reindexing the Players dataframe with the key value(year, player ID).

# In[28]:


keyValue = ("{}, {}".format(playersDF["yearID"].iloc[i],playersDF["playerID"].iloc[i]) for i in range(len(playersDF)))

playersDFkv = pd.DataFrame(playersDF.values, columns = list(playersDF.columns.values), index = list(keyValue))
playersDFkv.head()


# Merging both salary and players dataframe
# 

# In[29]:


salaryPlayerDF = pd.merge(salariesDFkv, playersDFkv, how = "inner")
salaryPlayerDF.head()


# Now, In order to find the correlation between pointswon and salary, we need to standardize each colums of both.

# In[30]:


# Standardizing
def standard(sr):
    return (sr - sr.mean())/sr.std(ddof=0)

salaryPlayerDF = salaryPlayerDF[["pointsWon", "salary"]]


# In[31]:


# Creating scatter plot for better understanding

get_ipython().magic(u'matplotlib inline')
plt.scatter(salaryPlayerDF["pointsWon"], salaryPlayerDF["salary"])
plt.title('Scatter Plot')
plt.xlabel('salaries of Players')
plt.ylabel('Points Won')
plt.show()


# In[32]:


salariesDF_by_year = salariesDF[["yearID","salary"]].groupby("yearID").agg([np.sum,np.max,np.min,np.mean])
salariesDF_by_year.columns = ["sum", "max", "min", "mean"]


get_ipython().magic(u'matplotlib inline')
PlotList = ["sum", "max", "min", "mean"]

for item in PlotList:
    plt.title('{} by year'.format(item.upper()))
    plt.xlabel('Year')
    plt.ylabel('Salary')
    
    plt.plot(salariesDF_by_year.index, salariesDF_by_year[item])
    plt.show()
    


# Since all the graphs are increasing as the year progress,but in maximum graph there is a fall in the graph near year 2014.  

# In[33]:


# Invesigating Maximum Graph

maxSalaryByYear = salariesDF_by_year["max"].argmax()

print "\nMaximum salary in {}, $ {}\n".format(maxSalaryByYear, salariesDF_by_year["max"].loc[maxSalaryByYear])


# In[34]:


maxDFyear = salariesDF[salariesDF["yearID"]==2009]
maxPlayer2009 = maxDFyear[maxDFyear["salary"] == salariesDF_by_year["max"].loc[maxSalaryByYear]]
maxPlayerID = maxPlayer2009["playerID"].values[0]
print maxPlayerID
print "Detailed information of the player"
print maxPlayer2009


# In[35]:


# Reationship between year and salary
# Histogram

salaryYearDF = salariesDF[["yearID","salary"]]
standardizedDF = salaryYearDF.apply(standard)


get_ipython().magic(u'matplotlib inline')

plt.title("Salaries by year")

plt.plot(standardizedDF["yearID"], standardizedDF["salary"])


# In[36]:


# Reationship between year and salary
# Histogram

salaryYearDF = salariesDF[["yearID","salary"]]
standardizedDF = salaryYearDF.apply(standard)

get_ipython().magic(u'matplotlib inline')
plt.scatter(standardizedDF["yearID"], standardizedDF["salary"])
plt.title("Salaries by year")


# In[37]:


# Correlation

correlation = (standardizedDF["yearID"] * standardizedDF["salary"]).mean()
print "Correlation between salaries and year:",correlation


# Thus there is a positive correlation between years and salaries of the players

# In[38]:


# Relatonship between year and salary
# Vetiorized operations

salaryYearDF = salariesDF[["yearID","teamID","salary"]].groupby(["yearID","teamID"]).mean()

x = salaryYearDF.index.values
x = np.array(map(lambda x: int(x[0]), x))

y = salaryYearDF.values.reshape(1, len(salaryYearDF.values))[0]

x = (x - x.mean()) / x.std()
y = (y - y.mean()) / y.std()


get_ipython().magic(u'matplotlib inline')
plt.scatter(x,y)
plt.title("Means of teams by year")


# The above graph is showing the means of teams salries, not the salaries of the players. Here we can see that the minimum 
# salaries is increasing as the year progress.

# In[39]:


correlation = (x * y).mean()
print "Correlation between mean salaries by team and year:", correlation


# # CONCLUSION

# 1) Since the data volume of martija02 was very low, i have left that player from my dataset.
# 

# 2) The salary of jamesdi01 for the year 1993 was missing, so i took the assumption of that year salary equall to tha average of salary earned by him between year 1993-1995.
# 

# 3) I found the data appropriate to find answers of my investigaion.
# 

# 4) There are many tools such s 'R' and 'SQL' could be used to perfoem statistical test to find the exploration of this data.
