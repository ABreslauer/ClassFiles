#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


# In[2]:


from nltk import sent_tokenize
import string

# Read and split into phrases
with open('party.txt') as file:
    text = file.read()
    
phrases = sent_tokenize(text)

print(phrases)


# In[3]:


from nltk import word_tokenize

tag_list = []
for i in phrases:
    words = word_tokenize(i)
    word_tags = nltk.pos_tag(words)
    tags = []
    for j in word_tags:
        tags.append(j[1])
    tag_list.append(tags)


# In[4]:


import re

searches = []
for i in tag_list:
    sentence = ' '.join(i)
    search = re.findall('.*?NNP.*?V..?.*?NNP',sentence)
    if search:
        print(search[0])
        searches.append(search[0])
    else:
        searches.append("")


# In[5]:


# This is some of the ugliest garbage i've ever written but it works
joined_phrases = []
for i in range(len(phrases)):
    print(searches[i])
    split_searches = searches[i].split()
    length = len(searches[i].split())
    
    if length > 0:
        print("Length:",length)
        phrase = phrases[i]
        split = phrase.split()
        print(' '.join(split[0:length]))
        joined_phrase_list = []
        for j in range(length):
            joined_phrase_list.append((split[j],split_searches[j]))
        print(joined_phrase_list)
        joined_phrases.append(joined_phrase_list)
        print("\n")
        
for i in joined_phrases:
    print(i)


# In[6]:


from nltk.stem import PorterStemmer

people = []
triples = []

ps = PorterStemmer()
knows_words = ['talk','ask','speak','spoke','danc','visit']
for sentence in joined_phrases:
    for word_pair in sentence:
        if re.match('V..?',word_pair[1]):
            if ps.stem(word_pair[0]) in knows_words:
                temp_people=[]
                for i in sentence:
                    if i[1] == 'NNP':
                        no_period_string = re.sub('\.','',i[0])
                        temp_people.append(no_period_string)
                        people.append(no_period_string)
                triples.append((temp_people[0], word_pair[0], temp_people[1]))

people = list(set(people))
print("People:",people)
for i in triples:
    print(i)


# In[7]:


with open("mydata.n3",'w') as outfile:
    outfile.write("""@prefix :  <http://www.lyle.smu.edu//#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix schema: <http://schema.org/> .\n\n""")
    for i in people:
        outstring = ":" + i + " rdf:type schema:Person .\n"
        outfile.write(outstring)
    outfile.write("\n")
    for i in triples:
        outstring = ":" + i[0] + " schema:knows :" + i[2] + " .\n"
        outfile.write(outstring)
        # outstring = ":" + i[2] + " schema:knows :" + i[0] + " .\n"
        # outfile.write(outstring)


# In[ ]:




