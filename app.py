from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Lead
import jwt, datetime, bcrypt, os
import openai

app = Flask(__name__)
CORS(app)

# 🔗 Replace with your DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

SECRET_KEY = "secret123"

# 🔑 Add your OpenAI key
openai.api_key = "YOUR_OPENAI_API_KEY"

with app.app_context():
    db.create_all()

# SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

    user = User(username=data['username'], password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"})

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.checkpw(data['password'].encode(), user.password):
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"})

# ADD LEAD
@app.route('/add-lead', methods=['POST'])
def add_lead():
    token = request.headers.get("Authorization")
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    data = request.json

    lead = Lead(
        user_id=decoded["user_id"],
        name=data['name'],
        email=data['email']
    )

    db.session.add(lead)
    db.session.commit()

    return jsonify({"msg": "Lead added"})

# GET LEADS
@app.route('/leads', methods=['GET'])
def get_leads():
    token = request.headers.get("Authorization")
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    leads = Lead.query.filter_by(user_id=decoded["user_id"]).all()

    return jsonify([
        {"name": l.name, "email": l.email}
        for l in leads
    ])

# 🤖 AI CHAT
@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json['message']

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": msg}]
    )

    return jsonify({
        "reply": response['choices'][0]['message']['content']
    })

if __name__ == "__main__":
    app.run(debug=True)
