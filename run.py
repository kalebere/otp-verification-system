from flask import Flask, request, render_template_string
from flask_mail import Mail, Message
from dotenv import load_dotenv
import random
import os

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Mail Configuration

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# Store OTP
generated_otp = ""

# Home Page

@app.route('/')
def home():

    with open("index.html", "r") as file:
        return render_template_string(file.read())

# Send OTP Route

@app.route('/send-otp', methods=['POST'])
def send_otp():

    global generated_otp

    email = request.form['email']

    # Generate OTP
    generated_otp = str(random.randint(100000, 999999))

    # Create Mail
    msg = Message(
        'Your OTP Code',
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[email]
    )

    msg.body = f'Your OTP is: {generated_otp}'

    # Send Mail
    mail.send(msg)

    # OTP Verification Page
    return '''

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Verify OTP</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Poppins,sans-serif;
}

body{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#020617,#0f172a,#1e293b);
}

.container{

    width:420px;
    padding:40px;

    border-radius:28px;

    background:rgba(255,255,255,0.08);

    border:1px solid rgba(255,255,255,0.15);

    backdrop-filter:blur(18px);

    box-shadow:0 10px 35px rgba(0,0,0,0.4);

    text-align:center;

    color:white;

}

.logo{

    width:90px;
    height:90px;

    margin:auto;
    margin-bottom:25px;

    border-radius:24px;

    background:linear-gradient(135deg,#2563eb,#7c3aed);

    display:flex;
    justify-content:center;
    align-items:center;

    font-size:34px;
    font-weight:bold;

}

h1{
    margin-bottom:12px;
    font-size:32px;
}

p{
    color:#cbd5e1;
    margin-bottom:30px;
}

.success{

    background:rgba(34,197,94,0.15);

    color:#4ade80;

    padding:14px;

    border-radius:14px;

    margin-bottom:25px;

    font-weight:600;

}

input{

    width:100%;

    padding:16px;

    border:none;
    outline:none;

    border-radius:16px;

    background:rgba(255,255,255,0.08);

    border:1px solid rgba(255,255,255,0.1);

    color:white;

    margin-bottom:20px;

    font-size:15px;

}

input::placeholder{
    color:#94a3b8;
}

button{

    width:100%;

    padding:16px;

    border:none;

    border-radius:16px;

    background:linear-gradient(135deg,#2563eb,#7c3aed);

    color:white;

    font-size:16px;
    font-weight:600;

    cursor:pointer;

    transition:0.3s;

}

button:hover{
    transform:scale(1.02);
}

</style>

</head>

<body>

<div class="container">

    <div class="logo">
        OTP
    </div>

    <h1>Verify OTP</h1>

    <p>
        Enter the OTP sent to your email
    </p>

    <div class="success">
        OTP Sent Successfully
    </div>

    <form action="/verify-otp" method="POST">

        <input
            type="text"
            name="otp"
            placeholder="Enter OTP"
            required
        >

        <button type="submit">
            Verify OTP
        </button>

    </form>

</div>

</body>

</html>

'''

# Verify OTP Route

@app.route('/verify-otp', methods=['POST'])
def verify_otp():

    user_otp = request.form['otp']

    if user_otp == generated_otp:

        return '''

        <h1 style="
        text-align:center;
        margin-top:100px;
        color:green;
        font-family:Arial;
        ">
        ✅ OTP Matched Successfully
        </h1>

        '''

    else:

        return '''

        <h1 style="
        text-align:center;
        margin-top:100px;
        color:red;
        font-family:Arial;
        ">
        ❌ Invalid OTP
        </h1>

        '''

# Run Server

if __name__ == '__main__':
    app.run(debug=True)