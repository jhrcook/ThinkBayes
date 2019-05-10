
'''
author: Joshua Cook
date: 2019-05-06

These are the classes Pmf and Suite used throughout *Think Bayes*
by Allen Downey

I am not frequent Python programmer, so I apologize for 
inconsistencies and straying from PEP8 and common style customs
'''

class Pmf:
    '''
    A class to define and maitain a probability mass function
    '''
    def __init__(self):
        self.hypotheses = dict()
    
    
    # sets the `hypo` to the probability `prob`
    def Set(self, hypo, prob):
        self.hypotheses[hypo] = prob
    
    
    # increments the object `hypo` by `n`
    # useful for building the PMF from an iterator
    def Incr(self, hypo, n):
        if obj in self.options.keys():
            self.hypotheses[hypo] += 1
        else:
            self.hypotheses[hypo] = 1
    
    
    # nromalize the PMF back to a sum of 1
    def Normalize(self):
        possible_hypos = sum(self.hypotheses.values())
        if possible_hypos > 0:
            for hypo in self.hypotheses.keys():
                self.hypotheses[hypo] = self.hypotheses[hypo] / possible_hypos
        else:
            print("No values set")
    
    
    # return the probability of hypothesis `hypo`
    def Prob(self, hypo):
        if obj in self.hypotheses.keys():
            print(self.hypotheses[hypo])
        else:
            print(hypo + "has not been set, yet")
    
    
    # multiply the current prob of object `hypo` by `new_p`
    def Mult(self, hypo, new_p):
        if hypo in self.hypotheses.keys():
            self.hypotheses[hypo] *= new_p
    
    
    # print statement
    def __str__(self):
        msg = ""
        for hypo in self.hypotheses.keys():
            msg = msg + str(hypo) + ': ' + str(self.hypotheses[hypo]) + '\n'
        return(msg)



class Suite(Pmf):
    '''
    Creating a Pmf for multiple hypotheses
    '''
    def __init__(self, hypos):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()
    
    
    # update the hypotheses using new data
    def Update(self, data):
        for hypo in self.hypotheses.keys():
            like = self.Liklihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()
        
    # a more efficient version of `Update()`
    def UpdateSet(self, dataset):
        for data in dataset:
            for hypo in self.hypotheses.values():
                like = self.Liklihood(data, hypo)
                self.Mult(hypo, like)
        return self.Normalize()