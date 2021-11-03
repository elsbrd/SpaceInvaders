import random
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.manifold import TSNE
from sklearn.linear_model import LinearRegression

import warnings

from typing import Tuple

warnings.filterwarnings("ignore")

def get_XY(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return data.drop(["score"], axis=1), data.score


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


seed = 42
set_seed(seed)


categorical = ["algorithm", "is_win"]
data = pd.read_csv(r'C:\Users\elisa\PycharmProjects\SpaceInvaders\output2.csv')
train_data, test_data = data.iloc[:-5], data.iloc[-5:]

figure = plt.figure(figsize=(8, 8))
train_data.algorithm.value_counts().plot.pie(
    title="Algorithm",
    autopct="%1.1f%%",
    cmap="viridis",
)
figure.set_facecolor("white")
plt.show()


grid = sns.pairplot(
    train_data,
    hue="is_win",
    diag_kind="hist",
    height=4,
    palette="viridis",
)
grid.fig.suptitle("Time vs. Score", fontsize=12)
plt.show()

X, Y = get_XY(train_data)

X_train, X_valid, Y_train, Y_valid = train_test_split(
    X, Y, test_size=0.2, shuffle=True, random_state=seed)
encoder = OrdinalEncoder()
X_train[categorical] = encoder.fit_transform(X_train[categorical])
X_valid[categorical] = encoder.transform(X_valid[categorical])

XY_train = pd.concat([X_train, Y_train], axis=1)
tsne = TSNE(n_components=2)
train_2d = tsne.fit_transform(XY_train)

figure = plt.figure(figsize=(8, 8))
plt.title("Train data in 2D")
axes = np.split(train_2d, 2, axis=1)
plt.scatter(*axes, color="blue")
plt.show()

model = LinearRegression()
model.fit(X_train, Y_train)
print(model.coef_)


print("R2 score:", model.score(X_valid, Y_valid))

X_test, Y_test = get_XY(test_data)
X_test[categorical] = encoder.transform(X_test[categorical])


Y_pred = model.predict(X_test)
print("R2 score:", model.score(X_test, Y_pred))

stats = pd.DataFrame(
    {
        "$|Y_{true}-Y_{pred}|$": np.abs(Y_test - Y_pred),
        "$|Y_{true}-Y_{mean}|$": np.abs(Y_test - Y_train.mean()),
    }
).reset_index(drop=True)
print(stats)