import logging

import matplotlib.pyplot as plt
import pandas as pd
from keras import regularizers
from keras.layers import Dense, LSTM
from keras.layers.embeddings import Embedding
from keras.models import Sequential
from keras.models import load_model
from keras.optimizers import Adam
from keras.preprocessing import sequence
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split

from classifier.data_set_constants import *
from classifier.utils import tokenize_corpus, build_dictionary, transform_to_dictionary_values, \
    transform_class_to_one_hot_representation, get_calculated_user_profile

logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s', level=logging.INFO)
data_frame = pd.read_csv("../../../data-set/final-data-set.csv")
data_set = data_frame.values

# for id, tweet in enumerate(data_set[:, :]):
#     print(id, tweet[-1])

# for index, tweet in enumerate(data_frame.text):
#     print(index, tweet)

logging.info("Tokenizing the corpus")
corpus_token = tokenize_corpus(data_set[:, DATA_SET_TEXT])

logging.info("Building the dictionary")
dictionary = build_dictionary(corpus_token)

# to get sentence back
# ' '.join([list(dictionary.keys())[i-2] for i in x_test[0] if i > 1])

logging.info("Transforming the corpus to dictionary values")
x_corpus = transform_to_dictionary_values(corpus_token, dictionary)

y_corpus = transform_class_to_one_hot_representation(data_set[:, DATA_SET_CLASS])
user_profile = get_calculated_user_profile(data_set[:, DATA_SET_USER_ID], data_set[:, DATA_SET_CLASS])

# padding with zeros if not enough and else drop left words
x_corpus = sequence.pad_sequences(x_corpus, maxlen=MAX_WORD_COUNT)

# shuffling data for 5-fold cross validation
k_fold = StratifiedKFold(n_splits=5, shuffle=True, random_state=18)
# to split raw format (integer) is required
y_corpus_raw = [0 if cls[2] == 1 else (1 if cls[1] == 1 else 2) for cls in y_corpus]

for train_n_validation_indexes, test_indexes in k_fold.split(x_corpus, y_corpus_raw):
    x_train_n_validation = x_corpus[train_n_validation_indexes]
    y_train_n_validation = y_corpus[train_n_validation_indexes]
    x_test = x_corpus[test_indexes]
    y_test = y_corpus[test_indexes]

    # train and validation data sets
    x_train, x_valid, y_train, y_valid = train_test_split(x_train_n_validation, y_train_n_validation, test_size=0.12,
                                                          random_state=94)

    # create the model
    model = Sequential()
    model.add(Embedding(input_dim=6000, output_dim=50, input_length=MAX_WORD_COUNT))
    model.add(LSTM(300))
    model.add(Dense(units=50, activation='relu', W_regularizer=regularizers.l2(0.09)))
    model.add(Dense(3, activation='softmax', W_regularizer=regularizers.l2(0.02)))
    adam_optimizer = Adam(lr=0.0001)
    model.compile(loss='categorical_crossentropy', optimizer=adam_optimizer, metrics=['accuracy'])

    print(model.summary())

    best_accuracy = 0
    best_loss = 100000
    best_epoch = 0

    MAX_EPOCHS = 10
    epoch_history = {
        'acc': [],
        'val_acc': [],
        'loss': [],
        'val_loss': [],
    }

    # for each epoch
    for epoch in range(MAX_EPOCHS):
        history = model.fit(x=x_train, y=y_train, nb_epoch=1, batch_size=1, validation_data=(x_valid, y_valid),
                            verbose=1, shuffle=False)

        # get validation (test) accuracy and loss
        accuracy = history.history['val_acc'][0]
        loss = history.history['val_loss'][0]

        # set epochs' history
        epoch_history['acc'].append(history.history['acc'][0])
        epoch_history['val_acc'].append(history.history['val_acc'][0])
        epoch_history['loss'].append(history.history['loss'][0])
        epoch_history['val_loss'].append(history.history['val_loss'][0])

        # select best epoch and save to disk
        if accuracy >= best_accuracy and loss < best_loss:
            logging.info("Saving model")
            model.save("model.h5")

            best_accuracy = accuracy
            best_loss = loss
            best_epoch = epoch

    # Plot training & validation accuracy values
    plt.plot(epoch_history['acc'])
    plt.plot(epoch_history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(epoch_history['loss'])
    plt.plot(epoch_history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    print(epoch_history['val_acc'])

    # load the best model saved on disk
    del model
    model = load_model("model.h5")

    evaluation = model.evaluate(x=x_test, y=y_test)
    print(evaluation)

