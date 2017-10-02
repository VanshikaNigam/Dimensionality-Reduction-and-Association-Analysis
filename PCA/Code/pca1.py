import numpy as np
from numpy import linalg as LA
import pandas as pd
import csv
from sklearn.decomposition import TruncatedSVD
import time
from sklearn.manifold import TSNE
from numpy import inf


test=np.loadtxt('pca_c.txt', delimiter="\t",dtype='str').shape[1]

initial = np.loadtxt('pca_c.txt', delimiter="\t",dtype='str')
lastcol= initial[:,-1]
matrix = np.loadtxt('pca_c.txt', delimiter="\t",usecols=range(test-1))
row=len(matrix)
t=np.asmatrix(lastcol, dtype='U')
t=np.transpose(t)


matrix_t=np.transpose(matrix)
mean=np.mean(matrix,axis=0)

normalize=matrix-mean
#normalize_t=np.transpose(normalize)
col= normalize.shape[1];
#print(normalize.shape)




matrix_calc=np.matrix(normalize[0,:])
#matrix_calc=np.transpose(matrix)
#matrix=np.transpose(matrix)
print(matrix_calc.shape)

for i in range(1,col):
	mat_col=np.matrix(normalize[i,:])
	
	matrix_calc =np.vstack((matrix_calc,mat_col))

print(matrix_calc.shape)


covmat=np.cov(matrix_calc)
#print("covmat",covmat.shape)


eigvals, eigvecs = LA.eig(covmat)

#print(eigvals)
#print(eigvecs)

idx = eigvals.argsort()[::-1]   
eigvecs = eigvecs[idx]
eigvecs = eigvecs[:,idx]

#print(eigvals)
#print(eigvecs)

w=eigvecs[:,:2]
w_trans=np.transpose(w)
matrix_transpose=np.transpose(matrix)

ans = np.dot(w_trans,matrix_transpose)
ans= np.transpose(ans)
#print(ans)

print("ans", ans.shape)
print("t", t.shape)
temp=np.concatenate((ans,t),axis=1)

 
df=pd.DataFrame(temp)
df.to_csv("pca_c_file.csv")


svd= TruncatedSVD(n_components=2)
svd_result=svd.fit_transform(matrix)
svd_result=np.concatenate((svd_result,t),axis=1)
df_svd=pd.DataFrame(svd_result)
df.to_csv("svd_c_file.csv")


#print(np.isinf(matrix).any())
tsne=TSNE(n_components=2)
np.set_printoptions(suppress=True)
tsne_result=tsne.fit_transform(matrix)
tsne_result=np.concatenate((tsne_result,t),axis=1)
df_svd=pd.DataFrame(svd_result)
df.to_csv("tsne_c_file.csv")
#print(tsne_result)



