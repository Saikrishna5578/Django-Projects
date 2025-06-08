from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import account
import secrets
from decimal import Decimal
from .forms import Register
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
def index(request):
    return render(request, 'index1.html')

def delete_all_records(request):
    account.objects.all().delete()
    return HttpResponse("All records deleted successfully!")

def register(request):
    form = Register()
    msg = {}
    show_modal = False  # Flag to trigger OTP modal
    # Handle OTP verification first (when OTP form is submitted)
    if request.method == 'POST' and 'otp' in request.POST:
        entered_otp = request.POST.get('otp')
        print(entered_otp)
        actual_otp = str(request.session.get('otp'))
        print(actual_otp)
        username = request.session.get('pending_user')
        if entered_otp == actual_otp:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()

            # Cleanup session
            del request.session['otp']
            del request.session['pending_user']

            messages.success(request, "User verified and account activated. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            show_modal = True  # Show OTP modal again

    # Handle initial registration form submission
    elif request.method == 'POST':
        form = Register()
        form = Register(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Temporarily deactivate account
            user.save()
            print("User created")
            # Generate and store OTP
            otp = generate_otp()
            print(otp)
            request.session['otp'] = otp
            print(request.session['otp'])
            request.session['pending_user'] = user.username

            # Send OTP email
            send_otp_email(user.email)

            messages.error(request, "OTP sent to your email. Please enter it below.")
            show_modal = True  # Trigger modal to enter OTP
        else:
            msg['user'] = "Please check the username and password"
    else:
        form = Register()
    return render(request, "user/register.html", {'form': form, 'msg': msg, 'show_modal': show_modal})

def generate_otp(length=6):
    return ''.join(str(secrets.randbelow(10)) for _ in range(length))

def send_otp_email(mail_usr):
    otp_code = generate_otp()
    
    subject = "Your OTP for Account Verification – Black Money Bank"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; color: #333;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #004085;">Black Money Bank</h2>
                <p>Dear Customer,</p>

                <p>To complete your account verification, please use the following One-Time Password (OTP):</p>

                <p style="font-size: 24px; font-weight: bold; color: #d63384; text-align: center;">{otp_code}</p>

                <p>This OTP is valid for the next 10 minutes. Please do not share it with anyone.</p>

                <p>If you did not request this OTP, please contact our support team immediately.</p>

                <p>Thank you for banking with us.</p>

                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>Black Money Bank</strong><br>
                    Customer Service Team
                </p>
            </div>
        </body>
    </html>
    """
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[mail_usr],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
    return otp_code 

def log_in(request):
    msg = {}
    if request.method == "POST":
        un = request.POST.get('un')
        pswd = request.POST.get('password')
        user = authenticate(request,username = un,password = pswd)
        # print(user)
        if user is not None:
            login(request,user)
            if request.user.is_authenticated and not account.objects.filter(user=request.user).exists():
                return redirect("create")
            else:
                return redirect('home')
                
        else:
            msg['user'] = "Pleace check your username or password OR"
    return render(request, 'user/login.html', {"msg": msg})


@login_required(login_url='login')
def create(request):
    form = Register()
    reg = False
    msg = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        aadhar = request.POST.get('aadhar')
        address = request.POST.get('address')
        mail = request.POST.get('email')
        print(name,gender,mobile,aadhar,address,mail)
        if len(str(aadhar)) != 12:
            msg['aadhar'] = "Aadhar number must be 12 digits."
        elif len(str(mobile)) != 10:
            msg['mobile'] = "Mobile number must be 10 digits."
        else:
            try:
                if account.objects.filter(aadhar = aadhar).exists():
                    msg['exists']  = "Account already exists with the aadhar number please"

                elif account.objects.filter(phone = mobile).exists():
                    msg['exists_ph']  = "A account with the phone number is already exists "
     
                elif account.objects.filter(email = mail).exists():
                    msg['exists_em']  = "An account with email id already exists"
       
                else:
                    user = request.user
                    if not user:
                        msg['nouser'] = "User not found. Please create user first."
                    else:
                        print(request.user)
                        account.objects.create(
                            user = user,
                            name = name, 
                            gender = gender, 
                            phone = mobile, 
                            email = mail,
                            aadhar = aadhar, 
                            address = address
                        )
                        del request.session['new_user_email']
                        data = account.objects.get(user=request.user)
                        mail_usr = data.email
                        print(mail_usr)
                        print("sending email")
                        sub = "Thank You for Choosing Black Money Bank – Your Account Has Been Successfully Created"
                        body = (
                            "Dear Valued Customer,\n\n"
                            "We are pleased to inform you that your account with Black Money Bank has been successfully created.\n\n"
                            "Thank you for choosing us as your trusted banking partner. We are committed to providing you with secure,\n"
                            "innovative, and customer-centric financial services. Should you have any questions or need assistance,\n"
                            "please do not hesitate to contact our support team.\n\n"
                            "Welcome aboard, and we look forward to serving you.\n\n"
                            f"Your Bank Accout number is : <b>{data.acc_num}</b>"
                            "Warm regards,\n"
                            "Black Money Bank\n"
                        )
                        send_mail(sub,
                                body,
                                settings.EMAIL_HOST_USER,
                                [mail_usr],fail_silently=False)
                        print("email sent")
                        return redirect('login')
            except BaseException as e:
                print(e)
    else:
        form = Register()
    return render(request, 'create.html', {'form':form, 'reg':reg, 'msg': msg})

@login_required(login_url='login')
def log_out(request):
    print("Logging out")
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def home(request):
    try:
        user_account = account.objects.get(user=request.user)
        print(user_account.acc_num)
        if user_account.pin == "000000":
            messages.error(request, f"Please SET YOUR PIN first Your account number: {user_account.acc_num} <br> Use it to set your pin  ")
    except account.DoesNotExist:
        user_account = None  # or redirect to account creation

    return render(request, 'home.html')

@login_required(login_url='login')
def accdetails(request): 
    data = account.objects.get(user=request.user)
    print(data.pin)
    if data:
        details ={
            'acc': data
        }
    return render(request,'accdetails.html',details)

@login_required(login_url='login')
def pin_generation(request):
    msg = {}
    if request.method == 'POST':
        pin = request.POST.get('pin')
        cnfpin = request.POST.get('cnfpin')
        try:
            data = account.objects.get(user=request.user)
            # print(data.acc_num, "yes")
        except BaseException as e:
            if e:
                msg['account'] = "Account Doesn't exist"
                # return render(request, 'pin.html', {'msg': msg})
        if len(str(pin)) != 6 and len(str(cnfpin)) != 6:
            msg['pin'] = "Your PIN must be 6 digits."
        else:
            if pin != cnfpin:
                msg['cnfpin'] = "Please check the PIN and confirm PIN."
            else:
                data.pin = pin
                data.save()
                messages.error(request, "Congratulations! Your PIN has set Successfully" )
    return render(request, 'pin.html', {'msg': msg})


@login_required(login_url='login')
def balance(request):
    context = {}
    if request.method == 'POST':
        pin = request.POST.get('pin')
        try:
            data = account.objects.get(user=request.user)
            if len(str(pin)) != 6:
                context['pin'] = "Your PIN must be 6 digits."
            elif pin != data.pin:
                context['pin'] = "Incorrect PIN."
            else:
                context['success'] = f"Available Balance is:{data.balance}"
        except account.DoesNotExist:
            context['account'] = "Account doesn't exist."
    return render(request, 'balance.html', {'context':context})

@login_required(login_url='login')
def deposite(request):
    msg = {}
    data = account.objects.get(user=request.user)
    if request.method == 'POST':
        pin = request.POST.get('pin')
        amnt = int(request.POST.get('amnt'))
        if len(str(pin)) != 6:
            msg['pin'] = "Your PIN must be 6 digits."
        else:
            if pin != data.pin:
                msg['pin'] = "Incorrect PIN."
            else:
                if amnt >0 and amnt <=10000:
                    data.balance += Decimal(amnt)
                    data.save()
                    messages.error(request, "Amount Deposited successfully" )
                    send_mail(
                        'Deposit Confirmation',
                        f'Hi {request.user.username}, ₹{amnt} has been successfully deposited to your account.',
                        'bmbbank@gmail.com',
                        [request.user.email],
                        fail_silently=False,
                    )
                else:
                    msg['amount'] = "Please enter a valid amount"
    return render(request, 'deposite.html', {'msg': msg})


@login_required(login_url='login')
def withdraw(request):
    msg = {}
    data = account.objects.get(user=request.user)
    if request.method == 'POST':
        pin = request.POST.get('pin')
        amnt = int(request.POST.get('amnt'))
        if len(str(pin)) != 6:
            msg['pin'] = "Your PIN must be 6 digits."
        else:
            if pin != data.pin:
                msg['pin'] = "Incorrect PIN."
            else:
                # print("Updating balance")
                if amnt > 0 and amnt <= 10000:
                    if data.balance >= Decimal(amnt):
                        data.balance -= Decimal(amnt)
                        data.save()
                        # print(data.balance)
                        messages.error(request, "Amount Withdrawn successfully")
                        send_mail(
                            'Withdrawal Confirmation',
                            f'Hi {request.user.username}, ₹{amnt} has been withdrawn from your account.',
                            'bmbbank@gmail.com',
                            [request.user.email],
                            fail_silently=False,
                        )
                    else:
                        msg['funds'] = "Insufficient Funds"
                    
                else:
                    msg['amount'] = "Please enter a valid amount"       
    return render(request, 'withdraw.html', {'msg':msg})

@login_required(login_url='login')
def acc_transfer(request):
    msg = {}
    data = account.objects.get(user=request.user)
    if request.method == 'POST':
        to_acc_num = request.POST.get('to_acc_num')
        pin = request.POST.get('pin')
        amnt = int(request.POST.get('amnt'))
        if account.objects.filter(acc_num = to_acc_num).exists():
            data1 = account.objects.get(acc_num = to_acc_num)
            if len(str(pin)) != 6:
                msg['pin'] = "Your PIN must be 6 digits."
            else:
                if pin != data.pin:
                    msg['pin'] = "Incorrect PIN."
                else:
                    if amnt >0 and amnt <=10000:
                        print(data1.balance)
                        print("Updating balance")
                        if data.balance >= Decimal(amnt):
                            data1.balance += Decimal(amnt)
                            data.balance -= Decimal(amnt)
                            data.save()
                            data1.save()
                            messages.error(request, "Amount Transfered successfully")
                            send_mail(
                                'Transfer Confirmation',
                                f'Hi {request.user.username}, ₹{amnt} has been transferred to {data1.name}.',
                                'bmbbank@gmail.com',
                                [request.user.email],
                                fail_silently=False,
                            )

                            # Notify recipient
                            send_mail(
                                'Received Funds',
                                f'Hi {data1.name}, ₹{amnt} has been received from {request.user.username}.',
                                'bmbbank@gmail.com',
                                [data1.email],
                                fail_silently=False,
                            )
                        # print(data.balance, data1.balance)
                        else:
                            msg['funds'] = "Insufficient Funds"
                    else:
                        msg['amount'] = "Please enter a valid amount" 
        else:
            msg['account'] = "Account Doesn't exist"   
    return render(request, 'accTransfer.html', {'msg':msg})