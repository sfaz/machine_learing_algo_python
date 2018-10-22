import numpy as np
import matplotlib.pyplot as plt

TP = lambda y_true, y_pred, label_positive: np.sum(y_pred[np.where(y_true == label_positive)[0]] == label_positive)
TN = lambda y_true, y_pred, label_negative: np.sum(y_pred[np.where(y_true == label_negative)[0]] == label_negative)
FP = lambda y_true, y_pred, label_positive, label_negative: np.sum(y_pred[np.where(y_true == label_negative)[0]] == label_positive)
FN = lambda y_true, y_pred, label_positive, label_negative: np.sum(y_pred[np.where(y_true == label_positive)[0]] == label_negative)

def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def precision(y_true, y_pred, label_positive=1, label_negative=0):
    if TP(y_true, y_pred, label_positive) == 0:
        return 0

    return TP(y_true, y_pred, label_positive) / (TP(y_true, y_pred, label_positive) + FP(y_true, y_pred, label_positive, label_negative))

def recall(y_true, y_pred, label_positive=1, label_negative=0):
    if TP(y_true, y_pred, label_positive) == 0:
        return 0

    return TP(y_true, y_pred, label_positive) / (TP(y_true, y_pred, label_positive) + FN(y_true, y_pred, label_positive, label_negative))

def f_score(y_true, y_pred, beta, label_positive=1, label_negative=0):
    p = precision(y_true, y_pred, label_positive, label_negative)
    r = recall(y_true, y_pred, label_positive, label_negative)
    if p * r == 0:
        return 0

    return (1 + beta ** 2) * p * r / (beta ** 2 * p + r)

def confusion_matrix(y_true, y_pred, labels=[]):
    class_number = len(labels)

    matrix = np.zeros((class_number, class_number))
    for r in range(class_number):
        for c in range(class_number):
            matrix[r, c] = np.sum(y_pred[np.where(y_true == labels[r])[0]] == labels[c])

    return matrix

def roc_curve(y_true, y_score, label_positive=1, label_negative=0):
    TPR = []
    FPR = []

    scores = np.sort(y_score.flatten())
    for score in scores:
        y_pred = y_score > score

        if TP(y_true, y_pred, label_positive) == 0:
            TPR.append(0)
        else:
            TPR.append(TP(y_true, y_pred, label_positive) / (TP(y_true, y_pred, label_positive) + FN(y_true, y_pred, label_positive, label_negative)))

        if FP(y_true, y_pred, label_positive, label_negative) == 0:
            FPR.append(0)
        else:
            FPR.append(FP(y_true, y_pred, label_positive, label_negative) / (FP(y_true, y_pred, label_positive, label_negative) + TN(y_true, y_pred, label_negative)))

    plt.plot(FPR, TPR)
    plt.show()

def auc(y_true, y_score):
    rank = y_score[:, 0].argsort()
    positives = np.where(y_true == 1)[0]
    rank_sum = np.sum([np.argwhere(rank == positive)[0][0] + 1 for positive in positives])

    positive_number = np.sum(y_true == 1)
    negative_number = np.sum(y_true == 0)
    
    return (rank_sum - positive_number * (positive_number + 1) / 2) / (positive_number * negative_number)

def r2_score(y_true, y_pred):
    return 1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)

def silhouette_coefficient(X, y):
    data_number = X.shape[0]

    s = []
    for i in range(data_number):
        distances = np.linalg.norm(X[i] - X, axis=1)
        
        bs = []
        for cluster in np.unique(y):
            if y[i] == cluster:
                a = np.sum(distances[np.where(y == cluster)[0]]) / (len(np.where(y == cluster)[0]) - 1)
            else:
                bs.append(np.mean(distances[np.where(y == cluster)[0]]))
        b = np.min(bs)

        s.append((b - a) / max(a, b))
    
    return np.mean(s)