
# v2_ds_ml.py — generates ML/DL pages for v2.html
import sys, json

sys.path.insert(0, r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
import v2_python  # Ensure we have the helpers

card = v2_python.card
section_header = v2_python.section_header
page_nav = v2_python.page_nav
pages = {}

# ─── PAGE: ML Preprocessing ───────────────────────────────────────────────────
def sk_pre_page():
    body = section_header("Data Preprocessing","🤖 Scikit-Learn","Advanced","Hands-On Machine Learning")
    body += "<p>Scikit-Learn estimators require numeric, scale-normalized data without NaNs. The <code>preprocessing</code> and <code>impute</code> modules provide transformers for this.</p>"
    body += "<h2>Imputation</h2><div class='method-grid'>"
    body += card("SimpleImputer(strategy)", "Impute missing values", "Transformer",
        "Strategies: 'mean', 'median', 'most_frequent', 'constant'.",
        [("strategy","str","'mean'","Imputation strategy"),("fill_value","any","None","Value for 'constant' strategy")],
        examples=[("","from sklearn.impute import SimpleImputer\\nimp = SimpleImputer(strategy='mean')\\nX_filled = imp.fit_transform(X)","")])
    body += card("KNNImputer(n_neighbors)", "Impute using K-Nearest Neighbors", "Transformer",
        "More accurate than SimpleImputer for correlated features, but slower.",
        examples=[("","from sklearn.impute import KNNImputer\\nimp = KNNImputer(n_neighbors=5)\\nX_filled = imp.fit_transform(X)","")])
    body += "</div>"

    body += "<h2>Encoding Categorical Features</h2><div class='method-grid'>"
    body += card("OneHotEncoder(handle_unknown)", "One-hot encode categorical features", "Transformer",
        "Converts categories to one-hot (dummy) vectors. handle_unknown='ignore' prevents errors on new unseen categories.",
        examples=[("","from sklearn.preprocessing import OneHotEncoder\\nohe = OneHotEncoder(sparse_output=False)\\nX_cat = ohe.fit_transform(X[['color']])","")])
    body += card("OrdinalEncoder()", "Encode features as integer arrays", "Transformer",
        "Maps categories to [0, n_categories - 1].",
        examples=[("","from sklearn.preprocessing import OrdinalEncoder\\nenc = OrdinalEncoder()\\nX_cat = enc.fit_transform(X[['size']])","")])
    body += card("LabelEncoder()", "Encode target labels", "Transformer",
        "Only for 1D target variables (y), NOT for feature matrices (X).",
        examples=[("","from sklearn.preprocessing import LabelEncoder\\nle = LabelEncoder()\\ny_enc = le.fit_transform(['cat', 'dog', 'cat'])","[0 1 0]")])
    body += "</div>"

    body += "<h2>Scaling &amp; Normalization</h2><div class='method-grid'>"
    body += card("StandardScaler()", "Standardize features (z-score)", "Transformer",
        "Removes mean and scales to unit variance: z = (x - u) / s.",
        examples=[("","from sklearn.preprocessing import StandardScaler\\nscl = StandardScaler()\\nX_scaled = scl.fit_transform(X)","")])
    body += card("MinMaxScaler(feature_range)", "Scale features to a range", "Transformer",
        "Scales data explicitly to [0, 1] by default. Sensitive to outliers.",
        examples=[("","from sklearn.preprocessing import MinMaxScaler\\nscl = MinMaxScaler()\\nX_scaled = scl.fit_transform(X)","")])
    body += card("RobustScaler()", "Scale features using robust statistics", "Transformer",
        "Centers median and scales by IQR (Interquartile Range). Ignores extreme outliers.",
        examples=[("","from sklearn.preprocessing import RobustScaler\\nscl = RobustScaler()\\nX_scaled = scl.fit_transform(X)","")])
    body += "</div>"
    body += page_nav("#sns-grid","Seaborn","#sk-pipe","Pipelines")
    return body

pages["sk-pre"] = sk_pre_page()

# ─── PAGE: ML Pipelines & ColumnTransformer ───────────────────────────────────
def sk_pipe_page():
    body = section_header("Pipelines & ColumnTransformer","🤖 Scikit-Learn","Advanced","Hands-On Machine Learning")
    body += "<p>Pipelines sequence data processing steps and an estimator to prevent data leakage during Cross-Validation.</p>"
    
    body += "<h2>Pipeline Automation</h2><div class='method-grid'>"
    body += card("Pipeline(steps)", "Chain multiple estimators into one", "Pipeline",
        "Steps is a list of (name, transformer) tuples. Last step must be an estimator (model).",
        examples=[("","from sklearn.pipeline import Pipeline\\nfrom sklearn.preprocessing import StandardScaler\\nfrom sklearn.svm import SVC\\n\\npipe = Pipeline([\\n    ('scaler', StandardScaler()),\\n    ('svc', SVC())\\n])\\npipe.fit(X_train, y_train)\\npipe.score(X_test, y_test)","")])
    body += card("make_pipeline(*steps)", "Construct Pipeline without naming", "Pipeline",
        "Shorthand that auto-generates names (e.g. 'standardscaler', 'svc').",
        examples=[("","from sklearn.pipeline import make_pipeline\\npipe = make_pipeline(StandardScaler(), SVC())","")])
    body += "</div>"
    
    body += "<h2>Heterogeneous Data (ColumnTransformer)</h2><div class='method-grid'>"
    body += card("ColumnTransformer(transformers)", "Apply different transformers to columns", "ColumnTransformer",
        "Allows applying StandardScaler to numeric columns and OneHotEncoder to categorical columns in parallel.",
        [("transformers","list","—","List of (name, transformer, columns) tuples")],
        examples=[("","from sklearn.compose import ColumnTransformer\\n\\nnum_cols = ['age', 'income']\\ncat_cols = ['city', 'browser']\\n\\npreprocessor = ColumnTransformer(transformers=[\\n    ('num', StandardScaler(), num_cols),\\n    ('cat', OneHotEncoder(), cat_cols)\\n])\\n\\n# Combine with pipeline:\\nfull_pipe = make_pipeline(preprocessor, SVC())","")])
    body += "</div>"
    body += page_nav("#sk-pre","Preprocessing","#sk-models","Classification Models")
    return body

pages["sk-pipe"] = sk_pipe_page()

# ─── Assemble into master dict ────────────────────────────────────────────────
# Load existing and append
try:
    with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
except Exception:
    existing = {}

existing.update(pages)

with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "w", encoding="utf-8") as f:
    json.dump(existing, f)

print(f"v2_ds_ml.py complete. Added {len(pages)} pages.")
