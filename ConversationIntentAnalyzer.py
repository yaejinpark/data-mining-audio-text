# Import modules
import MyTrainTestSplit as mtts
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Conversation intent analyzer class
class ConversationIntentAnalyzer:

    # Constructor
    def __init__(self):

        # Classification categories
        self.categories = ['1:Small talk', '2:Compliment', '2:High risk factor', '4:Legal issue', '3:Information gathering', '4:Romance', '5:Explicit']

        # Train and test variables
        self.x_train = []   # train features
        self.y_train = []   # train labels
        self.x_test = []    # test features
        self.y_test = []    # test labels

        # Pipeline objects
        self.count_vect = CountVectorizer()     # classifies based on word count
        self.tfidf_trans = TfidfTransformer()   # classifies based on term frequency
        self.clf = MultinomialNB()              # classifier

        # Call setup() method so don't have to call it manually
        self.setup()

    # Method: Set up pipeline and train model
    def setup(self):

        # Split data into train & test
        self.x_train, self.x_test, self.y_train, self.y_test = mtts.my_train_test_split(test_size=0.3)

        # Feature extraction (learn vocab dict and return doc-term matrix for algorithm to understand)
        x_train_cv = self.count_vect.fit_transform(self.x_train)

        # Perform TF-IDF on data (further classify phrases with term frequency weight)
        x_train_tfidf = self.tfidf_trans.fit_transform(x_train_cv)

        # Use classifier to train model
        self.clf.fit(x_train_tfidf, self.y_train)

    # Method: Classify test data and report accuracy score
    def prediction(self, x_test=[], y_test=[]):

        # Check parameters for method output
        print_accuracy_score = True
        if x_test and not y_test:
            print_accuracy_score = False
        elif not x_test and not y_test:
            x_test = self.x_test
            y_test = self.y_test
        elif not x_test and y_test:
            return

        # Transform test data so that it's readable by algorithm
        x_test_cv = self.count_vect.transform(x_test)
        x_test_tfidf = self.tfidf_trans.transform(x_test_cv)

        # Perform predictions using transformed test data
        result = self.clf.predict(x_test_tfidf)

        # Display prediction results
        for doc, category in zip(x_test, result):
            print("%r => %s" % (doc, self.categories[int(category)]))

        # Print accuracy of result
        if print_accuracy_score:
            accuracy = accuracy_score(y_test, result)
            print("\n\nAccuracy score: " + str(accuracy) + "\n\n")
        
# Determine module operation
if __name__ == "__main__":

    # Create an instance of analyzer class and run with default split test data
    analyzer = ConversationIntentAnalyzer()
    analyzer.prediction()