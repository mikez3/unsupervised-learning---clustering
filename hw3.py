# -*- coding: utf-8 -*-
"""HW3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YwaMKYwZMPp8LQVwMUdXKWMRPJuky0Zu
"""

from keras.datasets import fashion_mnist
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn import metrics


# ---------- 1o ----------
# Load the Fashion MNIST dataset and split the data into training and test sets
(X_train, y_train), (X_test, y_test)= fashion_mnist.load_data()

# ---------- 2o ----------
# Split the data into training, validation, and test sets
X_train, X_validate, y_train, y_validate = train_test_split(X_train, y_train, test_size=0.1, random_state=1)

# ---------- 3o ----------
# Principal Component Analysis with 99% of variance
pca = PCA(0.99, whiten=True)

pca_created_data = pca.fit_transform(X_train.reshape(X_train.shape[0], (X_train.shape[1]*X_train.shape[2])))
pca_created_data.shape

# ---------- 4o ----------
# Apply the existing PCA transform to new data; i.e. on VALIDATION SET
pca_projected_data_validate_set = pca.transform(X_validate.reshape(X_validate.shape[0], (X_validate.shape[1]*X_validate.shape[2])))
print('validate set data projected sucessfully.')
print(pca_projected_data_validate_set.shape)

# Inverse transform
inversed_pca_validation_data = pca.inverse_transform(pca_projected_data_validate_set)

# ---------- 5o ----------
def plot_digits(data,labels):
    fig, ax = plt.subplots(10, 10, figsize=(28, 28),subplot_kw=dict(xticks=[], yticks=[]))
    fig.subplots_adjust(hspace=0.05, wspace=0.05)
    printed_classes = list(range(10))

    for i, axi in enumerate(ax.flat):
      im = axi.imshow(data[i], cmap='binary')
      im.set_clim(0, 16)
      if (printed_classes[labels[i]] is not None):
        printed_classes[labels[i]] = None
      # Check if an element from every class have been printed at least one time
      if (i>=90) and (not(all(element is None for element in printed_classes))):
        if (printed_classes[labels[i]] is not None):
          im = axi.imshow(data[i], cmap='binary')
          im.set_clim(0, 16)
          printed_classes[labels[i]] = None
          
plot_digits(X_validate,y_validate)

#remember to reshape the 2d to 3d for the plot digits function to work
plot_digits(inversed_pca_validation_data.reshape(inversed_pca_validation_data.shape[0],X_train.shape[1],X_train.shape[2]),y_validate)

# --------- 6o ---------
# Apply the existing PCA transform to new data; i.e. on TEST SET
pca_projected_data_test_set = pca.transform(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
print('test set data projected sucessfully.')
print(pca_projected_data_test_set.shape)

# ---------- 7o + 8o ----------
# define a performance evaluation function
from sklearn import metrics
def performance_score(input_values, cluster_indexes):
    try:
        silh_score = metrics.silhouette_score(input_values.reshape(-1, 1), cluster_indexes)
        print(' .. Silhouette Coefficient score is {:.2f}'.format(silh_score))
        #print( ' ... -1: incorrect, 0: overlapping, +1: highly dense clusts.')
    except:
        print(' .. Warning: could not calculate Silhouette Coefficient score.')
        silh_score = -999

    try:
        ch_score = metrics.calinski_harabasz_score(input_values.reshape(-1, 1), cluster_indexes)
        print(' .. Calinski-Harabasz Index score is {:.2f}'.format(ch_score))
        #print(' ... Higher the value better the clusters.')
    except:
        print(' .. Warning: could not calculate Calinski-Harabasz Index score.')
        ch_score = -999

    try:
        db_score = metrics.davies_bouldin_score(input_values.reshape(-1, 1), cluster_indexes)
        print(' .. Davies-Bouldin Index score is {:.2f}'.format(db_score))
        #print(' ... 0: Lowest possible value, good partitioning.')
    except:
        print(' .. Warning: could not calculate Davies-Bouldin Index score.')
        db_score = -999

    try:
        ami_score = metrics.adjusted_mutual_info_score(cluster_indexes, input_values)
        print(' .. Adjusted Mutual Information score is {:.2f}'.format(ami_score))
        #print( ' ...  Higher the value better the clusters')
    except:
        print(' .. Warning: could not calculate Adjusted Mutual Information score.')
        ami_score = -999
        

    return silh_score, ch_score, db_score, ami_score


# ORIGINAL DATA
# Find the best number of clusters for the mini batch kmeans
from sklearn import cluster
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),'number of clusters')
  mbkm = cluster.MiniBatchKMeans(n_clusters = numOfClust)
  mbkm.fit(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
  clusterLabels = mbkm.labels_
  # silh_score = metrics.silhouette_score(outputData.reshape(-1, 1), clusterLabels)
  silh_score, ch_score, db_score, ami_score = performance_score( y_test, clusterLabels)

# PCA
# Find the best number of clusters for the mini batch kmeans
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),'number of clusters')
  mbkm = cluster.MiniBatchKMeans(n_clusters = numOfClust)
  mbkm.fit(pca_projected_data_test_set)
  clusterLabels = mbkm.labels_
  # silh_score = metrics.silhouette_score(outputData.reshape(-1, 1), clusterLabels)
  silh_score, ch_score, db_score, ami_score = performance_score( y_test, clusterLabels)

# Find the best number of clusters for the Hierarchical clustering (Agglomerative Clustering)
# ORIGINAL DATA
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),'number of clusters')
  hier = cluster.AgglomerativeClustering(n_clusters = numOfClust).fit(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
  hier_original_clusterLabels = hier.labels_
  clusterLabels = hier_original_clusterLabels
  # silh_score = metrics.silhouette_score(outputData.reshape(-1, 1), clusterLabels)
  silh_score, ch_score, db_score, ami_score = performance_score( y_test, clusterLabels)

# Find the best number of clusters for the Hierarchical clustering (Agglomerative Clustering)
# PCA
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),'number of clusters')
  hier = cluster.AgglomerativeClustering(n_clusters = numOfClust).fit(pca_projected_data_test_set)
  hier_original_clusterLabels = hier.labels_
  clusterLabels = hier_original_clusterLabels
  # silh_score = metrics.silhouette_score(outputData.reshape(-1, 1), clusterLabels)
  silh_score, ch_score, db_score, ami_score = performance_score( y_test, clusterLabels)

# Find the best number of clusters for the Gaussian Mixture
# ORIGINAL DATA
from sklearn.mixture import GaussianMixture
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),'number of clusters')
  gmm = GaussianMixture(n_components=numOfClust).fit(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
  # Predict the cluster labels for each sample
  gmm_pca_labels = gmm.predict(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
  clusterLabels = gmm_pca_labels
  # silh_score = metrics.silhouette_score(outputData.reshape(-1, 1), clusterLabels)
  silh_score, ch_score, db_score, ami_score = performance_score( y_test, clusterLabels)

# Find the best number of clusters for the Gaussian Mixture
# PCA
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),'number of clusters')
  gmm = GaussianMixture(n_components=numOfClust).fit(pca_projected_data_test_set)
  # Predict the cluster labels for each sample
  gmm_pca_labels = gmm.predict(pca_projected_data_test_set)
  clusterLabels = gmm_pca_labels
  # silh_score = metrics.silhouette_score(outputData.reshape(-1, 1), clusterLabels)
  silh_score, ch_score, db_score, ami_score = performance_score( y_test, clusterLabels)

# ---------- 7o gia cluster = 3 ----------
# apply cluster approaches on the original test set
# the mini batch kmeans cluster approach 
# Specify the number of clusters
num_clusters = 3
# mini batch kmeans
mbkm = cluster.MiniBatchKMeans(n_clusters = num_clusters)
mbkm.fit(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
mbkm_original_clusterLabels = mbkm.labels_

# Hierarchical clustering (Agglomerative Clustering)
hier = cluster.AgglomerativeClustering(n_clusters = num_clusters).fit(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
hier_original_clusterLabels = hier.labels_

# Gaussian Mixture
gmm = GaussianMixture(n_components=num_clusters).fit(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))
# Predict the cluster labels for each sample
gmm_original_labels = gmm.predict(X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))

# The cluster labels are stored in the labels array

# apply cluster approaches on the projected test set
# mini batch k-Means - PCA
mbkm = cluster.MiniBatchKMeans(n_clusters = num_clusters)
mbkm.fit(pca_projected_data_test_set)
mbkm_pca_clusterLabels = mbkm.labels_

# Hierarchical clustering (Agglomerative Clustering) - PCA
hier = cluster.AgglomerativeClustering(n_clusters = num_clusters).fit(pca_projected_data_test_set)
hier_pca_clusterLabels = hier.labels_

# Gaussian Mixture - PCA
gmm = GaussianMixture(n_components=num_clusters).fit(pca_projected_data_test_set)
# Predict the cluster labels for each sample
gmm_pca_labels = gmm.predict(pca_projected_data_test_set)

# The cluster labels are stored in the labels array
print(gmm_pca_labels)

mbkm_silh_score, mbkm_ch_score, mbkm_db_score, mbkm_ami_score = performance_score( y_test, mbkm_original_clusterLabels)
hier_silh_score, hier_ch_score, hier_db_score, hier_ami_score = performance_score( y_test, hier_original_clusterLabels)
gmm_silh_score, gmm_ch_score, gmm_db_score, gmm_ami_score = performance_score( y_test, gmm_original_labels)

# PCA
mbkm_pca_silh_score, mbkm_ch_score, mbkm_db_score, mbkm_ami_score = performance_score( y_test, mbkm_pca_clusterLabels)
hier_pca_silh_score, hier_ch_score, hier_db_score, hier_ami_score = performance_score( y_test, hier_pca_clusterLabels)
gmm_pca_silh_score, gmm_ch_score, gmm_db_score, gmm_ami_score = performance_score( y_test, gmm_pca_labels)


# ---------- 9o ----------
#performance scores & visualizations

# mini batch kMeans / raw
fig = plt.figure(figsize=(20,20))
for clusterIdx in range(num_clusters):
    # cluster = cm[r].argmax()
    for c, val in enumerate(X_test[mbkm_original_clusterLabels == clusterIdx][0:10]):
        fig.add_subplot(10, 10, 10*clusterIdx+c+1)
        plt.imshow(val.reshape((28,28)))
        plt.gray()
        plt.xticks([])
        plt.yticks([])
        # print(clusterIdx, c)
        plt.xlabel('cluster: '+str(cluster))
        # plt.ylabel('class: '+str(clusterIdx))
        plt.ylabel('class: '+str(clusterIdx))

# mini batch kMeans / PCA
fig = plt.figure(figsize=(20,20))
for clusterIdx in range(num_clusters):
    # cluster = cm[r].argmax()
    for c, val in enumerate(X_test[mbkm_pca_clusterLabels == clusterIdx][0:10]):
        fig.add_subplot(10, 10, 10*clusterIdx+c+1)
        plt.imshow(val.reshape((28,28)))
        plt.gray()
        plt.xticks([])
        plt.yticks([])
        # print(clusterIdx, c)
        plt.xlabel('cluster: '+str(cluster))
        # plt.ylabel('class: '+str(clusterIdx))
        plt.ylabel('class: '+str(clusterIdx))

# Hierarchical Clustering / raw
fig = plt.figure(figsize=(20,20))
for clusterIdx in range(num_clusters):
    # cluster = cm[r].argmax()
    for c, val in enumerate(X_test[hier_original_clusterLabels == clusterIdx][0:10]):
        fig.add_subplot(10, 10, 10*clusterIdx+c+1)
        plt.imshow(val.reshape((28,28)))
        plt.gray()
        plt.xticks([])
        plt.yticks([])
        # print(clusterIdx, c)
        plt.xlabel('cluster: '+str(cluster))
        # plt.ylabel('class: '+str(clusterIdx))
        plt.ylabel('class: '+str(clusterIdx))

# Hierarchical Clustering / PCA
fig = plt.figure(figsize=(20,20))
for clusterIdx in range(num_clusters):
    # cluster = cm[r].argmax()
    for c, val in enumerate(X_test[hier_pca_clusterLabels == clusterIdx][0:10]):
        fig.add_subplot(10, 10, 10*clusterIdx+c+1)
        plt.imshow(val.reshape((28,28)))
        plt.gray()
        plt.xticks([])
        plt.yticks([])
        # print(clusterIdx, c)
        plt.xlabel('cluster: '+str(cluster))
        # plt.ylabel('class: '+str(clusterIdx))
        plt.ylabel('class: '+str(clusterIdx))

# GMM / raw
fig = plt.figure(figsize=(20,20))
for clusterIdx in range(num_clusters):
    # cluster = cm[r].argmax()
    for c, val in enumerate(X_test[gmm_original_labels == clusterIdx][0:10]):
        fig.add_subplot(10, 10, 10*clusterIdx+c+1)
        plt.imshow(val.reshape((28,28)))
        plt.gray()
        plt.xticks([])
        plt.yticks([])
        # print(clusterIdx, c)
        plt.xlabel('cluster: '+str(cluster))
        # plt.ylabel('class: '+str(clusterIdx))
        plt.ylabel('class: '+str(clusterIdx))

# GMM / PCA
fig = plt.figure(figsize=(20,20))
for clusterIdx in range(num_clusters):
    # cluster = cm[r].argmax()
    for c, val in enumerate(X_test[gmm_pca_labels == clusterIdx][0:10]):
        fig.add_subplot(10, 10, 10*clusterIdx+c+1)
        plt.imshow(val.reshape((28,28)))
        plt.gray()
        plt.xticks([])
        plt.yticks([])
        # print(clusterIdx, c)
        plt.xlabel('cluster: '+str(cluster))
        # plt.ylabel('class: '+str(clusterIdx))
        plt.ylabel('class: '+str(clusterIdx))
