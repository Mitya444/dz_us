from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///profiles.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route("/")
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)


@app.route('/profile', methods=['GET'])
def get_profile_by_username():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        profile = user.profile
        return jsonify({
            'username': user.username,
            'full_name': profile.full_name,
            'age': profile.age
        })
    else:
        return jsonify({'error': 'Profile not found for the given username'}), 404


def fill_database():
    user_data = [
        {"username": "John Doe", "full_name": "John Doe", "age": 30},
        {"username": "Will Smith", "full_name": "Will Smith", "age": 45},
        {"username": "Eloh Minsk", "full_name": "Eloh Minsk", "age": 25}
    ]
    for user_info in user_data:
        user = User(username=user_info["username"])

        db.session.add(user)

        profile = Profile(full_name=user_info["full_name"],
                          age=user_info["age"],
                          user=user)
        db.session.add(profile)
    db.session.commit()


