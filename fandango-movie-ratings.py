# Has Fandago considered Walt's analysis in its more recent ratings?
# https://fivethirtyeight.com/features/fandango-movies-ratings/
# In the above article, we consider Walt Hickey's analysis of Fandago's scale of over-archingly 
# lending an overly positive rating of its movies to encourage its bias in selling movie tickets. 
# From a list of 437 films considered reviewed by one user or more, 98 percent was found to be rated 
# at least three stars and 75 percent had at least a four star rating, as shown in the 
# fivethirtyeight article linked above.
# Fandago described the rounding disparity — by which, for example, 4.1 is rounded to 4.5 — as a bug in 
# the system rather than a general practice (Hicky, last couple paragraphs).
# “If you look over the last 20 years, the release strategy used to be much more based around a movie playing 
# for a long time, perhaps releasing regionally and building word-of-mouth around the country,” said box office 
# analyst Bruce Nash, who operates The-Numbers.com, which tracks box office data. “Today, it’s much more focused 
# on getting into theaters opening weekend and hitting as hard as you can with the opening. For that, I think the 
# reviews can have more of an effect” (Hicky, Last two paragraphs).
# In this way, Fandango is accused of inventing an AI critic to promote its films. Some say it shouldn't be taken 
# seriously as some like Todd VanDerWerff (again found in the Hicky article), that "whether a movie is 
# good or bad [is]... a very personal question.”



# UNDERSTANDING THE DATA 
######################################
# We'll work with two samples of movie ratings:the data in one sample was collected previous to Hickey's analysis, 
# while the other sample was collected after. 

import pandas as pd
pd.options.display.max_columns = 100

previous = pd.read_csv('fandango_score_comparison.csv')
after = pd.read_csv('movie_ratings_16_17.csv')

previous.head(3)

after.head(3)

#We make copies to avoid any SettingWithCopyWarning later on.

fandango_previous = previous[['FILM', 'Fandango_Stars', 'Fandango_Ratingvalue', 'Fandango_votes', 'Fandango_Difference']].copy()
fandango_after = after[['movie', 'year', 'fandango']].copy()

fandango_previous.head(3)

fandango_after.head(3)


# The population of interest is all the movie ratings stored on Fandango's website, irrespective of releasing year.
# The data we're working with was sampled at the moments we want: one sample was taken previous to the analysis, and the other 
# after the analysis. We want to describe the population, so we need to show the samples as representative, otherwise 
# there's high likelihood large sampling error and, ultimately, wrong conclusions.

# From Hickey's article:
# The movie must have had at least 30 fan ratings on Fandango's website at the time of sampling (Aug. 24, 2015).
# The movie must have had tickets on sale in 2015.

# The sampling was not random as not every movie had the same chance to be included in the sample.This sample is most likely not reperesentative
# as it's subject to temporal trends — e.g. movies in 2015 might have been outstandingly good or bad compared to other years.

# The sampling conditions for our other sample were:
# The movie must have been released in 2016 or later.
# The movie must have had a considerable number of votes and reviews.
# This second sample is also subject to temporal trends and it's unlikely to be representative of our population of interest.

# CHANGING THE GOAL OF ANALYSIS
# New goal: is there any difference between Fandango's ratings for popular movies in 2015 and Fandango's ratings for popular movies in 2016?
# With this new research goal, we have two populations of interest:

# All Fandango's ratings for popular movies released in 2015 and 2016.
# When we refer to popular, we will utilize Hickey's benchmark so a movie will be considered popular if it has 30 fan ratings or more on the Fandango site.
# In our second sample is movie popularity, so to check the representativity we sample randomly 10 movies from it and then check the number of 
# fan ratings ourselves on Fandango's website. Ideally, at least 8 out of the 10 movies have 30 fan ratings or more.



fandango_after.sample(10, random_state = 1)
# Above we used a value of 1 as the random seed. It's meant to show an unwillingness to trying out various 
# random seeds which would bias towards a favorable sample.
# 90% of the movies in our sample are popular. The documentation states clearly that there're 
# only movies with at least 30 fan ratings; here we double-check.

sum(fandango_previous['Fandango_votes'] < 30)
# Exploring the two data sets, there are movies with a releasing year different than 2015 
# or 2016. Next, we extract it from the strings in the FILM column.

fandango_previous.head(2)

fandango_previous['Year'] = fandango_previous['FILM'].str[-5:-1]
fandango_previous.head(2)

#isolating the movies released in 2015:
fandango_previous['Year'].value_counts()

fandango_2015 = fandango_previous[fandango_previous['Year'] == '2015'].copy()
fandango_2015['Year'].value_counts()

# isolating the movies in the other data set:
fandango_after.head(2)

fandango_after['year'].value_counts()

fandango_2016 = fandango_after[fandango_after['year'] == 2016].copy()
fandango_2016['year'].value_counts()


# Comparing Distribution Shapes for 2015 and 2016
# analyzing & comparing the distributions of movie ratings for the two samples:
# using kernel density plots
import matplotlib.pyplot as plt
from numpy import arange
%matplotlib inline
plt.style.use('fivethirtyeight')

fandango_2015['Fandango_Stars'].plot.kde(label = '2015', legend = True, figsize = (8,5.5))
fandango_2016['fandango'].plot.kde(label = '2016', legend = True)

plt.title("Comparing distribution shapes for Fandango's ratings\n(2015 vs 2016)", y = 1.07)
plt.xlabel('Stars')
plt.xlim(0,5)
plt.xticks(arange(0,5.1,.5))
plt.show() 

# Both distributions are strongly left skewed. 
# The slight left shift of the 2016 distribution shows that ratings were slightly lower in 2016 compared to 2015. 

# COMPARING RELATIVE FREQUENCIES
#####################################
# Examining the frequency tables of the two distributions to analyze some numbers. 
# The data sets have different numbers of movies, so adjustments to the tables with percentages are made.

print('2015' + '\n' + '-' * 16) 
fandango_2015['Fandango_Stars'].value_counts(normalize = True).sort_index() * 100

print('2016' + '\n' + '-' * 16)
fandango_2016['fandango'].value_counts(normalize = True).sort_index() * 100

# 2016 vs. 2015: 2016 was found to have one percent of films to have a five star rating; in 2015, five star ratings were five percent of films.
# In the same vien, four point five ratings also decreased by approxiamately thirteen percent. And again, in 2016, there are lower ratings overall
# accounting for the change of the lowest ratings from a startling solid three point rating to two point five.  

#There were juxtaposing results too. More films grew to receive three point five and four point ratings overall in 2016 over 2015. 
#There may be continued bias and it may be combined with previous ingrained issues of finding simply better movies overall in 2016.

mean_2015 = fandango_2015['Fandango_Stars'].mean()
mean_2016 = fandango_2016['fandango'].mean()

median_2015 = fandango_2015['Fandango_Stars'].median()
median_2016 = fandango_2016['fandango'].median()

mode_2015 = fandango_2015['Fandango_Stars'].mode()[0] 
mode_2016 = fandango_2016['fandango'].mode()[0]

summary = pd.DataFrame()
summary['2015'] = [mean_2015, median_2015, mode_2015]
summary['2016'] = [mean_2016, median_2016, mode_2016]
summary.index = ['mean', 'median', 'mode']
summary

plt.style.use('fivethirtyeight')
summary['2015'].plot.bar(color = '#0066FF', align = 'center', label = '2015', width = .25)
summary['2016'].plot.bar(color = '#CC0000', align = 'edge', label = '2016', width = .25,
                         rot = 0, figsize = (8,5))

plt.title('Comparing summary statistics: 2015 vs 2016', y = 1.07)
plt.ylim(0,5.5)
plt.yticks(arange(0,5.1,.5))
plt.ylabel('Stars')
plt.legend(framealpha = 0, loc = 'upper center')
plt.show()

# The mean was less in 2016 by an estimate of 0.2.
(summary.loc['mean'][0] - summary.loc['mean'][1]) / summary.loc['mean'][0]
# The mode is less in 2016 by 0.5. 
# The median is the same for both distributions. 
# The direction on the kernel density plot is further vouched for: 
# On average, popular movies released in 2016 were rated lower than popular movies released in 2015.
# Overall, bias can be concluded to have been accounted for. 