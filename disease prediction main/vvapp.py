from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()
print("Database connected successfully!")  # Debugging line


# Load and preprocess Diabetes Model
diabetes_dataset = pd.read_csv("data/diabetes.csv")
X_diabetes = diabetes_dataset.drop(columns='Outcome', axis=1)
Y_diabetes = diabetes_dataset['Outcome']

scaler_diabetes = StandardScaler()
X_diabetes = scaler_diabetes.fit_transform(X_diabetes)

X_train_diabetes, X_test_diabetes, Y_train_diabetes, Y_test_diabetes = train_test_split(
    X_diabetes, Y_diabetes, test_size=0.2, stratify=Y_diabetes, random_state=2
)

classifier_diabetes = svm.SVC(kernel='linear')
classifier_diabetes.fit(X_train_diabetes, Y_train_diabetes)

# Load and preprocess Heart Disease Model
heart_data = pd.read_csv("data/heart_dataset.csv")
X_heart = heart_data.drop(columns='target', axis=1)
Y_heart = heart_data['target']

X_train_heart, X_test_heart, Y_train_heart, Y_test_heart = train_test_split(
    X_heart, Y_heart, test_size=0.2, stratify=Y_heart, random_state=2
)

model_heart = LogisticRegression(max_iter=1000)
model_heart.fit(X_train_heart, Y_train_heart)

# Routes for Main Pages
@app.route('/')
def home():
    return render_template('main/home.html')

@app.route('/patient')
def patient_index():
    return render_template('main/patient_index.html')

@app.route('/Registerlogin')
def Registerlogin():
    return render_template('main/Registerlogin.html')

@app.route('/hospital')
def hospital():
    return render_template('main/hospital.html')

# Doctors List Page
@app.route('/doctor')
def doctor_page():
    hospital_name = request.args.get('hospital')
    return render_template('main/doctor.html', hospital=hospital_name) if hospital_name else ("Hospital not found", 404)


# Doctor Profile Page
@app.route('/doctor-profile')
def doctor_profile():
    doctor_name = request.args.get('doctor', 'Unknown Doctor')

    # Dictionary of doctors with details
    doctors = {
        "Dr. Krishnan Kumar": {
            "speciality": "Cardiologist",
            "experience": "15 years",
            "degrees": "MBBS, MD (Cardiology)",
            "about": "Experienced cardiologist with a passion for patient care and treatments.",
            "image": "images/dr_krishnan.jpg"
        },
        "Dr. Shalini K.": {
            "speciality": "Neurologist",
            "experience": "10 years",
            "degrees": "MBBS, MD (Neurology)",
            "about": "Expert in treating neurological disorders with innovative techniques.",
            "image": "images/dr_shalini.jpg"
        },
        "Dr. Aatmaram": {
            "speciality": "Pediatrician",
            "experience": "8 years",
            "degrees": "MBBS, DCH",
            "about": "Caring pediatrician specializing in child health and wellness.",
            "image": "images/dr_aatmaram.jpg"
        },
        "Dr. Govinda": {
            "speciality": "Dentist",
            "experience": "12 years",
            "degrees": "BDS, MDS",
            "about": "Skilled dentist with expertise in dental surgery and oral health care.",
            "image": "images/dr_govinda.jpg"
        }
    }

    # Check if doctor exists in the dictionary
    if doctor_name in doctors:
        return render_template('main/doctor-profile.html', doctor=doctors[doctor_name], doctor_name=doctor_name)
    else:
        return "Doctor not found", 404


# Patient and Health Prediction Routes
@app.route('/index')
def index():
    return render_template('index.html') 

@app.route('/patient-history')
def patient_history():
    return render_template('patient_index.html')

@app.route('/heart-patient-list')
def heart_patient_list():
    return render_template('main/heart-patient-list.html')  

@app.route('/diabetes-patient-list')
def diabetes_patient_list():
    return render_template('main/diabetes-patient-list.html')

@app.route('/diabetes')
def diabetes_page():
    return render_template('diabetes.html')

@app.route('/heart')
def heart_page():
    return render_template('heart.html')

@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    try:
        input_data = [float(request.form[key]) for key in ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']]
        std_data = scaler_diabetes.transform(np.asarray(input_data).reshape(1, -1))
        prediction = classifier_diabetes.predict(std_data)
        result = "The person is diabetic." if prediction[0] == 1 else "The person is not diabetic."
    except ValueError as e:
        result = f"Invalid input data: {e}"
    except Exception as e:
        result = f"Error in processing: {e}"
    return render_template('diabetes.html', prediction_text=result)

@app.route('/predict_heart', methods=['POST'])
def predict_heart():
    try:
        input_data = [float(request.form[key]) for key in ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']]
        prediction = model_heart.predict(np.asarray(input_data).reshape(1, -1))
        result = "The person has heart disease." if prediction[0] == 1 else "The person does not have heart disease."
    except ValueError as e:
        result = f"Invalid input data: {e}"
    except Exception as e:
        result = f"Error in processing: {e}"
    return render_template('heart.html', prediction_text=result)


# User Authentication Routes
# Ensure Database is Connected
if db.is_connected():
    print(" Database connected successfully!")

# Route to serve the Register/Login Page
@app.route('/Registerlogin', methods=['GET'])
def register_login_page():
    return render_template('registerlogin.html')

# Register Route
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    password = request.form.get('password', '').strip()

    if not all([name, email, phone, password]):
        return "<script>alert(' All fields are required!'); window.location.href='/registerlogin';</script>"

    hashed_password = generate_password_hash(password)

    try:
        cursor.execute("INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)", (name, email, phone, hashed_password))
        db.commit()
        return "<script>alert('Registration successful! Login now.'); window.location.href='/registerlogin';</script>"
    except mysql.connector.Error as e:
        return f"<script>alert(' Database Error: {str(e)}'); window.location.href='/registerlogin';</script>"

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not all([email, password]):
        return "<script>alert(' Both email and password are required!'); window.location.href='/registerlogin';</script>"

    try:
        cursor.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return "<script>alert(' Login successful! Redirecting...'); window.location.href='/index';</script>"

        return "<script>alert('Invalid credentials! Try again.'); window.location.href='/registerlogin';</script>"

    except Exception as e:
        return f"<script>alert(' Database Error: {str(e)}'); window.location.href='/registerlogin';</script>"

 

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"<h1>Welcome {session['user_name']}! 🎉</h1><br><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for('register_login_page'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register_login_page'))

# Register Login Page
@app.route('/registerlogin')
def register_login():
    return render_template('registerlogin.html', message=request.args.get('message', ''))



# Contact Form Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Debugging: Print database connection and cursor
    print(f" Debug: Cursor Object → {cursor}")  
    print(f" Debug: Database Connection Status → {db.is_connected()}")  

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
       

        print(f" Received Contact Form Data: {name}, {email}, {message}")

        if not all([name, email, message]):
            print(" Error: Missing form fields!")
            flash("All fields are required!", "error")
            return redirect(url_for('contact'))

        try:
            query = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
            values = (name, email, message)
            
            print(f"Executing Query: {query} | Values: {values}")

            # Check database connection
            if db.is_connected():
                print(" Database is connected inside contact function!")
            else:
                print("Database connection lost!")

            cursor.execute(query, values)
            db.commit()

            print(" Message Sent Successfully!")
            flash("Message sent successfully!", "success")

        except Exception as e:
            db.rollback()
            print(f" Database Error: {str(e)}")
            flash(f"Error: {str(e)}", "error")

        return redirect(url_for('contact'))

    return render_template('main/home.html') 

    

# Appointment Booking Route
@app.route('/book-appointment/<doctor_name>', methods=['GET', 'POST'])
def book_appointment_page(doctor_name):
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        doctor = request.form.get('doctor', doctor_name)
        date = request.form.get('date', '').strip()
        message = request.form.get('message', '').strip()

        print(f"📌 Received Data: Name={name}, Email={email}, Phone={phone}, Doctor={doctor}, Date={date}, Message={message}")

        # Check for missing fields
        if not all([name, email, phone, date]):
            print(" Error: Missing form fields!")
            flash("All fields are required!", "error")
            return redirect(url_for('book_appointment_page', doctor_name=doctor_name))

        try:
            query = "INSERT INTO appointments (name, email, phone, doctor, date, message) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, email, phone, doctor, date, message)

            # Print query before execution
            print(f"Executing Query: {query} | Values: {values}")

            cursor.execute(query, values)
            db.commit()

            print(" Data successfully inserted into database!")  
            flash("Appointment booked successfully!", "success")
            return redirect(url_for('book_appointment_page', doctor_name=doctor_name))

        except Exception as e:
            db.rollback()  
            print(f"Database Error: {str(e)}")  
            flash("Error booking appointment. Please try again.", "error")

    return render_template('main/book-appointment.html', doctor_name=doctor_name)


if __name__ == '__main__':
    app.run(debug=True)