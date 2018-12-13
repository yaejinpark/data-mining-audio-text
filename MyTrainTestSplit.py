def my_train_test_split(test_size=0.3):

    # Import modules
    import csv
    import random

    # Declare needed variables
    data = []
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    category_count = 7
    category_item_count = 85
    test_percentage = test_size
    test_item_count_per_category = int(category_item_count * test_percentage)

    # Get data from csv file
    with open('data.csv', 'r') as raw_data:
        data_reader = csv.reader(raw_data, delimiter=',')
        data = list(data_reader)

    # Get indexes of all test items
    start_idx = 0
    end_idx = category_item_count
    test_idxs = []
    for i in range(category_count):
        for j in random.sample(range(start_idx, end_idx), test_item_count_per_category):
            test_idxs.append(j)
        start_idx += category_item_count
        end_idx += category_item_count

    # Extract train and test data from raw data
    for idx,row in enumerate(data):
        if idx in test_idxs:
            x_test.append(row[1])
            y_test.append(row[0])
        else:
            x_train.append(row[1])
            y_train.append(row[0])

    # Return split data
    return x_train, x_test, y_train, y_test

# Run as standalone script
if __name__ == "__main__":
    x_train, x_test, y_train, y_test = my_train_test_split()
    print("TRAIN: Feature list")
    print(x_train)
    print("TRAIN: Label list")
    print(y_train)
    print("TEST: Feature list")
    print(x_test)
    print("TEST: Label list")
    print(y_test)