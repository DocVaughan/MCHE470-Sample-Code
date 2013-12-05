#! /usr/bin/env python 

##########################################################################################
# kmeans_example.py
#
# Script to look at an example KMeans classificaiton
#
# Based on: 
#   http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 12/4/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
##########################################################################################


from time import time
import numpy as np
from scipy import genfromtxt
from matplotlib.pyplot import * 
from matplotlib.colors import ListedColormap

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale


# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])


np.random.seed(42)

# import some data to play with
data = genfromtxt("me2110grades.csv",delimiter=",",skip_header=1)
# data = genfromtxt("vib_fall2012.csv",delimiter=",",skip_header=1)
X = data[:,(0,2)]    # we only take two features at a time

# Normalize/scale the data
# X[:,0] = 1*X[:,0]/np.max(X[:,0])
# X[:,1] = 1*X[:,1]/np.max(X[:,1])
# or
# X = scale(X)


# the fifth column is the grade A=3, B=2, <C = 1
y = data[:,4]    

# Get the A data
A_itemindex=np.where(y==3)
X_A = X[A_itemindex]
y_A = y[A_itemindex]

# Get the B data
B_itemindex=np.where(y==2)
X_B = X[B_itemindex]
y_B = y[B_itemindex]

# Get the <C data
C_itemindex=np.where(y==1)
X_C = X[C_itemindex]
y_C = y[C_itemindex]

# Show the raw data
plot(X_A[:,0],X_A[:,1],'r*',label='A')
plot(X_B[:,0],X_B[:,1],'bo',label='B')
plot(X_C[:,0],X_C[:,1],'kx',label = 'C')
xlim(min(X[:,0])-0.5,max(X[:,0])+0.5)
ylim(min(X[:,1])-0.5,max(X[:,1])+0.5)

xlabel('Feature 1',fontsize=22,labelpad=8)
ylabel('Feature 2',fontsize=22,labelpad=8)

leg = legend(loc='upper left', ncol = 1, fancybox=True, borderaxespad=0.2)
ltext  = leg.get_texts() 
setp(ltext,fontsize=16)

   

n_samples = len(data)
n_features = 2
n_digits = len(np.unique(y))
labels = y

sample_size = 75

print("n_digits: %d, \t n_samples %d, \t n_features %d"
      % (n_digits, n_samples, n_features))


print(79 * '_')
print('% 9s' % 'init'
      '    time  inertia    homo   compl  v-meas     ARI AMI  silhouette')


def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
              name="k-means++", data=X)

bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
              name="random", data=X)

# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
pca = PCA(n_components=n_digits).fit(X)
bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
              name="PCA-based",
              data=X)
print(79 * '_')

###############################################################################
# Visualize the results on PCA-reduced data

reduced_data = PCA(n_components=2).fit_transform(X)
kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=3)
kmeans.fit(reduced_data)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
figure()
clf()
imshow(Z, interpolation='nearest',
          extent=(xx.min(), xx.max(), yy.min(), yy.max()),
          cmap=cmap_light,
          aspect='auto', origin='lower')

# plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
## Show the raw data
plot(X_A[:,0],X_A[:,1],'r*',label='A')
plot(X_B[:,0],X_B[:,1],'bo',label='B')
plot(X_C[:,0],X_C[:,1],'kx',label = 'C')
xlim(min(X[:,0])-0.5,max(X[:,0])+0.5)
ylim(min(X[:,1])-0.5,max(X[:,1])+0.5)

xlabel('Feature 1',fontsize=22,labelpad=8)
ylabel('Feature 2',fontsize=22,labelpad=8)

leg = legend(loc='upper left', ncol = 1, fancybox=True, borderaxespad=0.2)
ltext  = leg.get_texts() 
setp(ltext,fontsize=16)


# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
scatter(centroids[:, 0], centroids[:, 1],
           marker='x', s=169, linewidths=3,
           color='w', zorder=10)
# title('K-means clustering on the digits dataset (PCA-reduced data)\n'
#          'Centroids are marked with white cross')
xlim(x_min, x_max)
ylim(y_min, y_max)
xticks(())
yticks(())

show()
