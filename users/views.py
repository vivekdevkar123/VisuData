from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Create your views here.


def send_otp(receiver_email, otp):
    myemail = 'contactmoneyniti@gmail.com'
    paswd = 'pjzyeslvgudyuctr'

    message = MIMEMultipart()
    message['From'] = myemail
    message['To'] = receiver_email
    message['Subject'] = 'OTP DO NOT SHARE'

    # Create the HTML body
    html = f"""
<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
  <div style="margin:50px auto;width:70%;padding:20px 0">
    <div style="border-bottom:1px solid #eee">
      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
    </div>
    <p style="font-size:1.1em">Hi,</p>
    <p>Thank you for choosing Your Brand. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
    <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
    <hr style="border:none;border-top:1px solid #eee" />
    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
      <p>Your Brand Inc</p>
      <p>1600 Amphitheatre Parkway</p>
      <p>California</p>
    </div>
  </div>
</div>
    """

    # Attach the HTML body to the message
    message.attach(MIMEText(html, 'html'))

    # body = f"Your OTP is {otp}. PLEASE DO NOT SHARE IT"
    # message.attach(MIMEText(body, 'plain'))

    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(myemail, paswd)
    text = message.as_string()
    connection.sendmail(myemail, receiver_email, text)
    connection.quit()


def account_created(receiver_email, username):
    myemail = 'contactmoneyniti@gmail.com'
    paswd = 'pjzyeslvgudyuctr'

    message = MIMEMultipart()
    message['From'] = myemail
    message['To'] = receiver_email
    message['Subject'] = 'ACCOUNT IS CREATED SUCCESFULLY'
    # Create the HTML body
    html = f"""
        <h1> Your account is created for {username} successfully </h1>
    """

    # Attach the HTML body to the message
    message.attach(MIMEText(html, 'html'))

    # body = f"Your OTP is {otp}. PLEASE DO NOT SHARE IT"
    # message.attach(MIMEText(body, 'plain'))

    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(myemail, paswd)
    text = message.as_string()
    connection.sendmail(myemail, receiver_email, text)
    connection.quit()


def OtpVerification(request):
    if request.method == 'POST':

        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('signup_data').get('otp')

        if str(user_otp) == str(stored_otp):

            # Create the user account if the OTP is verified
            username = request.session.get('signup_data').get('username')
            email = request.session.get('signup_data').get('email')
            password = request.session.get('signup_data').get('password')
            fname = request.session.get('signup_data').get('fname')
            lname = request.session.get('signup_data').get('lname')

            myuser = CustomUser.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            account_created(email, username)
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('OtpVerification')

    return render(request, 'accounts/otp_verification.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")
            return redirect('signup')

        # Generate and send OTP
        otp = random.randint(100000, 999999)
        send_otp(email, otp)

        # Create a session variable to store the OTP and other user info
        request.session['signup_data'] = {
            'username': username,
            'email': email,
            'password': password,
            'fname': fname,
            'lname': lname,
            'otp': otp,
        }

        # Redirect the user to the OTP verification page
        return redirect('OtpVerification')

    return render(request, 'accounts/signup.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try authenticating using both email and username
        user = CustomUser.objects.filter(email=username).first() or CustomUser.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect...')

    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')
