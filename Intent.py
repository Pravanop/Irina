import numpy as np
import sister
embedder=sister.MeanEmbedding(lang='en')
from scipy.spatial.distance import cosine
class Intent:
    threshold=0.7 #say
    
    def intent_searcher(self,testing_phrases,training_phrases):
        iteration_count=0
        for training_phrase in training_phrases:
            training_phrase=training_phrase.reshape(300,1)
            cosine_sim=1- cosine(training_phrase,testing_phrase)
            if iteration_count == 0:
                cosine_max=cosine_sim
            if (cosine_max<cosine_sim):
                cosine_max=cosine_sim
            iteration_count= iteration_count+1
        if (cosine_max>=self.threshold):
            return True,cosine_max
        else:
            return False,0
            
