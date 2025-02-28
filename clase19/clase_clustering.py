#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:20:52 2024

@author: mcerdeiro
"""

import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
#from statsmodels.datasets import get_rdataset
#from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import datasets
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram , cut_tree

#%%
np.random.seed (0);
X = np.random.standard_normal ((50 ,2));
X[:25 ,0] += 6;
X[:25 ,1] -= 8;
X[:10 ,0] += 8;
X[:10 ,1] += 8;
X[:1 ,0] -= 8;
#%%
fig , ax = plt.subplots (1, 1, figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1])
#%%
kmeans = KMeans(n_clusters = 2, random_state = 2, n_init = 20)
kmeans.fit(X)
kmeans.labels_
#%%

fig , ax = plt.subplots (1, 1, figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=kmeans.labels_)
ax.set_title("K-Means Clustering Results with K=2");

#%%
kmeans = KMeans(n_clusters =3, random_state =3, n_init =20)
kmeans.fit(X)
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=kmeans.labels_)
ax.set_title("K-Means Clustering Results with K=3");


#%%
kmeans1 = KMeans(n_clusters =3, random_state =3, n_init =1)
kmeans1.fit(X) 
kmeans20 = KMeans(n_clusters =3, random_state =3, n_init =20)
kmeans20.fit(X);

kmeans1.inertia_ , kmeans20.inertia_

#%%
dbclust = DBSCAN(eps=2, min_samples=6)

dbclust.fit(X)
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=dbclust.labels_)
ax.set_title("DBSCAN Results");
#%%



#%%
HClust = AgglomerativeClustering
hc_comp = HClust( distance_threshold =0, n_clusters=None , linkage='complete')
hc_comp.fit(X)
#%%
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=hc_comp.labels_)
ax.set_title("Agglomerative Clustering Results");
#%%
HClust = AgglomerativeClustering
hc_comp = HClust( distance_threshold =None, n_clusters=3 , linkage='complete')
hc_comp.fit(X)
#%%
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=hc_comp.labels_)
ax.set_title("Agglomerative Clustering Results");
#%%
HClust = AgglomerativeClustering
hc_comp = HClust( distance_threshold = None, n_clusters=2 , linkage='complete')
hc_comp.fit(X)
#%%
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=hc_comp.labels_)
ax.set_title("Agglomerative Clustering Results");
#%%
hc_avg = HClust(distance_threshold =0, n_clusters=None , linkage='average'); 
hc_avg.fit(X)
hc_sing = HClust(distance_threshold =0, n_clusters=None , linkage='single');
hc_sing.fit(X);

#%%
D = np.zeros ((X.shape [0], X.shape [0]));
for i in range(X.shape [0]):
    x_ = np.multiply.outer(np.ones(X.shape [0]) , X[i])
    D[i] = np.sqrt(np.sum((X - x_)**2, 1));
hc_sing_pre = HClust( distance_threshold =0, n_clusters=None , metric='precomputed', linkage='single')
hc_sing_pre.fit(D)

#%%
def compute_linkage(model):
    # Create linkage matrix 
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    return linkage_matrix
    

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

#%%

hc_comp = HClust( distance_threshold =0, n_clusters=None , linkage='complete')
hc_comp.fit(X)

linkage_comp = compute_linkage(hc_comp)
dendrogram(linkage_comp)
#%%
plt.figure(figsize = (15,15))
plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
#plot_dendrogram(hc_comp, truncate_mode="level", p=3)
dendrogram(linkage_comp ,  color_threshold =4, above_threshold_color ='black');

#plot_dendrogram(hc_comp)
# plt.show()

#%%
cargs = {'color_threshold':-np.inf , 'above_threshold_color':'black'}
linkage_comp = compute_linkage(hc_comp)
fig , ax = plt.subplots(1, 1, figsize =(12, 8))
dendrogram(linkage_comp , ax=ax , ** cargs);

#%%
fig , ax = plt.subplots (1, 1, figsize =(8, 8))
dendrogram(linkage_comp , ax=ax , color_threshold =4, above_threshold_color ='black');

#%%
cut_tree(linkage_comp , n_clusters =4).T

#%%
cut_tree(linkage_comp , height = 3)

#%%
scaler = StandardScaler ()
X_scale = scaler.fit_transform(X)
hc_comp_scale = HClust( distance_threshold =0,
n_clusters=None ,
linkage='complete').fit(X_scale)
linkage_comp_scale = compute_linkage(hc_comp_scale)
fig , ax = plt.subplots (1, 1, figsize =(8, 8))
dendrogram(linkage_comp_scale , ax=ax , ** cargs)
ax.set_title("Hierarchical Clustering with Scaled Features");

#%%
######## OTROS DATOS SINTETICOS
#%%
seed = 75
n_samples = 500
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=0.05, random_state=seed)

noisy_circles = datasets.make_circles(n_samples=n_samples, factor=0.5, noise=0.05, random_state=seed)

blobs = datasets.make_blobs(n_samples=n_samples, random_state=seed)

varied = datasets.make_blobs(n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5], random_state=seed)
#%%
for dataset in [noisy_moons, noisy_circles, blobs, varied]:
    X, y = dataset
    plt.figure()
    plt.scatter(X[:, 0], X[:, 1], s=10)
    

    plt.xticks(())
    plt.yticks(())
    plt.show()

#%%



