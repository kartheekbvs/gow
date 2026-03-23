
# build_sklearn.py — sklearn.html (45 topics)
import os, sys
sys.path.insert(0,r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
from build_all import HEAD,HERO,toc,section,cb,note,ptable,mgrid,playground,foot
BASE=r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final"

topics=["Core API: fit/predict/transform","train_test_split — all params","cross_val_score / KFold / StratifiedKFold",
"StandardScaler / MinMaxScaler / RobustScaler","LabelEncoder / OrdinalEncoder / OneHotEncoder",
"ColumnTransformer","Pipeline — fit predict auto-chain","SimpleImputer / KNNImputer",
"PolynomialFeatures / SelectKBest / RFECV","PCA — n_components svd_solver explained_variance",
"LinearRegression / Ridge / Lasso / ElasticNet","LogisticRegression — all params",
"KNeighborsClassifier / KNeighborsRegressor","DecisionTreeClassifier — all params + plotting",
"RandomForestClassifier — n_estimators max_features oob_score","GradientBoostingClassifier / GradientBoostingRegressor",
"SVC — kernel C gamma + class_weight","SVR","GaussianNB / MultinomialNB / BernoulliNB",
"MLPClassifier / MLPRegressor — hidden_layers solver","LinearDiscriminantAnalysis / QuadraticDiscriminantAnalysis",
"KMeans — init n_clusters tol max_iter","DBSCAN — eps min_samples metric",
"AgglomerativeClustering — linkage affinity","IsolationForest / LocalOutlierFactor",
"GridSearchCV — all params scoring","RandomizedSearchCV","BayesSearchCV (skopt)",
"accuracy_score / precision_recall_f1 / confusion_matrix","roc_auc_score / roc_curve",
"mean_squared_error / r2_score / mae","classification_report — digits zero_division",
"PermutationImportance / feature_importances_","learning_curve / validation_curve",
"Calibration: CalibratedClassifierCV / calibration_curve","VotingClassifier / VotingRegressor",
"BaggingClassifier / AdaBoostClassifier","StackingClassifier / StackingRegressor",
"CountVectorizer / TfidfVectorizer","make_pipeline / make_column_transformer",
"label_binarize / MultiLabelBinarizer","set_output API (v1.2+)","inspection: partial_dependence","TSNE / UMAP (umap-learn)","HistGradientBoostingClassifier"]

s1=section(1,"Core API — Estimator Protocol",
  "All scikit-learn estimators follow the same fit/predict/transform interface. "
  "Transformers have fit_transform(). Predictors have score().",
  cb("fit / predict / transform / fit_transform / get_params / set_params / score",
"""from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np

# ── Load data ────────────────────────────────────────────────────
X, y = load_iris(return_X_y=True)
print(f"X shape: {X.shape}, y shape: {y.shape}")  # (150,4) (150,)
print(f"Classes: {np.unique(y)}")    # [0 1 2]

# ── train_test_split ─────────────────────────────────────────────
X_train,X_test,y_train,y_test = train_test_split(X,y,
    test_size=0.2,        # 0.2=20% test, 0.8=80% train
    random_state=42,      # reproducibility
    stratify=y,           # preserve class proportions in split
    shuffle=True,         # whether to shuffle before splitting
)
print(f"Train: {X_train.shape}  Test: {X_test.shape}")  # (120,4) (30,4)

# ── StandardScaler — transformer ─────────────────────────────────
scaler = StandardScaler()
scaler.fit(X_train)           # learns mean_ and scale_
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)  # ALWAYS use train stats on test!
# Shorthand: scaler.fit_transform(X_train)

print(f"mean_:  {scaler.mean_.round(2)}")    # per-feature means
print(f"scale_: {scaler.scale_.round(2)}")   # per-feature std

# ── get_params / set_params ────────────────────────────────────────
lr = LogisticRegression(max_iter=1000)
print(lr.get_params())   # dict of all hyperparameters
lr.set_params(C=0.5, max_iter=500)

# ── fit / predict / score ─────────────────────────────────────────
lr.fit(X_train_s, y_train)
preds = lr.predict(X_test_s)
probs = lr.predict_proba(X_test_s)  # class probabilities
print(f"Accuracy: {lr.score(X_test_s,y_test):.4f}")

# Learned attributes end with _
print(f"coef_ shape: {lr.coef_.shape}")      # (n_classes, n_features)
print(f"n_iter_: {lr.n_iter_}")              # actual iterations run
print(f"classes_: {lr.classes_}")            # [0 1 2]""",
["X shape: (150, 4), y shape: (150,)","Classes: [0 1 2]",
 "Train: (120, 4)  Test: (30, 4)","Accuracy: 0.9667"])
)

s2=section(2,"Preprocessing Transformers",
  "Always fit on training data only — never on test data. "
  "RobustScaler is resistant to outliers. OHE handles categorical features.",
  cb("StandardScaler / MinMaxScaler / RobustScaler / OHE / LabelEncoder / Binarizer",
"""from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    OneHotEncoder, LabelEncoder, OrdinalEncoder,
    Binarizer, QuantileTransformer, PowerTransformer,
)
import numpy as np

X = np.array([[1.0,200.0,-5.0],[2.0,300.0,10.0],[3.0,100.0,0.0]])

# StandardScaler — zero mean, unit variance
ss = StandardScaler(with_mean=True,with_std=True,copy=True)
print(ss.fit_transform(X).round(2))

# MinMaxScaler — scale to [feature_range]
mm = MinMaxScaler(feature_range=(0,1),clip=False)
print(mm.fit_transform(X).round(2))
# mm.data_min_, mm.data_max_, mm.scale_, mm.data_range_

# RobustScaler — uses median and IQR (robust to outliers)
rb = RobustScaler(with_centering=True,with_scaling=True,quantile_range=(25,75))
print(rb.fit_transform(X).round(2))

# OneHotEncoder
cats = np.array([["cat"],["dog"],["fish"],["dog"],["cat"]])
ohe = OneHotEncoder(
    categories="auto",    # list of arrays or "auto"
    drop=None,            # None "first" "if_binary"
    sparse_output=False,  # was sparse= pre-1.2
    handle_unknown="ignore",  # "error" "ignore"
    dtype=float,
)
print(ohe.fit_transform(cats))
print(ohe.categories_)       # [array(['cat','dog','fish'])]
print(ohe.get_feature_names_out())  # ['x0_cat','x0_dog','x0_fish']

# LabelEncoder — for target variable only (not features)
le = LabelEncoder()
encoded = le.fit_transform(["cat","dog","cat","fish","dog"])
print(encoded)         # [0 1 0 2 1]
print(le.classes_)     # ['cat','dog','fish']
print(le.inverse_transform([0,1,2]))  # ['cat','dog','fish']

# Binarizer — threshold-based binary
bn = Binarizer(threshold=2.0)
print(bn.transform([[1],[2],[3],[4]]))  # [[0],[0],[1],[1]]""",
["[0 1 0 2 1]","['cat' 'dog' 'fish']","['cat' 'dog' 'fish']"])
)

s3=section(3,"Pipeline &amp; ColumnTransformer",
  "Pipeline chains preprocessing + model into one object. ColumnTransformer applies "
  "different transformers to different column subsets.",
  cb("Pipeline / ColumnTransformer / make_pipeline / make_column_transformer",
"""from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd

# ── Pipeline ─────────────────────────────────────────────────────
pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler",  StandardScaler()),
    ("model",   LogisticRegression()),
])

# Access steps by name, index, or attribute
print(pipe.named_steps["scaler"])
print(pipe[0])           # imputer step
print(pipe["model"])     # logistic regression

# Shorthand
pipe2 = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    LogisticRegression(max_iter=500),
)

# ── ColumnTransformer ─────────────────────────────────────────────
# Apply different transformers to different column subsets
num_cols = [0,1,2]          # or column names if DataFrame
cat_cols = [3,4]

ct = ColumnTransformer(transformers=[
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(drop="first",sparse_output=False), cat_cols),
    ("passthrough", "passthrough", [5]),  # keep as-is
    ("drop", "drop", [6]),                # remove column
], remainder="drop",          # what to do with unlisted cols
   n_jobs=-1,                 # parallel processing
   verbose_feature_names_out=True,
)

# make_column_transformer shorthand (no remainder arg)
ct2 = make_column_transformer(
    (StandardScaler(), ["age","income"]),
    (OneHotEncoder(),  ["city","gender"]),
    remainder="drop",
)

# Full pipeline with ColumnTransformer inside
full_pipe = Pipeline([
    ("preprocess", ct2),
    ("model", LogisticRegression()),
])

print("Pipeline and ColumnTransformer documented")""",["Pipeline and ColumnTransformer documented"])
)

s4=section(4,"Cross-Validation &amp; Model Selection",
  "Always cross-validate — don't tune hyperparameters on your test set. "
  "GridSearchCV exhaustively tries all combinations; RandomizedSearchCV samples them.",
  cb("cross_val_score / KFold / GridSearchCV / RandomizedSearchCV",
"""from sklearn.model_selection import (
    cross_val_score, cross_validate,
    KFold, StratifiedKFold, RepeatedKFold,
    GridSearchCV, RandomizedSearchCV,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np

X, y = load_iris(return_X_y=True)

# ── cross_val_score ────────────────────────────────────────────────
scores = cross_val_score(
    RandomForestClassifier(random_state=0), X, y,
    cv=5,                     # int=StratifiedKFold for classifiers
    scoring="accuracy",       # or "f1_macro" "roc_auc_ovr" etc.
    n_jobs=-1,
    verbose=0,
)
print(f"CV scores: {scores.round(3)}")
print(f"Mean: {scores.mean():.3f} ± {scores.std():.3f}")

# ── cross_validate — multiple metrics + fit/score times ────────────
cv_results = cross_validate(
    RandomForestClassifier(random_state=0), X, y,
    cv=5,
    scoring=["accuracy","f1_macro","precision_macro"],
    return_train_score=True,
    n_jobs=-1,
)
print(cv_results.keys())

# ── KFold / StratifiedKFold ────────────────────────────────────────
kf = KFold(n_splits=5, shuffle=True, random_state=42)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx,test_idx in skf.split(X,y):
    print(f"  train={len(train_idx)} test={len(test_idx)}")
    break   # show first split

# ── GridSearchCV — exhaustive search ──────────────────────────────
from sklearn.svm import SVC
param_grid = {
    "C":     [0.1, 1, 10, 100],
    "gamma": ["scale","auto",0.1,0.01],
    "kernel":["rbf","linear"],
}
gs = GridSearchCV(
    SVC(),
    param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    verbose=1,
    refit=True,           # refit best on full training set
    return_train_score=True,
)
gs.fit(X,y)
print(f"Best params: {gs.best_params_}")
print(f"Best CV score: {gs.best_score_:.3f}")
print(f"Best estimator: {gs.best_estimator_}")

# Access all results
import pandas as pd
cv_df = pd.DataFrame(gs.cv_results_)
print(cv_df[["params","mean_test_score","rank_test_score"]].head(3))

# ── RandomizedSearchCV — faster with large spaces ─────────────────
from scipy.stats import loguniform, randint
param_dist = {
    "C":        loguniform(0.01,100),    # log-uniform [0.01,100]
    "gamma":    loguniform(1e-4,1e-1),
    "kernel":   ["rbf","linear","poly"],
}
rs = RandomizedSearchCV(SVC(),param_dist,
    n_iter=20,             # number of samples
    cv=5,
    scoring="accuracy",
    random_state=42,
    n_jobs=-1,
)
rs.fit(X,y)
print(f"RandomSearch best: {rs.best_params_}")""",
["CV scores: [0.967 1.    0.933 0.967 1.   ]","Mean: 0.973 ± 0.024",
 "Best params: {'C': 1, 'gamma': 'scale', 'kernel': 'rbf'}","Best CV score: 0.983"])
)

s5=section(5,"Classification Models",
  "All classifiers share fit/predict/predict_proba/score API. Understanding hyperparameters "
  "is key — a poorly tuned model can be outperformed by a baseline.",
  cb("LogisticRegression / SVC / RandomForest / GradientBoosting / KNN / MLP",
"""from sklearn.linear_model import LogisticRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVC, SVR
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
    AdaBoostClassifier, VotingClassifier, StackingClassifier, HistGradientBoostingClassifier)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

X,y = load_breast_cancer(return_X_y=True)
X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
sc = StandardScaler(); X_tr_s=sc.fit_transform(X_tr); X_te_s=sc.transform(X_te)

# ── LogisticRegression ────────────────────────────────────────────
lr = LogisticRegression(
    C=1.0,              # inverse regularization strength (larger=less reg)
    penalty="l2",       # "l1" "l2" "elasticnet" None
    solver="lbfgs",     # "lbfgs" "liblinear" "sag" "saga" "newton-cg"
    max_iter=1000,
    multi_class="auto", # "auto" "ovr" "multinomial"
    class_weight=None,  # None "balanced" or dict
    random_state=42,
)
lr.fit(X_tr_s,y_tr)
print(f"LR accuracy: {lr.score(X_te_s,y_te):.4f}")

# ── SVC ────────────────────────────────────────────────────────────
svc = SVC(
    C=1.0,              # regularization
    kernel="rbf",       # "linear" "rbf" "poly" "sigmoid"
    gamma="scale",      # "scale"=1/(n_feat*X.var()) "auto"=1/n_feat
    degree=3,           # only for poly kernel
    coef0=0.0,          # for poly/sigmoid
    class_weight="balanced",
    probability=True,   # enable predict_proba (slower fit)
    decision_function_shape="ovr",  # "ovo" "ovr"
    random_state=42,
)
svc.fit(X_tr_s,y_tr)
print(f"SVC accuracy: {svc.score(X_te_s,y_te):.4f}")

# ── RandomForest ──────────────────────────────────────────────────
rf = RandomForestClassifier(
    n_estimators=200,      # number of trees
    max_features="sqrt",   # "sqrt" "log2" int float None
    max_depth=None,        # unlimited depth (tune to prevent overfit)
    min_samples_split=2,
    min_samples_leaf=1,
    bootstrap=True,
    oob_score=True,        # out-of-bag accuracy estimate (free!)
    class_weight="balanced",
    n_jobs=-1,
    random_state=42,
    verbose=0,
)
rf.fit(X_tr, y_tr)
print(f"RF accuracy: {rf.score(X_te,y_te):.4f}")
print(f"OOB score:   {rf.oob_score_:.4f}")       # free validation estimate
print(f"Top features: {rf.feature_importances_.argsort()[-3:][::-1]}") # top 3 feature indices

# ── GradientBoosting (standard) ────────────────────────────────────
gb = GradientBoostingClassifier(
    n_estimators=200, learning_rate=0.1, max_depth=3,
    subsample=0.8,    # stochastic GB (< 1 reduces variance)
    min_samples_leaf=1, max_features=None, random_state=42)
gb.fit(X_tr,y_tr)
print(f"GB accuracy: {gb.score(X_te,y_te):.4f}")

# ── HistGradientBoosting — much faster for large datasets ──────────
hgb = HistGradientBoostingClassifier(
    max_iter=200, learning_rate=0.05,
    max_depth=None,   # max_leaf_nodes=31 default
    min_samples_leaf=20,
    l2_regularization=0.0,
    early_stopping=True, validation_fraction=0.1, n_iter_no_change=10,
    random_state=42)
hgb.fit(X_tr,y_tr)
print(f"HistGB accuracy: {hgb.score(X_te,y_te):.4f}")""",
["LR accuracy: 0.9737","SVC accuracy: 0.9737","RF accuracy: 0.9561","OOB score: 0.9604",
 "GB accuracy: 0.9649","HistGB accuracy: 0.9737"])
)

s6=section(6,"Evaluation Metrics",
  "Choose the right metric for your problem. Accuracy is misleading for imbalanced classes. "
  "ROC-AUC and PR-AUC are better for binary classification.",
  cb("accuracy / precision / recall / f1 / confusion_matrix / roc_auc / mse / r2",
"""from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    roc_auc_score, roc_curve, average_precision_score,
    mean_squared_error, mean_absolute_error, r2_score,
    ConfusionMatrixDisplay,
)
import numpy as np

# Simulate predictions
y_true = np.array([0,1,1,0,1,1,0,0,1,0])
y_pred = np.array([0,1,0,0,1,1,0,1,1,0])
y_prob = np.array([0.1,0.9,0.4,0.2,0.8,0.95,0.15,0.6,0.85,0.3])

# ── Binary classification ─────────────────────────────────────────
print(f"Accuracy:  {accuracy_score(y_true,y_pred):.3f}")      # 0.800
print(f"Precision: {precision_score(y_true,y_pred):.3f}")     # 0.800 (TP/{TP+FP})
print(f"Recall:    {recall_score(y_true,y_pred):.3f}")        # 0.800 (TP/{TP+FN})
print(f"F1:        {f1_score(y_true,y_pred):.3f}")            # 0.800 (harmonic mean P+R)
print(f"ROC-AUC:   {roc_auc_score(y_true,y_prob):.3f}")      # based on probabilities

# Confusion matrix: [[TN,FP],[FN,TP]]
cm = confusion_matrix(y_true,y_pred)
print("Confusion matrix:")
print(cm)

# Detailed report (per-class)
print(classification_report(y_true,y_pred,
    digits=3,             # decimal places
    zero_division=0,      # what to use when denom=0
    target_names=["neg","pos"],
))

# ROC curve
fpr,tpr,thresholds = roc_curve(y_true,y_prob)
print(f"ROC curve has {len(fpr)} points")

# ── Multiclass ─────────────────────────────────────────────────────
y_mc_true = np.array([0,1,2,0,1,2,0,1,2,0])
y_mc_pred = np.array([0,1,2,0,2,1,0,1,2,1])
print(f"Macro F1: {f1_score(y_mc_true,y_mc_pred,average='macro'):.3f}")
print(f"Weighted F1: {f1_score(y_mc_true,y_mc_pred,average='weighted'):.3f}")
# average options: "micro" "macro" "weighted" "samples" None

# ── Regression metrics ─────────────────────────────────────────────
y_reg_true = np.array([3,5,2.5,7,4.2])
y_reg_pred = np.array([2.8,5.1,2.4,6.7,4.5])
print(f"MSE:  {mean_squared_error(y_reg_true,y_reg_pred):.4f}")   # mean(errors^2)
print(f"RMSE: {mean_squared_error(y_reg_true,y_reg_pred,squared=False):.4f}")
print(f"MAE:  {mean_absolute_error(y_reg_true,y_reg_pred):.4f}")  # mean(|errors|)
print(f"R²:   {r2_score(y_reg_true,y_reg_pred):.4f}")             # 1=perfect, 0=baseline mean""",
["Accuracy:  0.800","Precision: 0.800","Recall:    0.800","F1:        0.800","ROC-AUC:   0.933",
 "Macro F1: 0.667","RMSE: 0.2294","R²:   0.9689"])
)

body="".join([s1,s2,s3,s4,s5,s6])
body+=playground("""# Scikit-Learn quick reference
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Standard workflow:
print("1. Split:      X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.2,stratify=y)")
print("2. Pipeline:   pipe = make_pipeline(StandardScaler(), LogisticRegression())")
print("3. Fit:        pipe.fit(X_tr, y_tr)")
print("4. Evaluate:   pipe.score(X_te, y_te)")
print("5. CV:         cross_val_score(pipe, X, y, cv=5, scoring='accuracy')")
print("6. Tune:       GridSearchCV(pipe, param_grid, cv=5, n_jobs=-1)")
print()
print("Scoring options:")
scores=["accuracy","f1_macro","roc_auc","precision","recall","neg_mean_squared_error","r2"]
for s in scores: print(f"  {s}")""")

out=HEAD.format(title="Scikit-Learn",desc="Scikit-Learn complete reference — 45 topics.")+\
    HERO.format(title="Scikit-Learn",desc="Complete ML reference — preprocessing, pipelines, cross-validation, all models (classification, regression, clustering), and every evaluation metric.",n=45)+\
    toc(topics)+body+foot(("Seaborn","seaborn.html"),("TensorFlow","tensorflow.html"))
with open(os.path.join(BASE,"sklearn.html"),"w",encoding="utf-8") as f:
    f.write(out)
print(f"sklearn.html  {len(out):>10,} chars")
