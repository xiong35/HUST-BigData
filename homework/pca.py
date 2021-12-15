
import numpy as np

mat = np.array([[1, 2, 3], [3, 4, 5], [5, 4, 3], [0, 2, 4], [1, 3, 5]])

mt_m = np.dot(mat.T, mat)
m_mt = np.dot(mat, mat.T)


eig_mt_m = np.linalg.eig(mt_m)
eig_m_mt = np.linalg.eig(m_mt)

# U, sigma, VT = np.linalg.svd(mat)
#
# print(U)
# print(sigma)
# print(VT)


def pca(dataMat, topNfeat=2):
    mean = dataMat.mean(axis=0)
    meanRemoved = dataMat - mean
    covMat = np.cov(meanRemoved, rowvar=0)
    eigVals, eigVecs = np.linalg.eig(np.mat(covMat))
    eigValInd = np.argsort(eigVals)
    # sort eigvals
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVecs = eigVecs[:, eigValInd]
    lowDimData = meanRemoved*redEigVecs
    reconMat = (lowDimData*redEigVecs.T)+mean
    return lowDimData, reconMat


print(pca(mat))


a = np.dot(np.dot(np.array([
    [0.2977, 0.1591],
    [0.5705, -0.0332],
    [0.5207, -0.7359],
    [0.3226, 0.5104],
    [0.4590, 0.4143],
]),
    np.array([
        [12.3922, 0],
        [0, 3.9285]
    ])),
    np.array([
        [0.4093, 0.5635, 0.7176],
        [0.8160, 0.1259, -0.5642]
    ])
)

print(a)
