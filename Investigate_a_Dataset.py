#!/usr/bin/env python
# coding: utf-8

# > **Tip**: Welcome to the Investigate a Dataset project! You will find tips in quoted sections like this to help organize your approach to your investigation. Before submitting your project, it will be a good idea to go back through your report and remove these sections to make the presentation of your work as tidy as possible. First things first, you might want to double-click this Markdown cell and change the title so that it reflects your dataset and investigation.
# 
# # Project: Investigate a Dataset (Replace this with something more specific!)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# Research Question 1 (What are the highest rating movies?)
# Research Question 2 (Which month has the highest revenue?)
# Research Question 3 (What are the most popular genres by years?!)
# Research Question 4 (What are the relation betwwen the number of movies and year released ?!)
# Research Question 5 (What are the relation between run time and average vote?!)

# In[6]:


# Use this cell to set up import statements for all of the packages that you

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you document your steps carefully and justify your cleaning decisions.
# 
# ### General Properties

# In[7]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df_movies = pd.read_csv('tmdb-movies.csv')
df_movies.info()
df_movies.head()


# In[9]:


df_movies.shape


# In[12]:


# checking the data tupe
df_movies.dtypes


# In[8]:


#checking for missing data
df_movies.isnull().sum()


# In[4]:


#checking unique data
df_movies.nunique()


# In[17]:


#checking duplicated data
df_movies.duplicated().sum()


# # Data Cleaning 
# 1- Removing missing values
# 2- Removing duplicates
# 3- Replacing zero with NAN in runtime column
# 4- Removing 0's from budget and the revenue columns

# In[19]:


#remove the missing values
df_movies.dropna(subset=['imdb_id','cast','director','genres','homepage','tagline','keywords','production_companies'],inplace=True)
df_movies.isnull().sum()


# In[28]:


#remove duplicate
df_movies = df_movies.drop_duplicates()
df_movies.duplicated().sum()


# In[8]:


#Replacing zero with NAN in runtime column
df_movies['runtime']=df_movies['runtime'].replace(0, np.NAN)


# In[6]:


#Removing 0`s from budget and revenue
# creating a seperate list of revenue and budget column
budget_revenue_list=['budget', 'revenue']

#replace all the value from '0' to NAN in the list
df_movies[budget_revenue_list] = df_movies[budget_revenue_list].replace(0, np.NAN)

#removing all the row which has NaN value in temp_list 
df_movies.dropna(subset = budget_revenue_list, inplace = True)


# In[18]:


#save the dataset
df_movies.to_csv('df_movies.csv', index=False)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. Compute statistics and create visualizations with the goal of addressing the research questions that you posed in the Introduction section. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables.
# 
# ### Research Question 1 (What are the highest rating movies?)

# In[32]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.


# In[9]:


# Exploring the histogram of the dataset 
df_movies.hist(figsize=(20,10));


# In[19]:


#Get a list of the top rating movies
df_highest_rating = df_movies.nlargest(10,'vote_average')
print(df_highest_rating)


# In[65]:


sns.set(style="darkgrid");
sns.set(font_scale=2);
f, ax = plt.subplots(figsize=(5, 10));
ax = sns.barplot(x='vote_average', y='original_title', data=df_highest_rating);

ax.set(xlim=(7,8.5), ylabel="Movie Title", xlabel="Average Rating");
plt.title('Top Rating Movies');


# In[ ]:


#from the first question we get the top 10 movies by rating:
#1. The Godfather
#2. Whiplash
#3. Bill Cunningham New York
#4. Fight Club
#5. The Dark Knight
#6. Kill Bill: The Whole Bloody Affair
#7. Schindler's List
#8. Inside Out
#9. Room
#10.Intersteller


# ### Research Question 2  (Which month has the highest revenue?!)

# In[26]:


# changing release year from int to datatime
df_movies = pd.read_csv('df_movies.csv')
df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])
df_movies.dtypes


# In[27]:


# extract month from release year
df_movies['month'] = df_movies['release_date'].apply(lambda x: x.month)
df_movies.head()


# In[12]:


# use groupy to split data
month_revenue = df_movies.groupby('month')['revenue_adj'].sum()
month_revenue


# In[34]:


#plot the relation between month and revenue using bar chart.
sns.set_style('darkgrid')
sns.set(font_scale= 2);
f, ax =  plt.subplots(figsize=(8,12));
month_revenue.plot(kind='bar',title= 'Month release vs Revenue');
plt.ylabel('Revenue Adjusted', fontsize= 15);
plt.xlabel('Month', fontsize=15);


# In[13]:


#From the second question and the month release Vs revenue chart, 
#we can see that June and December have the highest revenue for movie releases.
#Therefore, we can still conclude June and December are "better" months to release movies in, as they'll most likely produce the highest revenue.


# ### Research Question 3  (What are the most popular genres by years?!)

# In[28]:


popular_genres = df_movies.groupby(['release_year','genres'])['popularity'].max().nlargest(20)
popular_genres


# In[ ]:


#the most popular genres in 2015 are action ,adventure, science fiction and thriller.


# #### Research Question 4  (What are the relation between the number of movies and year released?!)

# In[15]:


number_movies=df_movies.groupby('release_year').count()['id']
number_movies


# In[24]:


sns.set_style('darkgrid')
number_movies.plot(xticks = np.arange(1960,2016,5))
sns.set(font_scale= 2);
sns.set(rc={'figure.figsize':(14,5)})
plt.title("Number of Movies Vs Release year",fontsize = 15)
plt.xlabel('Release year')
plt.ylabel('Number Of Movies')


# In[ ]:


# the curve sharply increase. the number of movies produced increased with time


# ##### Research Question 5 (What are the relation between run time and average vote?!)

# In[25]:


df_movies.plot(x='vote_average', y='runtime', kind='scatter', figsize=(14,10))
sns.set(font_scale=2);
sns.set_style('darkgrid')
plt.title('Relation between run time and average vote')
plt.xlabel('vote_average')
plt.ylabel('Runtime');


# In[ ]:


#movies with a runtime around minues have high rating 
#short movies has higher rating than long movies


# <a id='conclusions'></a>
# ## Conclusions
# Throughout this data analysis, I posed questions that Production Companies might
# find useful, This was a very interesting data analysis. We came out with some very interesting facts about movies. After this analysis we can conclude following:
# 1-It is best to release a movie in June or December, because I can conclusively
# say that those movies are more popular and tend to bring in the most revenue espesially june and december have always vacation.
# 2-the number of produced movie increase with time which proved that the movie maker industry is promised industry
# 3-people perfer the short movie and movies with long runtime has lower rating
# 
# ## Limitations
# there are more than 5 to 10% of data having null values or highly correlated having erroneous or missing values or imbalanced data. The sample doesn't represent the population. All these will lead either to wrong analysis which will lead to wrong predictions or biased analysis.
# 
# 
# ## Submitting your Project 
# 
# > Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should get a return code of 0, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# > Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# > Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

