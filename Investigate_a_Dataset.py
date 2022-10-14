#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset - [TMDb movie data]
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
# 
# ### Dataset Description 
# La base de données soumis à notre analyse contient les informations sur 10 000 films obtnues auprès de `Tthe Movie Database (TMDb)`. Elle est constituée de 21 colonnes : 
#  1-id: identifiant du film
#  2-imdb_id: identifiant IMDB du film
#  3-poularity: score de popularité du film
#  4-budget:le budget du film
#  5- revenue: le revenue du film
#  6-genres: le genre du film
#  7- original_title: le tire original
#  8-cast: les acteurs 
#  9-homepage: le site du film
#  10-director: directeur 
#  11-overview: un apperçu
#  12-runtime: durée du film
#  13-release_year: année de réalisation
#  14- release_date: date de réalisation 
#  15- tagline: titre
#  16-vote_count: vote des consommateurs
#  17- vote_average: moyenne des votes
#  18-budget_adj: budget_déflaté
#  19- revenue_adj: revenu déflaté
#  20-production_companies: maison de production
#  21-keywords: les mots clefs
# 
# 
# ### Question(s) 
# 1- Quels sont les types de films les plus populaires d'une année à une autre? 
# 2-Quels relations entre popularité, le revenu et le budget?

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns 
get_ipython().run_line_magic('matplotlib', 'inline')
# Use this cell to set up import statements for all of the packages that you
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# In[2]:


# Upgrade pandas to use dataframe.explode() function. 
#!pip install --upgrade pandas==0.25.0


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 

# In[3]:


# Importation de la base 
df=pd.read_csv('Database_TMDb_movie_data/tmdb-movies.csv')


# ####  Inspection du jeu de données 
# Maintenant que la base a été importée, essayons de commencer par les premières inspections à savoir les types des variables, valeurs manquantes etc.

# In[4]:


# Nombre d'observations  ainsi que le nombre de variables dans la base
print('Le nombre de lingnes dans le jeu de données est:',df.shape[0]) 
print('Le nombre de colonnes  dans le jeu de données est:',df.shape[1])


# ####  Structure de la base de données 

# In[5]:


# Les 21 premières lignes de la base (l'entête inclue) 
df.head(20)


# In[6]:


# les 20 dernières lignes de la base 
df.tail(20)


# In[7]:


# Types des variables, nombre de valeurs non nulles par variable
df.info()


# On remarque que les colonnes de cette base sont de trois types: _entier, chaîne de caractère et flottant_. Aussi, la base contient beaucoup de valeurs manquantes.  

# Esssayons d'en savoir un peu plus sur le nombre de valeurs manquantes par variable.

# In[8]:


# base de données bouléenne, où False signifie que la valeur est non nulle et True le contraire. 
# Inspiré par un travail similaire su kaggle
df_bool=df.isnull()
df_bool.head()


# In[9]:


#sum(df_bool.iloc[:,1:21].astype(bool))
#df_bool.dtypes
#sum(df_bool['homepage'])


# In[10]:


# Nombre de valeurs nulles par variable
df_missing=pd.DataFrame(df_bool.sum(), columns=['Nb_NaN'])
df_missing


# In[11]:


# Nombre total de valeurs manquantes dans la base
sum(df_missing['Nb_NaN'])


# Ainsi, la base contient 13434 valeurs manquantes soit 5.89% des obsevations. 12  des 21 variables ne continnent pas de données manquantes. La variable `homepage` est celle qui contient le plus de données manquantes.

# ### Plus d'inspections
# Détermination des observations dupliquées, des valeurs uniques ect.

# In[12]:


# Nombre de duplication das la base de données 
sum(df.duplicated())


# In[13]:


# Nombre de valeurs unique par variable
df.nunique()


# #### Résumé globale de la partie précédente: 
# Les ispections effectuées précédemment sur le jeux de données montrent qu'il est nécessaire de procéder à certaines modifications afin de rendre la base un peu plus propre. Par exemple,`release_date` doit être transformer en format date. De même l'affichage de la colonne `genres` est trop confuse, il serait intéressant de la rendre un peu plus lisible en séparant les types de films. Un autre problème qu'il faudra prendre en compte dans le nettoyage des données est celui des `budjet, revenue, budget_adj et revenue_adj` qui sont nuls car cela n'est pas logique. 

# 
# ### Data Cleaning
# 

# In[14]:


# Suppression des duplications 
df.drop_duplicates(keep='first', inplace=True)# inspiré par un travail similaire su kaggle
df.shape


# In[15]:


# Conversion de "release_date" et "release_year	" en format date 
df['release_date']=pd.to_datetime(df['release_date'])


# In[16]:


# Types de données après conversion
pd.DataFrame(df.dtypes, columns=['Types'])


# *Attaquons maintenant un des gros problème du jeux de données: __les budgets et revenus nuls des films__*. 

# In[17]:


# Nombre d'enrégistriments avec un revenu nul
#df[df['revenue']==0].count()
sum(df['revenue']==0)


# In[18]:


# Vérifions si le nombre de nuls pour revenue est le même pour revenue_adj
sum(df['revenue']==0)==sum(df['revenue_adj']==0)


# In[19]:


# Nombre d'enrégistriments avec un budget nul
#df[df['budget']==0].count()
sum(df['budget']==0)


# In[20]:


# Vérifions si le nombre de nuls pour budget est le même pour budget_adj
sum(df['budget']==0)==sum(df['budget_adj']==0)


# #### Commentaires: 
# Il n'est pas logique que la réalisation d'un film n'ai pas de buget(coût nul) et n'ai occasionné aucun revenu. Nous interpreterons donc les zéros de ces variables comme des valeurs manquantes. La prochaine étape consistera à  remplacer  ces zéros par des valeurs manquantes.

# In[21]:


# Inpiré par un travail similaire sur kaggle
df['revenue']=df['revenue'].replace(0,np.nan)
df['budget'] = df['budget'].replace(0, np.nan)
df['revenue_adj'] = df['revenue_adj'].replace(0, np.nan)
df['budget_adj'] = df['budget_adj'].replace(0, np.nan)


# In[22]:


sum(df.isnull().sum())


# ##### Traitement des valeurs manquantes
# Les méthodes de traitement des valeurs manquantes telles que imputation par la moyenne ou la médiane, interpolation linéaire etc. semblent appropriées mais après une étape: constitution des groupes de films ayant des caractéristiques similaires et ensuite effectuer l'imputation au sein de chaque groupe. Cela fait appel aux méthodes de classification etc. qui ne sont pas aux programme. 
# ***Pour gérer les données manquantes, nous allons simplement les supprimées***
# Mais la variable `homepage` ayant plus de **7000** de données manquantes, une  suppression  tenant compte de cette variable porrait réduire significativement la taille de l'échantillon. ***Il faudra dont l'exclure***

# In[23]:


new_columns=(['id', 'imdb_id', 'popularity', 
              'budget', 'revenue', 'original_title',
              'cast',  'director', 'tagline', 
              'keywords', 'overview',
               'runtime', 'genres', 'production_companies', 'release_date',
                'vote_count', 'vote_average', 'release_year', 'budget_adj',
                'revenue_adj']
            )


# In[24]:


df=df[new_columns]


# In[25]:


df.dropna(inplace=True)
df.shape


# Terminons la partie de néttoyage en rendant plus lisible la variable `genres`. Pour cela, on va considérer le type du film est la premier élément. Par exemple
# pour *Action|Drama|Thriller|Crime|Mystery, le type sera __Action__*

# In[26]:


df['genres']=(df['genres']).str.split("|", expand=True)[0]
df.head(20)


# In[27]:


#Conversion de la variable 'id' en chaîne
df['id']=df['id'].astype(str)


# In[28]:


df.describe()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# Nos variables d'intérêt sont: `popularity, genres, revenue_adj et budget_adj`
# 
# ### Quels sont les types de films les plus populaires d'une année à une autre? 

# Interessons-nous  premièrement à la variable `genres`

# In[29]:


#Les types de films distincts
df['genres'].nunique()


# In[30]:


# Visualisation
df['genres'].value_counts().sort_values(ascending=True).plot(kind='barh',figsize=(8,8))
plt.title('Nombre de films produits pour chaque type de film')
plt.xlabel('Nombre de films');


# Les films de type dramatiques semblent être les plus produits sur l'ensemble de la période.
# *Pour répondre à la question posée, visualisons le nombre de film produits pour chaque type au fil des années.* 

# In[31]:


# Nombre de films produits chaque années pour chaque type de film
df.groupby('release_year')['genres'].value_counts().plot(kind='bar')
plt.title('Nombre de films produits pour chaque type par année ');


# Comme on peut le constater, le graphique ci-dessous n'est pas du tout lisible. Afin d'améliorer la visualition des données, essayons de construire une variable `decenie` qui désigne la décénie dans laquelle le film a été réalisé. ***Cette idée a été inspirée par un travail similaire sur kaggle*** 

# In[32]:



bin_dec=[1960,1970,1980, 1990,2000,2010, 2015]
bin_dec_names=['60_69','70_79','80_89','90_99','20_09','10+']
df['decenie']=pd.cut(df['release_year'],bin_dec, labels=bin_dec_names)


# In[33]:


# Moyenne de la popularité de cahque type film au cours des décénie
# Inspiré sur kaggle 
df_dec_mean=(df.groupby(
    ['decenie', 'genres'], as_index=False)['popularity'].mean()

             )
df_dec_mean.head()
# Formation des sous groupes: décénie-type
dec_60=df_dec_mean.query('decenie=="60_69"').sort_values(by=['popularity'],ascending=True)
dec_70=df_dec_mean.query('decenie=="70_79"').sort_values(by=['popularity'],ascending=True)
dec_80=df_dec_mean.query('decenie=="80_89"').sort_values(by=['popularity'],ascending=True)
dec_90=df_dec_mean.query('decenie=="90_99"').sort_values(by=['popularity'],ascending=True)
dec_20=df_dec_mean.query('decenie=="20_09"').sort_values(by=['popularity'],ascending=True)
dec_10_plus=df_dec_mean.query('decenie=="10+"').sort_values(by=['popularity'],ascending=True)


# In[34]:


#dec_60.head()


# In[35]:


# Réalisation des graphiques des types de films et leurs popularités pour chaque décénie 
# à partir d'une boucle for.
for elt in [dec_60, dec_70, dec_80, dec_90, dec_20, dec_10_plus]:
    elt.plot.barh(x='genres', y='popularity')
    plt.title('Popularité Vs Type de film de la décénie'+" "+str(elt.decenie[0]))
    plt.xlabel('Popularité')
    plt.ylabel('Types de films')


# In[36]:


#dec_60.plot.barh(x='genres', y='popularity')
#dec_70.plot.barh(x='genres', y='popularity')
#dec_80.plot.barh(x='genres', y='popularity')
#dec_90.plot.barh(x='genres', y='popularity')
#dec_20.plot.barh(x='genres', y='popularity')
#dec_10_plus.plot.barh(x='genres', y='popularity');


# #### Commentaires:
# Les films d'actions semblent être de plus en plus populaire au fil des années. Aussi, les films de type western, qui auraient perdues leur popularité, semblent revenir sur la scène au cours des deux dernières décénies.   

# ### Quels relations entre popularité, le revenu et le budget?

# On s'instéressera aux varibles: `popularity', 'budget_adj','revenue_adj`

# In[37]:


df_new=df[['popularity', 'budget_adj','revenue_adj']]


# In[38]:


# Statistiques élémentaires 
df_new.describe()


# In[39]:


# Histogrammes des variables 
df_new.hist(figsize=(8,8), color='b'); 


# In[40]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.


# In[41]:


# Définition d'une fonction pour le : Nuage de points popularité et revenue/budget
def df_scatter(df_new,var, titre):
    plt.scatter(x=df_new[var], y=df_new['popularity'], color='b')
    plt.xlabel(var)
    plt.ylabel('Popularité')
    plt.title(titre);


# In[42]:


# Nuage de points popularité et revenue
df_scatter(df_new,'revenue_adj', 'Popularité Vs Revenue')


# Il semble exister une rellation positive entre le revenue et la popularité.

# In[43]:


# Nuage de points popularité et revenue
df_scatter(df_new,'budget_adj', 'Popularité Vs Budget')


# Il semble exister une rellation positive entre le budget et la popularité.

# <a id='conclusions'></a>
# ## Conclusions
# L'analyse exploratoire des données nous a permis d'identifier des types de films qui sont de plus en plus populaire (les films d'actions par exemple) et d'autres dont la popularité semble dimuner. De plus, on a remarqué qu'il pourrait exister un lien posivitif entre la popularité des films et le bubget consacré à leurs réalisations d'une part et également entre le revenu engendré par le film. 
# 
# Une principale limite dans notre analyse concerne les données manquantes. Après toute transformation, un total de **36857** de valeurs sont manquantes; cela constitue une grande limite pour de bonnes analyses. Surtout que les varibles d'intérêt `revenue_adj et budget_adj`sont concernées par ces valeurs manquantes, nos analyses pourraient être entachées d'erreurs. 
# Il serait intéressant d'utiliser des méthodes performantes pour l'imputation des données manquantes.
# 
# Des recherches supplémentaires devraient être effectuer pour trouver des méthodes d'imputation des données manquantes beaucoup plus adadptées à notre contexte. 
# 
# 
# 

# In[44]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# ### Sources utilisées:
# 1- Cours Udacity
# 2- kaggle: TMDB 5000 Movie Dataset
# 3- kaggle: The Story of Film
# 4- GeeksforGeeks
# 5-Numpy: nupyrepeat
# 6-pandas: pandas.DataFrame.append
# 7- matplotlib:(Figure labels: suptitle, supxlabel, supylabel)
# 8-stackoverflow : How do I change the figure size with subplots?

# In[ ]:




