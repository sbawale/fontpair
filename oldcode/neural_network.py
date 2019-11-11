from __future__ import absolute_import, division, print_function, unicode_literals
import json, urllib.request, re, csv, glob, os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from keras.models import Sequential
from keras.layers import Dense
from numpy import array
from scipy.sparse import csr_matrix
from sklearn.cluster import KMeans
from keras.datasets import mnist

# Get custom helper functions
# from preprocess_data import *
from preprocess_data_gf import *
from helper_functions import *

# ***************** BUILD MODEL *****************

# STEPS:
# Get data, reshape/preprocess as necessary
# Split into train/test (not as necessary for recommender systems)
# Standardize data (StandardScalar -> fit_transform)
# Reduce dimensionality (PCA)
# Construct NN
    # Initialize weights (parameters that we want to train)
    # Propagate forward
    # Calculate the cost
    # Propagate backward
    # Update the weights
    # Repeat until convergence
# Optimize iteratively with gradient descent
# Test neural network

col_names =  ['name','family','category','is_body','is_serif','is_italic','weight']
font_weights = ['Thin','Extra Light','Light','Regular','Medium',
                'Semi Bold','Bold','Extra Bold','Black']
font_weights_num = [100, 200, 300, 400, 500, 600, 700, 800, 900]

def build_neural_network(data_filename):
    # ***************** RETRIEVE AND PREPROCESS DATA *****************
    # Get preprocessed data from Google Fonts API
    fonts = preprocess_data_gf()
    # fonts = pd.read_csv(data_filename)
    print(fonts.head())

    # Encode string features as labels for standardization
    le_name = preprocessing.LabelEncoder()
    le_family = preprocessing.LabelEncoder()
    le_category = preprocessing.LabelEncoder()

    fonts['name'] = le_name.fit_transform(fonts['name'])
    fonts['family'] = le_family.fit_transform(fonts['family'])
    fonts['category'] = le_name.fit_transform(fonts['category'])

    # Split data into train, test, and validation sets
    train_data, test_data = train_test_split(fonts,train_size=0.8)
    train_data, validation_data = train_test_split(train_data, train_size=0.8)
    # print(len(train), 'train examples')
    # print(len(validation), 'validation examples')
    # print(len(test), 'test examples')

    # Standardize data using Scaler; fit on training data
    scaler = preprocessing.StandardScaler()
    scaler.fit(train_data)

    # Apply standardization to each dataset
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.fit_transform(test_data)
    validation_data = scaler.fit_transform(validation_data)

    # scaled_df = pd.DataFrame(train_data, columns=col_names)
    # print(train_data,"\n")
    # print(train_data.head())
    # print(scaled_df.head())

    # Define and fit PCA model for reducing dimensionality
    pca = PCA(.95)
    pca.fit(train_data)

    # Apply PCA to each dataset
    train_data = pca.transform(train_data)
    test_data = pca.transform(test_data)
    validation_data = pca.transform(validation_data)
    print("\n",pca.n_components_)
    print(train_data)

    # ***************** CONVERT FONT TUPLES TO VECTORS  *****************
    # print("Converting font tuples to vectors...")

    # # Create list of all unique words in font names and families
    # names = get_unique_strings(fonts,0)
    # families = get_unique_strings(fonts,1)

    # # Create list of features (combination of category, is_body, is_serif, is_italic, and weight)
    # features = ['body','display','handwriting','monospace','serif','sans-serif','italic','weight']

    # # Convert all fonts to vectors and store in list
    # vectors = []
    # for f in fonts.itertuples(index=False,name=None):
    #     current = vectorize_font(f,names,families,features,font_weights_num)
    #     vectors.append(current)

    # print("All vectors created.")

    # # condensed = csr_matrix(vectors)
    # # print(condensed)
    # # denser = vectors.todense()

    # # Split data into train, test, and validation sets
    # train_data, test_data = train_test_split(vectors,train_size=0.8)
    # train_data, validation_data = train_test_split(train_data, train_size=0.8)

    # # Define and fit PCA model for reducing dimensionality
    # # pca = PCA(.95)
    # # pca.fit(train_data)

    # # # Apply PCA to each dataset
    # # train_data = pca.transform(train_data)
    # # test_data = pca.transform(test_data)
    # # validation_data = pca.transform(validation_data)
    # print(train_data)

    # ***************** CREATE EMBEDDINGS FROM VECTORS  *****************
    # code blah blah blah
    # Convert list of embeddings to dataframe?
    # batch_size = 5 # A small batch sized is used for demonstration purposes
    # train_ds = df_to_dataset(train, batch_size=batch_size)
    # val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    # test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

    # train_data, test_data = train_test_split(fonts,train_size=0.8)
    # train_data, validation_data = train_test_split(train_data,train_size=0.8)
    # # train_data, test_data = split_train_test(fonts, 0.8)
    # # print(len(fonts))
    # print("train size: ",len(train_data))
    # # print(train_data.head())
    # print("test size: ",len(test_data))
    # # print(test_data.head())
    # print("val size: ",len(validation_data))


    # ***************** BUILD AND TRAIN MODEL *****************

    # Use clustering NN instead
    # category used as the "class" (display,handwriting,monospace)
    # or possibly add another feature to act as the class/label? formal,informal,neutral

    # (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # x = np.concatenate((x_train, x_test))
    # y = np.concatenate((y_train, y_test))
    # x = x.reshape((x.shape[0], -1))
    # x = np.divide(x, 255.)
    # # 10 clusters
    # n_clusters = len(np.unique(y))
    # # Runs in parallel 4 CPUs
    # kmeans = KMeans(n_clusters=n_clusters, n_init=20, n_jobs=4)
    # # Train K-Means.
    # y_pred_kmeans = kmeans.fit_predict(x)
    # # Evaluate the K-Means clustering accuracy.
    # metrics.acc(y, y_pred_kmeans)

    # autoencoder.fit(x, x, batch_size=256, epochs=300) #, callbacks=cb)
    # autoencoder.save_weights('./results/ae_weights.h5')

    # clustering_layer = ClusteringLayer(n_clusters, name='clustering')(encoder.output)
    # model = Model(inputs=encoder.input, outputs=clustering_layer)
    # # Initialize cluster centers using k-means.
    # kmeans = KMeans(n_clusters=n_clusters, n_init=20)
    # y_pred = kmeans.fit_predict(encoder.predict(x))
    # model.get_layer(name='clustering').set_weights([kmeans.cluster_centers_])


    # define the keras model
    model = Sequential()
    # model.add(Dense(12, input_dim=7, activation=activation_function))
    model.add(Dense(12, input_dim=7, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # compile the keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit the keras model on the dataset
    model.fit(train_data, font['category'], epochs=150, batch_size=10)

    # evaluate the keras model
    _, accuracy = model.evaluate(train_data, y)
    print('Accuracy: %.2f' % (accuracy*100))

# ***************** TEST MODEL *****************

# Google's helper method for converting dataframe to dataset
# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  # labels = dataframe.pop('target') # BUT I DON'T NEED LABELS???
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe)))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds

def predict(neural_network,value,n):
    print("Definitely can't do yet.")
    # This function should return a list of the n most similar fonts and the n most dissimilar fonts

# ***************** DEBUGGING *****************

test = build_neural_network("cleanedGF.csv")

class ClusteringLayer(Layer):
    """
    Clustering layer converts input sample (feature) to soft label.

    # Example
    ```
        model.add(ClusteringLayer(n_clusters=10))
    ```
    # Arguments
        n_clusters: number of clusters.
        weights: list of Numpy array with shape `(n_clusters, n_features)` witch represents the initial cluster centers.
        alpha: degrees of freedom parameter in Student's t-distribution. Default to 1.0.
    # Input shape
        2D tensor with shape: `(n_samples, n_features)`.
    # Output shape
        2D tensor with shape: `(n_samples, n_clusters)`.
    """

    def __init__(self, n_clusters, weights=None, alpha=1.0, **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(ClusteringLayer, self).__init__(**kwargs)
        self.n_clusters = n_clusters
        self.alpha = alpha
        self.initial_weights = weights
        self.input_spec = InputSpec(ndim=2)

    def build(self, input_shape):
        assert len(input_shape) == 2
        input_dim = input_shape[1]
        self.input_spec = InputSpec(dtype=K.floatx(), shape=(None, input_dim))
        self.clusters = self.add_weight((self.n_clusters, input_dim), initializer='glorot_uniform', name='clusters')
        if self.initial_weights is not None:
            self.set_weights(self.initial_weights)
            del self.initial_weights
        self.built = True

    def call(self, inputs, **kwargs):
        """ student t-distribution, as same as used in t-SNE algorithm.
                 q_ij = 1/(1+dist(x_i, µ_j)^2), then normalize it.
                 q_ij can be interpreted as the probability of assigning sample i to cluster j.
                 (i.e., a soft assignment)
        Arguments:
            inputs: the variable containing data, shape=(n_samples, n_features)
        Return:
            q: student's t-distribution, or soft labels for each sample. shape=(n_samples, n_clusters)
        """
        q = 1.0 / (1.0 + (K.sum(K.square(K.expand_dims(inputs, axis=1) - self.clusters), axis=2) / self.alpha))
        q **= (self.alpha + 1.0) / 2.0
        q = K.transpose(K.transpose(q) / K.sum(q, axis=1)) # Make sure each sample's 10 values add up to 1.
        return q

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) == 2
        return input_shape[0], self.n_clusters

    def get_config(self):
        config = {'n_clusters': self.n_clusters}
        base_config = super(ClusteringLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))