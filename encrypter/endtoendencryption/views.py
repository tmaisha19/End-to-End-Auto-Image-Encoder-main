from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.core.mail import send_mail  
from random import randint, randrange
from django.contrib.auth import logout
# Create your views here.
def home(request):
    print(request.user)
    return render(request,'index.html')
def decodefunc(request):
    return render(request,'decode.html')
def register(request):
    if(request.method == 'POST'):
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        email_q = User.objects.all().filter(email = email)
        username_q = User.objects.all().filter(username = username)
        try:
            checked = request.POST['checked']
        except:
            messages.warning(request,'Sorry You Need To Accept The Agreement')
            return render(request,'register.html')
        if(len(firstname) <= 0):
            messages.warning(request,"Sorry First Name Can't be blank")
            return render(request,'register.html')
        else:
            if(len(lastname) <= 0):
                messages.warning(request,"Sorry Last Name Can't be blank")
                return render(request,'register.html')
            else:
                if(len(email_q) == 0):
                    if(len(username_q) == 0):
                        if(len(password) >= 8):
                            user = User.objects.create_user(first_name = firstname,last_name = lastname, username = username,email = email,password = password)
                            user.save()
                            messages.success(request,'We Mailed You With Confirm Code!')
                            code = randint(100000, 999999)
                            request.session['code'] = code
                            request.session['verify'] = email
                            send_mail(
                            'Confirmation Mail',
                            'Here is Your Verification Code {}'.format(code),
                            'itstechnerd@gmail.com',
                            [str(email)],
                            fail_silently=False,
        )
                            return render(request,'verifyprofile.html')
                        #TODO: OTP Auth Need To DO
                        else:
                            messages.warning(request,"Sorry Password Must be 8 Char Long And Must Contain Upper Case Lower Case And Symbol")
                            return render(request,'register.html')
                    else:
                        messages.warning(request,"Sorry Username Already Used")
                        return render(request,'register.html')

                else:
                    messages.warning(request,"Sorry Email Already Used")
                    return render(request,'register.html')

                        
    else:
        return render(request,'register.html')
def loginfunc(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        username = User.objects.all().filter(email = email)
        if(len(username) > 0):
            user = authenticate(username = username[0].username,password = password)
            print(user)
        else:
            messages.warning(request,"Sorry Email Or Password Is Wrong!")
            return render(request,'login.html')
        if(user is not None and username[0].is_superuser == False):
            request.session['email'] = email
            login(request,user)
            # return render(request,'login.html')
            return redirect("/")

        else:
            messages.warning(request,"Sorry Email Or Password Is Wrong! hit here")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def recoverfunc(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        user = User.objects.all().filter(email = email)
        if(len(user) == 1):
            code = randint(100000, 999999)
            request.session['code'] = code
            request.session['verify'] = email
            send_mail(
            'Confirmation Mail',
            'Here is Your Verification Code {}'.format(code),
            'itstechnerd@gmail.com',
            [str(email)],
            fail_silently=False,
        )
            return render(request,'verify.html')
        else:
            messages.warning(request,"Sorry Email Not In Database!")
            return render(request,'Recover.html')            
    else:
        return render(request,'Recover.html')

def verifyfunc(request):
    if(request.method == 'POST'):
        verify = request.POST['verify']
        if(int(verify) == request.session['code']):
            return render(request,'changepass.html')
        else:
            messages.warning(request,"Sorry Verification Code is wrong!")
            return render(request,'verify.html')           
    else:
        return redirect("/account/login")
    
def verifyprofilefunc(request):
    if(request.method == 'POST'):
        verify = request.POST['verify']
        if(int(verify) == request.session['code']):
            user = User.objects.all().filter(email = request.session['verify'])
            messages.success(request,'Registration Success. You Can Login Now!')
            return redirect("/account/login")
        else:
            messages.warning(request,"Sorry Verification Code is wrong!")
            return render(request,'verifyprofile.html')           
    else:
        return redirect("/account/login")
    
def logout_view(request):
    logout(request)
    return redirect("/")