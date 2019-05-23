
'''
author: Joshua Cook
date: 2019-05-06

These are the classes Pmf and Suite used throughout *Think Bayes*
by Allen Downey

I am not frequent Python programmer, so I apologize for 
inconsistencies and straying from PEP8 and common style customs
'''

from numpy.random import choice


'''
Functions used by the classes defined below
'''

def MakePmfFromCdf(cdf):
    """Makes a normalized Pmf from a Cdf object.
    Args:
        cdf: Cdf object
    Returns:
        Pmf object
    """
    pmf = Pmf()

    prev = 0.0
    for val, prob in cdf.Items():
        pmf.Incr(val, prob - prev)
        prev = prob
    return pmf


def MakeCdfFromItems(items):
    """Makes a cdf from an unsorted sequence of (value, frequency) pairs.
    Args:
        items: unsorted sequence of (value, frequency) pairs
    Returns:
        cdf: list of (value, fraction) pairs
    """
    runsum = 0
    hyps = {}

    for value, count in sorted(items):
        runsum += count
        hyps[value] = runsum

    total = float(runsum)
    hyps = {x: c / total for x,c in hyps.items()}

    cdf = Cdf(hyps.keys(), hyps.values())
    return cdf


def MakeCdfFromPmf(pmf):
    """Makes a CDF from a Pmf object.
    Args:
       pmf: Pmf.Pmf object
    Returns:
        Cdf object
    """
    return MakeCdfFromItems(pmf.Items())


def MakeMixture(pmf_dice):
    ''' Calculates the PMF for a mixture of dice
    Args:
        pmf_dice: a pmf filled with Die() pmfs
    Returns:
        a Pmf object
    '''
    mix = Pmf()
    for die, weight in pmf_dice.Items():
        for outcome, prob in die.Items():
            mix.Incr(outcome, weight * prob)
    return mix


'''
New classes
'''

class Pmf:
    '''
    A class to define and maitain a probability mass function
    '''
    def __init__(self):
        self.hypotheses = dict()
    
    
    def Items(self):
        '''
        Wrapper for dict.items()
        '''
        return self.hypotheses.items()
    
    def Values(self):
        '''
        Wrapper for dict.values()
        '''
        return self.hypotheses.values()
    
    def Keys(self):
        '''
        Wrapper for dict.keys()
        '''
        return self.hypotheses.keys()
    
    
    def Set(self, hypo, prob):
        '''
        sets the `hypo` to the probability `prob`
        '''
        self.hypotheses[hypo] = prob
    
    
    def Incr(self, hypo, n=1):
        '''
        increments the object `hypo` by `n`
        useful for building the PMF from an iterator
        '''
        if hypo in self.hypotheses.keys():
            self.hypotheses[hypo] += n
        else:
            self.hypotheses[hypo] = n
    
    
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
    
    
    def MakeCdf(self):
        """Makes a Cdf."""
        return MakeCdfFromPmf(self)
    
    
    def Max(self, k):
        """Computes the CDF of the maximum of k selections from this dist.
        k: int
        returns: new Cdf
        """
        cdf = self.MakeCdf()
        return cdf.Max(k)
    
    
    def Random(self, n=1):
        '''
        Returns a random hypothesis from the hypotheses
        weighed by the probability of the hypothesis
        '''
        return choice(list(self.hypotheses.keys()), p=list(self.hypotheses.values()))
    
    
    def __add__(self, other):
        '''
        Sum two Pmf objects
        Enumerate all possibilities, add calculate the sum and probability of each
        '''
        pmf = Pmf()
        for v1, p1 in self.hypotheses.items():
            for v2, p2 in other.hypotheses.items():
                pmf.Incr(v1+v2, p1*p2)
        return pmf
    


class Cdf:
    '''
    CDF for a set of hypotheses, and probabilities
    '''
    def __init__(self, xs=None, ps=None):
        self.hypotheses = {}
        for x, p in zip(xs, ps):
            self.hypotheses[x] = p

    
    def Items(self):
        '''
        Wrapper for dict.items()
        '''
        return self.hypotheses.items()
    
    
    def Values(self):
        '''
        Wrapper for dict.values()
        '''
        return self.hypotheses.values()
    
    
    def Keys(self):
        '''
        Wrapper for dict.keys()
        '''
        return self.hypotheses.keys()
            
            
    def Copy(self):
        """
        Returns a copy of this Cdf.
        """
        return Cdf(list(self.hypotheses.keys()), list(self.hypotheses.values()))

    def MakePmf(self):
        """Makes a Pmf."""
        return MakePmfFromCdf(self)

    def Values(self):
        """Returns a sorted list of values.
        """
        return self.hypotheses.values()

    def Items(self):
        """Returns a sorted sequence of (value, probability) pairs.
        Note: in Python3, returns an iterator.
        """
        return self.hypotheses.items()

    def Append(self, x, p):
        """Add an (x, p) pair to the end of this CDF.
        Note: this us normally used to build a CDF from scratch, not
        to modify existing CDFs.  It is up to the caller to make sure
        that the result is a legal CDF.
        """
        self.hypotheses[x] = p
    
    def Max(self, k):
        cdf = self.Copy()
        for x, p in cdf.hypotheses.items():
            cdf.hypotheses[x] = p**k
        return cdf
    
    

    
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