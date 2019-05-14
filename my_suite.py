
'''
author: Joshua Cook
date: 2019-05-06

These are the classes Pmf and Suite used throughout *Think Bayes*
by Allen Downey

I am not frequent Python programmer, so I apologize for 
inconsistencies and straying from PEP8 and common style customs
'''

from numpy.random import choice

class Pmf:
    '''
    A class to define and maitain a probability mass function
    '''
    def __init__(self):
        self.hypotheses = dict()
    

    def Set(self, hypo, prob):
        '''
        sets the `hypo` to the probability `prob`
        '''
        self.hypotheses[hypo] = prob
    
    
    def Incr(self, hypo, n):
        '''
        increments the object `hypo` by `n`
        useful for building the PMF from an iterator
        '''
        if obj in self.options.keys():
            self.hypotheses[hypo] += 1
        else:
            self.hypotheses[hypo] = 1
    
    
    def Normalize(self):
        '''
        normalize the PMF back to a sum of 1
        '''
        possible_hypos = sum(self.hypotheses.values())
        if possible_hypos > 0:
            for hypo in self.hypotheses.keys():
                self.hypotheses[hypo] = self.hypotheses[hypo] / possible_hypos
        else:
            print("No values set")
    
    
    def Prob(self, hypo):
        '''
        return the probability of hypothesis `hypo`
        '''
        if obj in self.hypotheses.keys():
            print(self.hypotheses[hypo])
        else:
            print(hypo + "has not been set, yet")
    
    
    def Mult(self, hypo, new_p):
        '''
        multiply the current prob of object `hypo` by `new_p`
        '''
        if hypo in self.hypotheses.keys():
            self.hypotheses[hypo] *= new_p
    
    
    def __str__(self):
        msg = ""
        for hypo in self.hypotheses.keys():
            msg = msg + str(hypo) + ': ' + str(self.hypotheses[hypo]) + '\n'
        return(msg)

    
    def MaximumLiklihood(self):
        '''
        Calculates the maximum liklihood of the posterior prob of a Suite object
        '''
        prob, val = max((prob, val) for val, prob in self.hypotheses.items())
        return val
    
    
    def Mean(self):
        '''
        Calculates the mean of the posterior prob of a Suite object
        '''
        avg = sum(prob * val for val, prob in self.hypotheses.items())
        return avg


    def Percentile(self, percentage):
        '''
        Calculates the percentile of the posterior distribution
        '''
        p = percentage / 100.0
        total = 0
        for val, prob in self.hypotheses.items():
            total += prob
            if total >= p:
                return val
    
    def Random(self, n=1):
        '''
        Returns a random hypothesis from the hypotheses
        weighed by the probability of the hypothesis
        '''
        return choice(list(self.hypotheses.keys()), p=list(self.hypotheses.values()))
    


class Suite(Pmf):
    '''
    Creating a Pmf for multiple hypotheses
    '''
    def __init__(self, hypos):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()
    

    def Update(self, data):
        '''
        update the hypotheses using new data
        '''
        for hypo in self.hypotheses.keys():
            like = self.Liklihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()
        
    
    def UpdateSet(self, dataset):
        '''
        a more efficient version of `Update()`
        '''
        for data in dataset:
            for hypo in self.hypotheses.values():
                like = self.Liklihood(data, hypo)
                self.Mult(hypo, like)
        return self.Normalize()