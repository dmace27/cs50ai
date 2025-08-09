import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # opens and reads the csv file
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        labels = []
        evidence = []

        for row in csv_reader:
            # creates a list for each row and adds each value to the list
            row_evidence = []
            
            # converts a month input to a number input
            for i in range(17):
                if i == 10:
                    if row[i][0:3].lower() == "jan":
                        row_evidence.append(0)
                    elif row[i][0:3].lower() == "feb":
                        row_evidence.append(1)
                    elif row[i][0:3].lower() == "mar":
                        row_evidence.append(2)
                    elif row[i][0:3].lower() == "apr":
                        row_evidence.append(3)
                    elif row[i][0:3].lower() == "may":
                        row_evidence.append(4)
                    elif row[i][0:3].lower() == "jun":
                        row_evidence.append(5)
                    elif row[i][0:3].lower() == "jul":
                        row_evidence.append(6)
                    elif row[i][0:3].lower() == "aug":
                        row_evidence.append(7)
                    elif row[i][0:3].lower() == "sep":
                        row_evidence.append(8)
                    elif row[i][0:3].lower() == "oct":
                        row_evidence.append(9)
                    elif row[i][0:3].lower() == "nov":
                        row_evidence.append(10)
                    elif row[i][0:3].lower() == "dec":
                        row_evidence.append(11)

                # converts visitor type to a number input 
                elif i == 15:
                    if row[i][0] == "N":
                        row_evidence.append(0)
                    else:
                        row_evidence.append(1)
                # covnerts the week status to a number input
                elif i == 16:
                    if row[i] == True:
                        row_evidence.append(1)
                    else:
                        row_evidence.append(0)
                # handling ints and floats from the csv
                elif i in {0, 2, 4, 11, 12, 13, 14}:
                    row_evidence.append(int(row[i]))
                elif i in {1, 3, 5, 6, 7, 8, 9}:
                    row_evidence.append(float(row[i]))

            # adding each row of evidence to the total evidence   
            evidence.append(row_evidence)
            
            # adding the row label to the list of labels
            if row[17] == True:
                labels.append(1)
            else:
                labels.append(0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # creates the model and then fits the model with the data
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    total_positive = 0
    total_negative = 0
    positive_correct = 0
    negative_correct = 0

    for i in range(len(labels)):
        # totaling the amount correct positives and total positives
        if labels[i] == 1:
            total_positive += 1
            if labels[i] == predictions[i]:
                positive_correct += 1
        # totaling the amount correct negatives and total negatives
        else:
            total_negative += 1
            if labels[i] == predictions[i]:
                negative_correct += 1

    # calculating sensitivity and specificity
    sensitivity = positive_correct / total_positive
    specificity = negative_correct / total_negative

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
