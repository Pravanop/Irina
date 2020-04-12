import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sister
from scipy.spatial.distance import cosine
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article 

embedder=sister.MeanEmbedding(lang='en')

class Intent:
    threshold=0.7 #say
    def intent_builder(self,training_phrases):
        training_phrase=input("Enter a training phase:")
        sent_vector=embedder(training_phrase)
        sent_vector=np.array(sent_vector)
        sent_vector1=sent_vector.reshape(1,300)
        training_phrases1=np.vstack((training_phrases,sent_vector1))
        return training_phrases1
    
    def intent_searcher(self,testing_phrases,training_phrases):
        iteration_count=0
        for training_phrase in training_phrases:
            training_phrase=training_phrase.reshape(300,1)
            cosine_sim=1- cosine(training_phrase,testing_phrases)
            if iteration_count == 0:
                cosine_max=cosine_sim
            if (cosine_max<cosine_sim):
                cosine_max=cosine_sim
            iteration_count= iteration_count+1
        if (cosine_max>=self.threshold):
            return True,cosine_max
        else:
            return False,0

#given a list of intent objects(with function call as attribute). Training phrases already loaded.
def intent_matcher(intent_list,testing_phrase):
    
    count=0
    cosine_max=0
    intent_max=0
    vector_max=0
    
    for intent in intent_list:
        value,vector=intent.intent_searcher(testing_phrase,intent.training_phrases)
        if(value):
            vector_instance=vector
            count=count+1
            if (count==1):
                vector_max=vector_instance
                intent_max=intent
            elif (vector_max<vector_instance):
                vector_max=vector_instance
                intent_max=intent
        else: #value is false
            continue
        count=count+1
    return intent_max,vector_max

class Stocks(Intent):
    def training_phrase_adder_20(self,training_phrases):
        for phrase in range(5):
             training_phrases=Intent.intent_builder(self,training_phrases)
        return training_phrases
    def stock_price(self,company):
        driver = webdriver.Chrome('C:/Users/Sandesh Rangreji/Documents/React_sample/IRINA_bot/chromedriver.exe')
        driver.get("https://www.google.com") 
        import time 
        #time.sleep(1)
        search_bar = driver.find_element_by_name("q")
        search_bar.clear()
        search_bar.send_keys(company+' stock price')
        search_bar.submit()
        #time.sleep(1)
        price= driver.find_element_by_css_selector("span[jsname='vWLAgc']")
        percent=driver.find_element_by_css_selector("span[jsname='rfaVEf']")    
        reply ='The stock price is at '+ price.text + ' and ' + percent.text 
        driver.close()
        return reply

class News(Intent):
    def training_phrase_adder_20(self,training_phrases):
        for phrase in range(5):
             training_phrases=Intent.intent_builder(self,training_phrases)
        return training_phrases
    def generate_newsList(self):
        news_url="https://news.google.com/news/rss"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()
        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        return news_list
    def print_topNews(self):
        news_list=self.generate_newsList()
        # Print news title, url and publish date
        news_items=[]
        for news in news_list[:5]:
            #For different language newspaper refer above table 
            toi_article = Article(news.link.text, language="en") # en for English 
            news_item=''
            #To download the article 
            toi_article.download() 
            #To parse the article 
            toi_article.parse() 
            #To perform natural language processing ie..nlp 
            toi_article.nlp() 
            #To extract title 
            news_item="Article Title:"+'<br/>'
            news_item=news_item+toi_article.title + '<br/>'
            #To extract summary 
            news_item=news_item+"Article Summary:"+'<br/>'
            news_item=news_item+toi_article.summary + '<br/>'
            #To add link
            news_item=news_item+"Article Link:"+'<br/>'
            news_item=news_item+ news.link.text + '<br/><br/>'

            news_items.append(news_item)
        return news_items

#initialize functionality classes
def init_intents():
    stocks=Stocks()
    news=News()
    #Code to Store training phrases(Stocks)
    #training_phrases=stocks.training_phrase_adder_20(training_phrases)
    #stocks.training_phrases=training_phrases
    #np.save('stocks_training_phrases', stocks.training_phrases)

    stocks.training_phrases=np.load('stocks_training_phrases.npy')
    news.training_phrases=np.load('news_training_phrases.npy')
    
    intent_list=[stocks,news]

    return intent_list,stocks,news

def set_reply(query): 
    intent_list,stocks,news=init_intents()
    #query="What is the share price of google"
    testing_phrase=embedder(query)
    testing_phrase=testing_phrase.reshape(300,1)
    intent_max,vector_max=intent_matcher(intent_list,testing_phrase)
    if(intent_max==stocks):
        return(stocks.stock_price(query))
    elif(intent_max==news):
        news_items=news.print_topNews()
        reply=''
        for item in news_items:
            reply=reply+item+'\n'
        return(reply)
    else:
        return("I'm sorry,I can't help you with that.")


#print(set_reply("What's making the headlines today?"))