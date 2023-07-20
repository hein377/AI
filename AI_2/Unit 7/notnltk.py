from __future__ import division
from pydoc import doc
from sre_parse import CATEGORIES
from tkinter import W
import nltk, re, pprint
from nltk import word_tokenize
from nltk.book import *
from nltk.corpus import *
from nltk.corpus import wordnet as wn
from nltk.corpus import movie_reviews
import matplotlib.pylab as plt
import math
import random
from urllib import request
from bs4 import BeautifulSoup


ALPHA = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

'''
#Chapter2

#Q4
files = state_union.fileids()
modals = {"men":0, "women":0, "people":0}
for f in files:
    fdist = nltk.FreqDist(w.lower() for w in state_union.words(f))
    for m in modals: modals[m] += fdist[m]
for m in modals:
    print(f"{m}: {modals[m]}", end = "  ")

cfd = nltk.ConditionalFreqDist(
    (target, fileid[:4])
    for fileid in state_union.fileids()
    for word in state_union.words(fileid)
    for target in ["men", "women", "people"]
    if word.lower() in target)
cfd.plot()

#Q5
nouns = ["cows", "shelf", "water"]
for n in nouns:
    print(wn.synset(f"{n}.n.01").part_meronyms())
    print(wn.synset(f"{n}.n.01").substance_meronyms())
    print(wn.synset(f"{n}.n.01").member_meronyms())
    print(wn.synset(f"{n}.n.01").part_holonyms())
    print(wn.synset(f"{n}.n.01").substance_holonyms())
    print(wn.synset(f"{n}.n.01").member_holonyms())
    print()

#Q7
emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))
persuasion = nltk.Text(nltk.corpus.gutenberg.words('austen-persuasion.txt'))
sense = nltk.Text(nltk.corpus.gutenberg.words('austen-sense.txt'))
print(emma.concordance("however"))
print(persuasion.concordance("however"))
print(sense.concordance("however"))

#Q9
def process(genre, word):                             #genre1 = religion, genre2 = romance
    print(f"Genre: {genre}")
    text = brown.words(categories = genre)
    lexical_div = len(set(text)) / len(text)
    fdist = FreqDist(text)
    print(f"Lexical_diversity: {lexical_div}")
    print(f"Top 100 most common words: {fdist.most_common(100)}", end="\n\n")
    print(text.common_contexts("word"))
process("religion")
process("romance")

#Q12
w = cm.words()
s = set(w)
print(len(s))
print(((len(w)-len(s))/len(w)).as_integer_ratio())
'''

def isword(word):
    for c in list(word):
        if c not in ALPHA: return False
    return True

'''
#Q17
def fifty_most_common_words(text):                  #text = list of strings
    fdist, stpwords = FreqDist(text), stopwords.words('english')
    ls = fdist.most_common(700)
    most_common, i = [], 0
    while len(most_common) < 50:
        word, freq = ls[i]
        if(word not in stpwords and isword(word)): most_common.append(word)
        i += 1
    return most_common
print(fifty_most_common_words(brown.words(categories = "news")))

#Q18
def fifty_most_common_bigrams(text):                #text = list of strings
    fdist, stpwords = FreqDist(nltk.bigrams(text)), stopwords.words('english')
    ls = fdist.most_common(1500)
    most_common, i = [], 0
    while len(most_common) < 50:
        words, freq = ls[i]
        word1, word2 = words
        if(word1 not in stpwords and word2 not in stpwords and isword(word1) and isword(word2)): most_common.append((word1, word2))
        i += 1
    return most_common
print(fifty_most_common_bigrams(brown.words(categories = "news")))

#Q23
def zipfs_law(text, n):
    fdist = FreqDist(text)
    ls = fdist.most_common(1500)
    words, freqs, word_rank, i = fdist.keys(), [], [], 0
    while(len(freqs) < n):
        word, freq = ls[i]
        if(isword(word)):
            freqs.append(freq)
            word_rank.append(math.log(freq))
            #word_rank.append(freq)
        i += 1
    plt.bar(word_rank, freqs, tick_label = word_rank.reverse(), width = (word_rank[-1]-word_rank[0])/n, color = ["blue", "green"])
    plt.xlabel('Word Rank')
    plt.ylabel('Frequencies')
    plt.title("Word_Freq")
    plt.show()
#zipfs_law(brown.words(categories = "news"), 50)

def create_random_string(n):
    s = ""
    for i in range(n): s += random.choice("abcdefg ")
    return s
zipfs_law(create_random_string(50000).split(" "), 50)

#Q27
#synset:                 Synset('entity.n.01')
#synset.name():          entity.n.01
#synset.lemma_names():   ['entity']
#synset.lemmas():        [Lemma('entity.n.01.entity')]

def polysemy(wordtype):
    n, count = 0, 0
    for synset in wn.all_synsets(wordtype):
        for name in synset.lemma_names():
            n += len(wn.synsets(name, wordtype))
            count += 1

    return n/count

wordtypes = ['n', 'v', 'a', 'r']                #'n' = nouns, 'v' = verbs, 'a' = adjectives, 'r' = adverbs
for wordtype in wordtypes:
    print(f"{wordtype}: {polysemy(wordtype)}")

#Chapter3

#20
url = "https://lms.fcps.edu/"
html = request.urlopen(url).read().decode('utf8')

raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print(tokens)
'''
rawtxt = open("rawtxt.txt", "w")
rawparsed = open("rawparsed.txt", "w")
token = open("token.txt", "w")

#22
def extract(url):
    html = request.urlopen(url).read().decode('utf8')
    extract = re.findall(r'[a-z]+', html)
    raws = [x for x in extract[:150] if x not in nltk.corpus.words.words()]
    print(raws)

extract("http://news.bbc.co.uk/")

'''
#4
from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
    for category in movie_reviews.categories()
    for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(words)[:1000]

def document_features(document):
    document_words, features = set(document), {}
    for word in word_features: features['contains({})'.format(word)] = (word in document_words)
    return features

featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))
print(classifier.show_most_informative_features(30))
'''

'''
◑ Examine the results of processing the URL http://news.bbc.co.uk/ using the regular expressions suggested above. You will see that there 
is still a fair amount of non-textual data there, particularly Javascript commands. You may also find that sentence breaks have not been 
properly preserved. Define further regular expressions that improve the extraction of text from this web page.

☼ Using the movie review document classifier discussed in this chapter, generate a list of the 30 features that the classifier finds to be
 most informative. Can you explain why these particular features are informative? Do you find any of them surprising?

For BLUE credit:
2) In Chapter 2, complete exercises 4, 5, 7, 9, 12, 17, 18, 23, and 27.
3) In Chapter 3, complete exercises 20 and 22.
4) In Chapter 6, complete exercise 4.
5) Judiciously truncate any long output (ie, just copy/paste the first and last few outputs with a “...” in between)

For RED and BLACK credits I did:
 Chapter 2, questions 26, 27, and 28
 Chapter 4, questions 27, 30, and 33 (one new chapter)
 Chapter 8, questions 29, 30, 33, and 35 (a second new chapter)
and put all of your answers into a document.
'''