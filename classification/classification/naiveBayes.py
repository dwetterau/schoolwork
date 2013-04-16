import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    "*** YOUR CODE HERE ***"
    self.distribution = None
    self.label_counts = util.Counter()
    for i in range(len(trainingData)):
        self.label_counts[trainingLabels[i]] += 1

    datapoints = len(trainingData)
    best_distribution = None
    min = 2000000000
    kgrid.sort()
    
    all_distributions = util.Counter()
    for k in kgrid:
        distribution = util.Counter()
        for label in self.legalLabels:
            label_counts = util.Counter()
            for feature in self.features:
                label_counts[feature] = util.Counter()
                label_counts[feature][1] = k
                label_counts[feature][0] = k
                distribution[label] = label_counts
        all_distributions[k] = distribution
    for i in range(len(trainingData)):
        for feature in trainingData[i]:
            for k in kgrid:
                all_distributions[k][trainingLabels[i]][feature][1] += trainingData[i][feature] 
                all_distributions[k][trainingLabels[i]][feature][0] += 1 - trainingData[i][feature] 
    for label in self.legalLabels:
        for k in all_distributions:
            for entry in all_distributions[k][label]:
                denom = all_distributions[k][label][entry][0] + all_distributions[k][label][entry][1] 
                all_distributions[k][label][entry][1] /= float(denom)
                all_distributions[k][label][entry][0] /= float(denom)
    
    for k in all_distributions:
        self.distribution = all_distributions[k]
        guesses = self.classify(validationData)
        wrong = 0
        for i in range(len(trainingLabels)):
            if not guesses[i] == trainingLabels[i]:
                wrong += 1
        if wrong < min:
            min = wrong
            best_distribution = self.distribution
    self.distribution = best_distribution
        

  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
    sum = 0
    for i in self.label_counts:
        sum += self.label_counts[i]
    for label in self.legalLabels:
        total = math.log(float(self.label_counts[label])/sum)
        for feature in datum:
            val = self.distribution[label][feature][datum[feature]]
            total += math.log(val)
        logJoint[label] = total
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    """
    featuresOdds = []
        
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds
    

    
      
