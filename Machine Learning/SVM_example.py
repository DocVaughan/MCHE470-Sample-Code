#! /usr/bin/env python 

##########################################################################################
# SVM_example.py
#
# Script to look at an example nearest-SVM classificaiton
#
# Based on: 
#   http://scikit-learn.org/stable/auto_examples/svm/plot_iris.html
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 12/5/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
##########################################################################################


import numpy as np
from scipy import genfromtxt
from matplotlib.pyplot import * 
from matplotlib.colors import ListedColormap
from sklearn import svm, datasets


# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

# import some data to play with
data = genfromtxt("me2110grades.csv",delimiter=",",skip_header=1)
# data = genfromtxt("vib_fall2012.csv",delimiter=",",skip_header=1)
X = data[:,(0,2)]    # we only take two feature at a time

# Normalize/scale the data
# X[:,0] = 1*X[:,0]/np.max(X[:,0])
# X[:,1] = 1*X[:,1]/np.max(X[:,1])
# or
# X = scale(X)


# the third column is the grade A=3, B=2, <C = 1
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
xlim(0.9*min(X[:,0]),1.1*max(X[:,0]))
ylim(0.9*min(X[:,1]),1.1*max(X[:,1]))

xlabel('Feature 1',fontsize=22,labelpad=5)
ylabel('Feature 2',fontsize=22,labelpad=10)

leg = legend(loc='upper left', ncol = 1, fancybox=True, borderaxespad=0.2)
ltext  = leg.get_texts() 
setp(ltext,fontsize=16)


h = .005  # step size in the mesh

# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
C = 1.0  # SVM regularization parameter
svc = svm.SVC(kernel='linear', C=C).fit(X, y)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X, y)
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X, y)
lin_svc = svm.LinearSVC(C=C).fit(X, y)

# create a mesh to plot in
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# title for the plots
# titles = ['SVC with linear kernel',
#           'SVC with RBF kernel',
#           'SVC with polynomial (degree 3) kernel',
#           'LinearSVC (linear kernel)']
#
#
# for i, clf in enumerate((svc, rbf_svc, poly_svc, lin_svc)):
#     # Plot the decision boundary. For that, we will assign a color to each
#     # point in the mesh [x_min, m_max]x[y_min, y_max].
#     subplot(2, 2, i + 1)
#     Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
# 
#     # Put the result into a color plot
#     Z = Z.reshape(xx.shape)
#     contourf(xx, yy, Z, cmap=cm.Paired)
#     axis('off')
# 
#     # Plot also the training points
#     scatter(X[:, 0], X[:, 1], cmap=cm.Paired)
# 
#     title(titles[i])
# 
# show()


# types are svc, rbf_svc, poly_svc, lin_svc)
Z = rbf_svc.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
figure()
Z = Z.reshape(xx.shape)
contourf(xx, yy, Z, cmap=cmap_light)

# Show the raw data
plot(X_A[:,0],X_A[:,1],'r*',label='A')
plot(X_B[:,0],X_B[:,1],'bo',label='B')
plot(X_C[:,0],X_C[:,1],'kx',label = 'C')
xlim(0.9*min(X[:,0]),1.1*max(X[:,0]))
ylim(0.9*min(X[:,1]),1.1*max(X[:,1]))

xlabel('Feature 1',fontsize=22,labelpad=5)
ylabel('Feature 2',fontsize=22,labelpad=10)

leg = legend(loc='upper left', ncol = 1, fancybox=True, borderaxespad=0.2)
ltext  = leg.get_texts() 
setp(ltext,fontsize=16)


show()