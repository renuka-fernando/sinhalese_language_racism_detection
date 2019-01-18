import logging

import matplotlib.pyplot as plt
import numpy as np
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
    transform_class_to_one_hot_representation, get_calculated_user_profile, append_user_profile_features

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

# add user profile feature to end of the sentence
# from: Detecting Offensive Language in Tweets using Deep Learning
# by: Georgios K. Pitsilis, Heri Ramampiaro and Helge Langseth
max_word_count = MAX_WORD_COUNT + 3
x_corpus = append_user_profile_features(x_corpus=x_corpus, user_ids=data_set[:, DATA_SET_USER_ID],
                                        user_profile=user_profile)

# padding with zeros if not enough and else drop left-side words
x_corpus = sequence.pad_sequences(x_corpus, maxlen=max_word_count)

# shuffling data for 5-fold cross validation
k_fold = StratifiedKFold(n_splits=5, shuffle=True, random_state=18)
# to split, raw format (integer) is required
y_corpus_raw = [0 if cls[2] == 1 else (1 if cls[1] == 1 else 2) for cls in y_corpus]

fold = 0
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
    model.add(Embedding(input_dim=6000, output_dim=50, input_length=max_word_count))
    model.add(LSTM(300))
    model.add(Dense(units=50, activation='relu', W_regularizer=regularizers.l2(0.09)))
    model.add(Dense(3, activation='softmax', W_regularizer=regularizers.l2(0.02)))
    adam_optimizer = Adam(lr=0.0001)
    model.compile(loss='categorical_crossentropy', optimizer=adam_optimizer, metrics=['accuracy'])

    print(model.summary())

    best_accuracy = 0
    best_loss = 100000
    best_epoch = 0

    MAX_EPOCHS = 3
    epoch_history = {
        'acc': [],
        'val_acc': [],
        'loss': [],
        'val_loss': [],
    }

    # for each epoch
    for epoch in range(MAX_EPOCHS):
        logging.info("Epoch: %d" % epoch)
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
        if accuracy >= best_accuracy and loss < best_loss + 0.01:
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
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(epoch_history['loss'])
    plt.plot(epoch_history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

    # Saving evolution history of epochs in this fold
    evolution_history_file_name = "history_fold_" + str(fold)
    fold += 1
    f = open(evolution_history_file_name, 'w')
    f.write("epoch,training_accuracy,training_loss,validation_accuracy,validation_loss\n")
    for i in range(MAX_EPOCHS):
        f.write("%d,%f,%f,%f,%f\n" % (i, epoch_history['acc'][i], epoch_history['loss'][i],
                                      epoch_history['val_acc'][i], epoch_history['val_loss'][i]))
    f.close()

    # load the best model saved on disk
    del model
    model = load_model("model.h5")

    evaluation = model.evaluate(x=x_test, y=y_test)
    logging.info("Accuracy: %f" % evaluation[1])

    prediction = model.predict(x_test)

    test_indexes = test_indexes.reshape(test_indexes.shape[0], 1)
    tweet_ids = data_set[:, DATA_SET_USER_ID][test_indexes]
    true_labels = np.asarray(y_corpus_raw, dtype=int)[test_indexes]
    class_1 = prediction[:, 2]
    class_2 = prediction[:, 1]
    class_3 = prediction[:, 0]
    output = np.append(tweet_ids, true_labels, axis=1)
    output = np.append(output, class_1.reshape(test_indexes.shape[0], 1), axis=1)
    output = np.append(output, class_2.reshape(test_indexes.shape[0], 1), axis=1)
    output = np.append(output, class_3.reshape(test_indexes.shape[0], 1), axis=1)

    np.savetxt("report_output_%d" % fold, X=output, fmt="%s", delimiter=",")
    logging.INFO("Fold: %d - Completed" % fold)
