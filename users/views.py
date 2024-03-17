from django.shortcuts import render
from django.contrib import messages
from .models import UserRegisterModel 
from django.core.files.storage import FileSystemStorage

# from .statementcleaning import preprocess_tweet
# from .algorithm import prediction
import random
import csv
from django.conf import settings
# from .algorithm import classifier


# Create your views here.
def userlogin(request):
    return render(request,'users/UserLogin.html',{})

def userregister(request):
    return render(request,'UserRegister.html',{})

def userRegisterAction(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        status = 'waiting'
        try:
            obj = UserRegisterModel.objects.create(email=email,password=password,username=username,mobile=mobile,dob=dob,gender=gender,address=address,status=status)
            print(obj.id)
            if( obj.id > 0):
                messages.success(request, 'You have been successfully registered')
                print('user Register Success')
            else:
                messages.success(request, 'Email Already Registerd')
                print('user Already exist')
        except:
            messages.success(request, 'Email Already Registerd please change new mail')
            pass
    return render(request, 'UserRegister.html', {})

def userlogincheck(request):
    if request.method == "POST":
        usremail = request.POST.get('usremail')
        pswd     = request.POST.get('password')

        try:
            check    = UserRegisterModel.objects.get(email=usremail,password=pswd)
            request.session['id'] = check.id
            #print('User Email ', usremail, ' password is ', pswd)
            request.session['loggeduser'] = check.username
            request.session['email'] = check.email
            status = check.status
            if status == "activated":
                print("User id At", check.id, status)
                return render(request, 'users/userhomepage.html')
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'users/UserLogin.html')
        except:
            pass
        messages.success(request, 'Invalid Email id and password')
        return render(request, 'users/UserLogin.html')


def UserPredictions(request):
    from django.conf import settings
    if request.method=='POST':
        image_file = request.FILES['file']
        # let's check if it is a csv file
        # if not image_file.name.endswith('.png'):
        #     messages.error(request, 'THIS IS NOT A PNG  FILE')
        fs = FileSystemStorage(location="media/")
        filename = fs.save(image_file.name, image_file)
        # detect_filename = fs.save(image_file.name, image_file)
        file = settings.MEDIA_ROOT + '//' + filename
        uploaded_file_url = "/media/" + filename  # fs.url(filename)
        print("Image path ", uploaded_file_url)
        from .Utility.main import result
        result = result(file)
     
        return render(request, "users/UploadForm.html", {'path': uploaded_file_url})
    else:
        return render(request, "users/UploadForm.html",{})
    return HttpResponse('working')


# def video(request):
#     from django.core.files.storage import FileSystemStorage
#     from django.conf import settings
#     if request.method=='POST':
#         image_file = request.FILES['file']
#             # let's check if it is a csv file
#             # if not image_file.name.endswith('.png'):
#             #     messages.error(request, 'THIS IS NOT A PNG  FILE')
#         fs = FileSystemStorage(location="media/iput/")
#         filename = fs.save(image_file.name, image_file)
#             # detect_filename = fs.save(image_file.name, image_file)
#         print('filename:',filename)
#         from .Utility import main  
#         result = main(filename)
#         print("Result=", result)
#     return render(request, "users/upload.html", {})
# # from .models import uploadvideo  
# def upload_video(request):
#     model=uploadvideo()
#     print(model)
#     return render(request,'users/upload.html',{'model':model})
    