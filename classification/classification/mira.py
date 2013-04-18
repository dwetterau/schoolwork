# Mira implementation
import util
PRINT = True

class MiraClassifier:
  """
  Mira classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mira"
    self.automaticTuning = False 
    self.C = 0.001
    self.legalLabels = legalLabels
    self.max_iterations = max_iterations
    self.initializeWeightsToZero()

  def initializeWeightsToZero(self):
    "Resets the weights of each label to zero vectors" 
    self.weights = {}
    for label in self.legalLabels:
      self.weights[label] = util.Counter() # this is the data-structure you should use
  
  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    "Outside shell to call your method. Do not modify this method."  
      
    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        Cgrid = [0.002, 0.004, 0.008]
    else:
        Cgrid = [self.C]
        
    return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
    """
    This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid, 
    then store the weights that give the best accuracy on the validationData.
    
    Use the provided self.weights[label] data structure so that 
    the classify method works correctly. Also, recall that a
    datum is a counter from features to values for those features
    representing a vector of values.
    """
    "*** YOUR CODE HERE ***"
    print self.legalLabels
    self.features = trainingData[0].keys() # could be useful later
    allWeights = util.Counter()
    Cgrid.sort()
    for c in Cgrid: 
        allWeights[c] = util.Counter()
        for label in self.legalLabels:
            allWeights[c][label] = util.Counter()
        for iteration in range(self.max_iterations):
            for i in range(len(trainingData)):
                max = -2000000000
                quess = None
                for label in self.legalLabels:
                    sum = trainingData[i] * allWeights[c][label]
                    if sum > max:
                        max = sum
                        guess = label
                if not guess == trainingLabels[i]:
                    # Calculate tau
                    tau = min(c, ((allWeights[c][guess]-allWeights[c][trainingLabels[i]])*trainingData[i] + 1)/(2.0*abs(trainingData[i]*trainingData[i])))
                    for feature in self.features:
                        allWeights[c][guess][feature] -= trainingData[i][feature]*tau
                        allWeights[c][trainingLabels[i]][feature] += trainingData[i][feature]*tau
    least_wrong = 2000000000
    best_weights = None
    for c in Cgrid:
        self.weights = allWeights[c]
        guesses = self.classify(validationData)
        wrong = 0
        for i in range(len(guesses)):
            if not guesses[i] == validationLabels[i]:
                wrong += 1
        if wrong < least_wrong:
            best_weights = allWeights[c]
            least_wrong = wrong
    self.weights = best_weights

  def classify(self, data ):
    """
    Classifies each datum as the label that most closely matches the prototype vector
    for that label.  See the project description for details.
    
    Recall that a datum is a util.counter... 
    """
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        vectors[l] = self.weights[l] * datum
      guesses.append(vectors.argMax())
    return guesses

  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns a list of the 100 features with the greatest difference in feature values
                     w_label1 - w_label2

    """
    featuresOdds = []

    "*** YOUR CODE HERE ***"

    return featuresOdds

