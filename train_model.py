import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier

print("--- Starting Advanced Training Process ---")

# 1. Define Paths
path1 = 'phishing_email.csv/phishing_email.csv'
path2 = 'spam_assassin.csv/spam_assassin.csv'
path_enron = 'emails.csv/emails.csv'  # The Enron dataset you just downloaded

dataframes = []

# --- Load Phishing Dataset 1 ---
if os.path.exists(path1):
    print(f"✅ Found Dataset 1: {path1}")
    df1 = pd.read_csv(path1)
    df1 = df1[['text_combined', 'label']] 
    dataframes.append(df1)

# --- Load Spam Assassin ---
if os.path.exists(path2):
    print(f"✅ Found Dataset 2: {path2}")
    df2 = pd.read_csv(path2)
    df2 = df2.rename(columns={'text': 'text_combined', 'target': 'label'})
    df2 = df2[['text_combined', 'label']]
    dataframes.append(df2)

# --- Load ENRON (The "Safe" Brain) ---
if os.path.exists(path_enron):
    print(f"✅ Found Enron Dataset: {path_enron}")
    # We only read a portion to keep the model balanced and fast
    df_enron = pd.read_csv(path_enron, nrows=15000) 
    
    # Enron usually has a 'message' column. We rename it to match.
    df_enron = df_enron.rename(columns={'message': 'text_combined'})
    df_enron['label'] = 0  # Mark all Enron emails as SAFE
    
    df_enron = df_enron[['text_combined', 'label']]
    dataframes.append(df_enron)
else:
    print(f"⚠️ Warning: {path_enron} not found. Safe emails will be missing!")

# 2. Merge and Clean
if not dataframes:
    print("❌ ERROR: No datasets found.")
    exit()

df = pd.concat(dataframes, ignore_index=True)
df = df.dropna() # Remove any empty rows
print(f"📊 Total Combined Rows: {len(df)}")

# 3. Vectorization (Upgraded with N-Grams)
print("Converting text to numbers (Bigram Mode)...")
# ngram_range=(1, 2) helps the AI understand "Hello world" vs "Send password"
vectorizer = TfidfVectorizer(stop_words='english', max_features=10000, ngram_range=(1, 2))
X = vectorizer.fit_transform(df['text_combined'].values.astype('U'))
y = df['label']

# 4. Train XGBoost
print("Training SafePath AI (XGBoost)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# We increased n_estimators for better learning
model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=6, use_label_encoder=False)
model.fit(X_train, y_train)

# 5. Save Files
print("Saving your upgraded smart brain...")
with open('phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("🚀 SUCCESS: New model is ready for testing!")