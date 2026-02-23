from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
# CORS is essential so your Chrome Extension can talk to this Python server
CORS(app) 

# 1. Load the saved "Brain" (Model) and "Dictionary" (Vectorizer)
# Make sure these .pkl files are in the same folder as app.py
try:
    model = pickle.load(open('phishing_model.pkl', 'rb'))
    vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
    print("✅ ML Model and Vectorizer loaded successfully.")
except FileNotFoundError:
    print("❌ ERROR: Could not find .pkl files. Did you run train_model.py first?")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    email_content = data.get('text', '')
    
    # Handle empty input
    if not email_content.strip():
        return jsonify({
            'is_phishing': False,
            'confidence': 0,
            'message': 'No text provided'
        })
    
    # 2. Transform the pasted text using the vectorizer
    vectorized_text = vectorizer.transform([email_content])
    
    # 3. Calculate probabilities
    # predict_proba returns a list like [prob_of_safe, prob_of_phishing]
    probabilities = model.predict_proba(vectorized_text)[0]
    
    # FIX: Convert numpy float32 to standard Python float using .item()
    phishing_prob = probabilities[1].item() 

    # 4. SENSITIVITY THRESHOLD (The "Paranoia" Filter)
    # 0.50 = Default (very sensitive)
    # 0.75 = Recommended (only alerts if highly suspicious)
    # 0.90 = Strict (only alerts on obvious scams)
    threshold = 0.80 
    
    # If the probability is higher than our threshold, mark as phishing
    is_phishing = True if phishing_prob >= threshold else False
    confidence_score = round(phishing_prob * 100, 2)

    # Log to your terminal so you can see what the AI is thinking
    print(f"--- New Prediction ---")
    print(f"Score: {confidence_score}% | Result: {'PHISHING' if is_phishing else 'SAFE'}")

    # FIX: Explicitly cast values to standard Python types for JSON serialization
    return jsonify({
        'is_phishing': bool(is_phishing),
        'confidence': float(confidence_score),
        'threshold_used': float(threshold)
    })

if __name__ == '__main__':
    # Using debug=True means the server restarts automatically when you save changes
    app.run(port=5000, debug=True)