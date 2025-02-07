#!/usr/bin/env python
# coding: utf-8

# ## 1. Where are the old left-handed people?
# 
# <p>In this notebook, we will explore this phenomenon using age distribution data to see if we can reproduce a difference in average age at death purely from the changing rates of left-handedness over time, refuting the claim of early death for left-handers. This notebook uses <code>pandas</code> and Bayesian statistics to analyze the probability of being a certain age at death given that you are reported as left-handed or right-handed.</p>
# <p>A National Geographic survey in 1986 resulted in over a million responses that included age, sex, and hand preference for throwing and writing. Researchers Avery Gilbert and Charles Wysocki analyzed this data and noticed that rates of left-handedness were around 13% for people younger than 40 but decreased with age to about 5% by the age of 80. They concluded based on analysis of a subgroup of people who throw left-handed but write right-handed that this age-dependence was primarily due to changing social acceptability of left-handedness. This means that the rates aren't a factor of <em>age</em> specifically but rather of the <em>year you were born</em>, and if the same study was done today, we should expect a shifted version of the same distribution as a function of age. Ultimately, we'll see what effect this changing rate has on the apparent mean age of death of left-handed people, but let's start by plotting the rates of left-handedness as a function of age.</p>
# <p>This notebook uses two datasets: <a href="https://www.cdc.gov/nchs/data/statab/vs00199_table310.pdf">death distribution data</a> for the United States from the year 1999 (source website <a href="https://www.cdc.gov/nchs/nvss/mortality_tables.htm">here</a>) and rates of left-handedness digitized from a figure in this <a href="https://www.ncbi.nlm.nih.gov/pubmed/1528408">1992 paper by Gilbert and Wysocki</a>. </p>

# In[2]:


#importing libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[3]:


# ... YOUR CODE FOR TASK 1 ...

# load the data
lefthanded_data = pd.read_csv("https://gist.githubusercontent.com/mbonsma/8da0990b71ba9a09f7de395574e54df1/raw/aec88b30af87fad8d45da7e774223f91dad09e88/lh_data.csv")

#printing first 10 rows of the dataset
print("Dataset: Left-handedness rates of male and female at a given age according to data collected in 1986\n ")
print("First 5 rows of the dataset:")
print(lefthanded_data.head(), "\n")

# plot male and female left-handedness rates vs. age
print("Visualization of left-handedness v/s age using scatter plot.\n")
plt.scatter(lefthanded_data.Age, lefthanded_data.Female, marker = 'o', label = 'Female left-handedness rate') # plot "Female" vs. "Age"
plt.scatter(lefthanded_data.Age, lefthanded_data.Male, marker = 'x', label = 'Male left-handedness rate') # plot "Male" vs. "Age"
plt.legend() # add a legend
plt.title("Male and female left-handedness rates vs age")
plt.xlabel("Age")
plt.ylabel("Left-handedness rate")
plt.show()


# ## 2. Rates of left-handedness over time
# <p>Let's convert this data into a plot of the rates of left-handedness as a function of the year of birth, and average over male and female to get a single rate for both sexes. </p>
# <p>Since the study was done in 1986, the data after this conversion will be the percentage of people alive in 1986 who are left-handed as a function of the year they were born. </p>

# In[4]:


# create a new column for birth year of each age
birth_year = [1986-i for i in lefthanded_data.Age]
lefthanded_data['Birth_year'] = birth_year

# create a new column for the average of male and female left-handedness rate
mean_lh = [(lefthanded_data.Male[i] + lefthanded_data.Female[i])/2 for i in range(len(lefthanded_data.Age))]
lefthanded_data['Mean_lh'] = mean_lh

print("Updated dataset 'lefthanded data' after adding birth year column and Mean_lh column which is the average left-handedness rate:\n")
print(lefthanded_data.head())

# create a plot of the 'Mean_lh' column vs. 'Birth_year'
print("Visualization of average left-handedness v/s birth year using line graph.\n")
plt.plot(lefthanded_data.Birth_year, lefthanded_data.Mean_lh, color = 'green')
plt.title('Birth year vs Average of male and female left-handedness rate')
plt.xlabel("Birth Year")
plt.ylabel("Average of male and female left-handedness rate")
plt.show()


# ## 3. Applying Bayes' rule
# <p>The probability of dying at a certain age given that you're left-handed is <strong>not</strong> equal to the probability of being left-handed given that you died at a certain age. This inequality is why we need <strong>Bayes' theorem</strong>, a statement about conditional probability which allows us to update our beliefs after seeing evidence. </p>
# <p>We want to calculate the probability of dying at age A given that you're left-handed. Let's write this in shorthand as P(A | LH). We also want the same quantity for right-handers: P(A | RH). </p>
# <p>Here's Bayes' theorem for the two events we care about: left-handedness (LH) and dying at age A.</p>
# <p>$$P(A | LH) = \frac{P(LH|A) P(A)}{P(LH)}$$</p>
# <p>P(LH | A) is the probability that you are left-handed <em>given that</em> you died at age A. P(A) is the overall probability of dying at age A, and P(LH) is the overall probability of being left-handed. We will now calculate each of these three quantities, beginning with P(LH | A).</p>
# <p>To calculate P(LH | A) for ages that might fall outside the original data, we will need to extrapolate the data to earlier and later years. Since the rates flatten out in the early 1900s and late 1900s, we'll use a few points at each end and take the mean to extrapolate the rates on each end. The number of points used for this is arbitrary, but we'll pick 10 since the data looks flat-ish until about 1910. </p>

# In[5]:


# ... YOUR CODE FOR TASK 3 ...

# create a function for P(LH | A)
def P_lh_given_A(ages_of_death, study_year = 1990):
    """ P(Left-handed | ages of death), calculated based on the reported rates of left-handedness.
    Inputs: numpy array of ages of death, study_year
    Returns: probability of left-handedness given that subjects died in `study_year` at ages `ages_of_death` """
    
    # Use the mean of the 10 last and 10 first points for left-handedness rates before and after the start 
    early_1900s_rate = sum(lefthanded_data.Mean_lh[0:10])/10
    late_1900s_rate = sum(lefthanded_data.Mean_lh[-10::1])/10
    middle_rates = lefthanded_data.loc[lefthanded_data['Birth_year'].isin(study_year - ages_of_death)]['Mean_lh']
    youngest_age = study_year - 1986 + 10 # the youngest age is 10
    oldest_age = study_year - 1986 + 86 # the oldest age is 86
    
    P_return = np.zeros(ages_of_death.shape) # create an empty array to store the results
    # extract rate of left-handedness for people of ages 'ages_of_death'
    P_return[ages_of_death > oldest_age] = late_1900s_rate /100
    P_return[ages_of_death < youngest_age] = early_1900s_rate /100
    P_return[np.logical_and((ages_of_death <= oldest_age), (ages_of_death >= youngest_age))] = middle_rates / 100
    return P_return


# ## 4. When do people normally die?
# <p>To estimate the probability of living to an age A, we can use data that gives the number of people who died in a given year and how old they were to create a distribution of ages of death. If we normalize the numbers to the total number of people who died, we can think of this data as a probability distribution that gives the probability of dying at age A. The data we'll use for this is from the entire US for the year 1999 - the closest I could find for the time range we're interested in. </p>
# <p>In this block, we'll load in the death distribution data and plot it. The first column is the age, and the other columns are the number of people who died at that age. </p>

# In[6]:


# Death distribution data for the United States in 1999
data_url_2 = "https://gist.githubusercontent.com/mbonsma/2f4076aab6820ca1807f4e29f75f18ec/raw/62f3ec07514c7e31f5979beeca86f19991540796/cdc_vs00199_table310.tsv"

# load death distribution data
death_distribution_data = pd.read_table(data_url_2)
#Drop first row of this dataset as it contains total no. of deaths which can make the analysis biased for age considered 'All'
death_distribution_data.drop(0, inplace = True) 
#print(type(death_distribution_data.Age[2])) ........ ages are taken as string here
#converting ages from string to int
death_distribution_data.Age = [ int(i) for i in death_distribution_data.Age] 

print("Dataset: No. of deaths at a given age in 1999\n")
print(death_distribution_data)

# drop NaN values from the `Both Sexes` column
death_distribution_data.dropna(subset = ['Both Sexes'], inplace = True)

# plot number of people who died as a function of age
print("Visualization of no. of deaths v/s age using scatter plot.\n")
plt.scatter(death_distribution_data.Age, death_distribution_data['Both Sexes'], marker = '*')
plt.title("Both sexes death count v/s Age at which they died")
plt.xlabel("Age")
plt.ylabel("No. of deaths")
plt.show()


# ## 5. The overall probability of left-handedness
# <p>In the previous code block we loaded data to give us P(A), and now we need P(LH). P(LH) is the probability that a person who died in our particular study year is left-handed, assuming we know nothing else about them. This is the average left-handedness in the population of deceased people, and we can calculate it by summing up all of the left-handedness probabilities for each age, weighted with the number of deceased people at each age, then divided by the total number of deceased people to get a probability. In equation form, this is what we're calculating, where N(A) is the number of people who died at age A (given by the dataframe <code>death_distribution_data</code>):</p>
# <p><img src="https://i.imgur.com/gBIWykY.png" alt="equation" width="220"></p>
# <!--- $$P(LH) = \frac{\sum_{\text{A}} P(LH | A) N(A)}{\sum_{\text{A}} N(A)}$$ -->

# In[7]:


def P_lh(ages_of_death, death_distribution_data, study_year = 1990): # sum over P_lh for each age group
    """ Overall probability of being left-handed if you died in the study year
    Input: dataframe of death distribution data, study year
    Output: P(LH), a single floating point number """
    s = death_distribution_data['Both Sexes']
    p_lh_given_A = P_lh_given_A(ages_of_death, study_year)
    p_list = [p_lh_given_A[i] * s[i+7] for i in range(0,109)] # multiply number of dead people by P_lh_given_A
    p = sum(p_list) # calculate the sum of p_list
    return p/sum(s) # normalize to total number of people (sum of death_distribution_data['Both Sexes'])


# ## 6. Putting it all together: dying while left-handed (i)
# <p>Now we have the means of calculating all three quantities we need: P(A), P(LH), and P(LH | A). We can combine all three using Bayes' rule to get P(A | LH), the probability of being age A at death (in the study year) given that you're left-handed. To make this answer meaningful, though, we also want to compare it to P(A | RH), the probability of being age A at death given that you're right-handed. </p>
# <p>We're calculating the following quantity twice, once for left-handers and once for right-handers.</p>
# <p>$$P(A | LH) = \frac{P(LH|A) P(A)}{P(LH)}$$</p>
# <p>First, for left-handers.</p>
# <!--Notice that I was careful not to call these "probability of dying at age A", since that's not actually what we're calculating: we use the exact same death distribution data for each. -->

# In[8]:


def P_A_given_lh(ages_of_death, death_distribution_data, study_year = 1990):
    """ The overall probability of being a particular `age_of_death` given that you're left-handed """
    s = sum(death_distribution_data['Both Sexes'])
    P_A = [i / s for i in death_distribution_data['Both Sexes']][7:117]
    P_left =  P_lh(ages_of_death, death_distribution_data, study_year) # use P_lh function to get probability of left-handedness overall
    P_lh_A = P_lh_given_A(ages_of_death, study_year)# use P_lh_given_A to get probability of left-handedness for a certain age
    return P_lh_A*P_A/P_left


# ## 7. Putting it all together: dying while left-handed (ii)
# <p>And now for right-handers.</p>

# In[9]:


def P_A_given_rh(ages_of_death, death_distribution_data, study_year = 1990):
    """ The overall probability of being a particular `age_of_death` given that you're right-handed """
    s = sum(death_distribution_data['Both Sexes'])
    P_A = [i / s for i in death_distribution_data['Both Sexes']][7:117]
    P_left =  P_lh(ages_of_death, death_distribution_data, study_year)
    P_lh_A = P_lh_given_A(ages_of_death, study_year)
    P_right = 1 - P_left # either you're left-handed or right-handed, so P_right = 1 - P_left
    P_rh_A = 1 - P_lh_A # P_rh_A = 1 - P_lh_A 
    return P_rh_A*P_A/P_right


# ## 8. Plotting the distributions of conditional probabilities
# <p>Now that we have functions to calculate the probability of being age A at death given that you're left-handed or right-handed, let's plot these probabilities for a range of ages of death from 6 to 120. </p>
# <p>Notice that the left-handed distribution has a bump below age 70: of the pool of deceased people, left-handed people are more likely to be younger. </p>

# In[10]:


ages = np.arange(6, 116, 1) # make a list of ages of death to plot

# calculate the probability of being left- or right-handed for each 
left_handed_probability = P_A_given_lh(ages, death_distribution_data, 1990)
right_handed_probability = P_A_given_rh(ages, death_distribution_data, 1990)

# create a plot of the two probabilities vs. age
plt.plot(ages, left_handed_probability, label = "Left-handed")
plt.plot(ages, right_handed_probability, label = "Right-handed")
plt.legend() # add a legend
plt.title("Probability of dying at age A being left handed or right handed v/s Age")
plt.xlabel("Age")
plt.ylabel("Probability of dying at age A")
plt.show()


# ## 9. Moment of truth: age of left and right-handers at death
# <p>Finally, let's compare our results with the original study that found that left-handed people were nine years younger at death on average. We can do this by calculating the mean of these probability distributions in the same way we calculated P(LH) earlier, weighting the probability distribution by age and summing over the result.</p>
# <p>$$\text{Average age of left-handed people at death} = \sum_A A P(A | LH)$$</p>
# <p>$$\text{Average age of right-handed people at death} = \sum_A A P(A | RH)$$</p>

# In[11]:


# calculate average ages for left-handed and right-handed groups
# use np.array so that two arrays can be multiplied
average_lh_age =  np.nansum(ages*np.array(left_handed_probability))
average_rh_age =  np.nansum(ages*np.array(right_handed_probability))

# print the average ages for each group
# ... YOUR CODE FOR TASK 9 ...
print("Average age of death for left handed: ", average_lh_age)
print("Average age of death for right handed: ", average_rh_age)

# print the difference between the average ages
print("The difference in average ages is " + str(round(average_rh_age - average_lh_age, 1)) + " years.")


# ## 10. Final comments
# <p>We got a pretty big age gap between left-handed and right-handed people purely as a result of the changing rates of left-handedness in the population, which is good news for left-handers: you probably won't die young because of your sinisterness. The reported rates of left-handedness have increased from just 3% in the early 1900s to about 11% today, which means that older people are much more likely to be reported as right-handed than left-handed, and so looking at a sample of recently deceased people will have more old right-handers.</p>
# <p>Our number is still less than the 9-year gap measured in the study. It's possible that some of the approximations we made are the cause: </p>
# <ol>
# <li>We used death distribution data from almost ten years after the study (1999 instead of 1991), and we used death data from the entire United States instead of California alone (which was the original study). </li>
# <li>We extrapolated the left-handedness survey results to older and younger age groups, but it's possible our extrapolation wasn't close enough to the true rates for those ages. </li>
# </ol>
# <p>One thing we could do next is figure out how much variability we would expect to encounter in the age difference purely because of random sampling: if you take a smaller sample of recently deceased people and assign handedness with the probabilities of the survey, what does that distribution look like? How often would we encounter an age gap of nine years using the same data and assumptions? We won't do that here, but it's possible with this data and the tools of random sampling. </p>
# <!-- I did do this if we want to add more tasks - it would probably take three more blocks.-->
# <p>To finish off, let's calculate the age gap we'd expect if we did the study in 2018 instead of in 1990. The gap turns out to be much smaller since rates of left-handedness haven't increased for people born after about 1960. Both the National Geographic study and the 1990 study happened at a unique time - the rates of left-handedness had been changing across the lifetimes of most people alive, and the difference in handedness between old and young was at its most striking. </p>

# In[12]:


# Calculate the probability of being left- or right-handed for all ages
left_handed_probability_2018 = P_A_given_lh(ages, death_distribution_data, 2018)
right_handed_probability_2018 = P_A_given_rh(ages, death_distribution_data, 2018)

# create a plot of the two probabilities vs. age
plt.plot(ages, left_handed_probability_2018, label = "Left-handed")
plt.plot(ages, right_handed_probability_2018, label = "Right-handed")
plt.legend() # add a legend
plt.title("Probability of dying at age A being left handed or right handed v/s Age in 2018")
plt.xlabel("Age")
plt.ylabel("Probability of dying at age A")
plt.show()

# calculate average ages for left-handed and right-handed groups
average_lh_age_2018 = np.nansum(ages*np.array(left_handed_probability_2018))
average_rh_age_2018 = np.nansum(ages*np.array(right_handed_probability_2018))

print("Average age of death for left handed in 2018: ", average_lh_age_2018)
print("Average age of death for right handed in 2018: ", average_rh_age_2018)

print("The difference in average ages is " + 
      str(round(average_rh_age_2018 - average_lh_age_2018, 1)) + " years.")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




