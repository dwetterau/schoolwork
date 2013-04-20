import util
import classificationMethod
import naiveBayes
import mira

class contestClassifier(classificationMethod.ClassificationMethod):
  """
  Create any sort of classifier you want. You might copy over one of your
  existing classifiers and improve it.
  """
  def __init__(self, legalLabels):
    self.guess = None
    self.type = "minicontest"
    self.classifier = naiveBayes.NaiveBayesClassifier(legalLabels)
    #self.classifier = mira.MiraClassifier(legalLabels, 5)
    self.classifier.automaticTuning = True

  def train(self, data, labels, validationData, validationLabels):
    """
    Please describe your training procedure here.
    """
    self.classifier.train(data, labels, validationData, validationLabels)
  
  def classify(self, testData):
    """
    Please describe how data is classified here.
    """
    return self.classifier.classify(testData)
