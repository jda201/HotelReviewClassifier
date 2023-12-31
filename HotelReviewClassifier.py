import pandas as pd
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Specify the dataset file directly
dataset_file = 'tripadvisor_hotel_reviews.csv'

print('start processing data')
# Data Processing
input_data = pd.read_csv(dataset_file)
input_data['overall'] = input_data['overall'].astype(object)  # fix datatype error
input_data['reviewText'] = input_data['reviewText'].astype(object)  # fix datatype error

dataset = {'reviewText': input_data['reviewText'], 'overall': input_data['overall']}
dataset = pd.DataFrame(data=dataset)
dataset = dataset.dropna()  # ignore if any row contained NaN
dataset = dataset[dataset['overall'] != '3']
dataset['label'] = dataset['overall'].apply(lambda rating: +1 if str(rating) > '3' else -1)

# Splitting data into training set and testing set
X = pd.DataFrame(dataset, columns=['reviewText'])
y = pd.DataFrame(dataset, columns=['label'])
train_X, test_X, train_y, test_y = train_test_split(X, y, random_state=50)

# Bag of Words model
vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
train_vector = vectorizer.fit_transform(train_X['reviewText'])
test_vector = vectorizer.transform(test_X['reviewText'])
print('processing ... ok')
print('start training model')

# LogisticRegression model for classification problems
clr = LogisticRegression()
clr.fit(train_vector, train_y.values.ravel())
scores = clr.score(test_vector, test_y)  # accuracy
print('training ...ok')
print('accuracy: {}%'.format(scores * 100))

# Predicting new reviews
new_reviews = [
    "This hotel is amazing! Great service and comfortable rooms.",
    "Terrible experience. I wouldn't recommend this hotel to anyone."
]

# Vectorize the new reviews
new_reviews_vector = vectorizer.transform(new_reviews)

# Make predictions
predictions = clr.predict(new_reviews_vector)

# Display predictions
for review, prediction in zip(new_reviews, predictions):
    sentiment = "Positive" if prediction == 1 else "Negative"
    print(f"Review: {review}")
    print(f"Sentiment: {sentiment}\n")
