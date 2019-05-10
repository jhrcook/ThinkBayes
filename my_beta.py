class Beta(object):
    '''
    A beta distribution for Bayes Thrm calculations
    '''
    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta
    
    
    # update the posterior distribution based on the number of 
    # Heads and Tails seen from the data
    def Update(self, data):
        heads, tails = data
        self.alpha += heads
        self.beta += tails
    
    
    # calculate the mean of the distribution
    def Mean(self):
        return float(self.alpha) / (self.alpha + self.beta)
    
    
    # evalute the PDF of the distribution
    def EvalPdf(self, x):
        return x**(self.alpha-1) * (1-x)**(self.beta-1)