from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from .models import Category,User,Author, Contact,Post,Comment
from django.contrib import messages
from django.contrib.auth.hashers import  check_password, make_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import send_mail,send_mass_mail
from random import randint 
from .forms import PostForm

# Create your views here.

def HomeView(request):
    category = Category.objects.all()
    categoryName = request.GET.get('Category')
    print(categoryName)
    if categoryName:
        post = Post.objects.filter(category__cname=categoryName)
    else:
        post = Post.objects.all()
    return render(request, 'techapp/home.html',{'Category':category,'Post':post})

def SignupView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        profile = request.FILES.get('profile')
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'This Email is Already Registerd')
        else:
            u = User()
            u.email = email
            u.password = password
            print(u.password)
            u.password = make_password(u.password)
            print(u.password)
            u.save()
            author = Author.objects.create(first_name=first_name,last_name=last_name,phone=phone,
                                           profile=profile, user=u)
            author.save()
            messages.success(request, 'You Registerd successfully!!!')

    return render(request, 'techapp/signup.html')

def LoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user =  User.objects.get(email=email)
            except User.DoesNotExist:
                raise Http404("This Email is not registerd!!!")
            #print(password, user.password)
            checkPass = check_password(password, user.password)
            #print(checkPass)
            if checkPass:
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request,user)
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.email
                    #messages.success(request, 'You Logged In Successfully')
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.warning(request, 'Sorry, Please Check Your Email Or Password!!!')
            else:
                messages.warning(request, 'Password does not match!!!')
        return render(request, 'techapp/login.html')
    else:
        return HttpResponseRedirect('/dashboard/')
    

def SinglePostView(request, slug):
    category = Category.objects.all()
    singlePost = Post.objects.get(slug=slug)
    comment = Comment.objects.filter(post=singlePost)
    return render(request, 'techapp/singlepost.html',{'post':singlePost,'Category':category,'comments':comment})

def postCommentView(request, slug):
    if request.method == "POST":
        comment_data = request.POST.get("comment")
        user= request.user
        postid = request.POST.get("postId")
        post = Post.objects.get(id=id)
        cmt = Comment(comment_data=comment_data, user=user, post=post)
    return redirect(f"/single-post/{post.slug}/")

@login_required(login_url='login')
def DashboardView(request):
    user = request.user
    print(user)
    post = Post.objects.filter(author__user=user)
    return render(request, 'techapp/dashboard.html',{'post':post})

@login_required(login_url='login')
def LogoutView(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect('/')

def ContactView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        c = Contact(name=name,email=email,message=message)
        subject = "For Contact"
        body =  """
                    Team:  Tech-Blog

                    Hello!!!! Thank You 
                    Thanks For Beleving us .
                    My Team   will Contact You
                    very Soon {}

                   
                """.format(name)
        send_mail(subject, body,"armannmalik9880@gmail.com",[c.email,], fail_silently=False)
        c.save()
        messages.success(request, 'Thank You | Our Team Contact You Very soon')
    return render(request, 'techapp/contact.html')

@login_required(login_url='login')
def AddPostView(request):
    if request.method == 'POST':
        fm = PostForm(request.POST, request.FILES)
        if fm.is_valid():
            title = fm.cleaned_data['title']
            content = fm.cleaned_data['content']
            slug = fm.cleaned_data['slug']
            category = fm.cleaned_data['category']
            author = fm.cleaned_data['author']
            image = fm.cleaned_data['image']
            pst = Post(title=title,content=content,slug=slug,category=category,author=author,image=image)
            pst.save()
            messages.success(request, 'your blog posted Successfully!!')
        else:
            messages.warning(request, "Not Posted blog Please try once again!!!")
    else:
        fm = PostForm()       
    return render(request, 'techapp/addpost.html',{'form':fm})

@login_required(login_url='login')
def UpdatePostView(request,slug):
    if request.method == 'POST':
        post = Post.objects.get(slug=slug)
        fm = PostForm(request.POST, request.FILES, instance=post)
        if fm.is_valid():
            messages.success(request, 'Your Post Updated Successfully!!!')
            fm.save()
    else:
        post = Post.objects.get(slug=slug)
        fm = PostForm(instance=post)
    return render(request, 'techapp/updatepost.html',{'form':fm})


@login_required(login_url='login')
def DeletePostView(request, slug):
    return HttpResponse("<h1>Delete Post</h1>")

@login_required(login_url='login')
def CategoryView(request):
    category = Category.objects.all()
    return render(request, 'techapp/category.html',{"category":category})

@login_required(login_url='login')
def AddCategoryView(request):
    if request.method == 'POST':
        cname = request.POST.get('category')
        category = Category(cname=cname)
        category.save()
        messages.success(request, 'New Category Added')
    return render(request, 'techapp/addcategory.html')

@login_required(login_url='login')
def EditCategoryView(request,id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.cname = request.POST.get('category')
        category.save()
        messages.success(request, 'Your Category Updated Successfully')
    return render(request, 'techapp/editcategory.html',{'category':category,'id':id})

@login_required(login_url='login')
def DeleteCategoryView(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return HttpResponseRedirect('/category/')


def ForgetPasswordView(request):
    if request.method == 'POST':
        flag = False
        email = request.POST.get('email')
        print(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Http404("This email is not registerd Please Enter valid Email Address| Thank You")
        flag = True
        if (flag==True):
            user.otp = randint(100000,999999)
            user.save()
            subject = "Hey Your One Time Password(OTP)"
            body =  """
                    Hey User 

                    Your One Time Password is {}
                    The password will expire in 10 minute
                    if not used.

                    If you have not made this request,
                    please report Us

                    """.format(user.otp)
            send_mail(subject, body,"armannmalik9880@gmail.com",[user.email,], fail_silently=False)
            return HttpResponseRedirect('/enter-otp/'+email+"/")
        else:
            messages.warning(request,"Email Not Found")
    return render(request, 'techapp/forgetpassword.html')

def EnterOtpView(request,email):
    if request.method == 'POST':
        flag = False
        otp = int(request.POST.get('otp'))
        user = User.objects.get(email=email)
        flag = True
        if(flag == True):
            if (user.otp == otp):
                return HttpResponseRedirect('/reset-password/'+email+"/") 
            else:
                messages.warning(request,"OTP Does't Match")   
               
        else:
            messages.warning(request,"Email Not Found not fund")
    return render(request, 'techapp/enterotp.html')

def ResetPasswordView(request, email):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Http404("This email is not registerd Please Enter valid Email Address| Thank You")
        if (password1 == password2):
            user.set_password(password1)
            user.save()
            subject = "Password Reset Successfully"
            body =  """
                       Your Password Reset
                       successfully.
                       New password genereted
                        
                       
                    """
            send_mail(subject, body,"armannmalik9880@gmail.com",[user.email,], fail_silently=False)
            return HttpResponseRedirect('/')
        else:
            messages.error("Password and Confirm Password not Match")
    return render(request, 'techapp/resetpassword.html')

@login_required(login_url='login')
def ChangePasswordView(request):
    user = request.user
    if request.method == 'POST':
        usr = User.objects.get(email=user)
        password1 = request.POST.get('password1')
        password2   = request.POST.get('password2')
        print(user)
        if (password1 == password2):
            user.set_password(password1)
            user.save()
            messages.success(request, 'Your Password change Successfully!')
        else:
            messages.warning(request, 'Password & Confirm Password does not match')
    return render(request, 'techapp/changepassword.html')

@login_required(login_url='login')
def UserProfileView(request):
    user = request.user
    user_data = Author.objects.get(user=user)
    return render(request, 'techapp/userprofile.html',{'Author':user_data})


@login_required(login_url='login')
def UserEditProfileView(request,id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        author.first_name = request.POST.get('first_name')
        print(author.first_name)
        author.last_name = request.POST.get('last_name')
        print(author.last_name)
        author.phone = request.POST.get('phone')
        author.profile = request.FILES.get('profile')
        author.save()
        return HttpResponseRedirect('/user-profile/')
    return render(request, 'techapp/editprofile.html',{'author':author})


@login_required(login_url='login')
def UserDeleteProfileView(request):
    user= request.user
    user_data = User.objects.get(email=user)
    user_data.delete()
    return HttpResponseRedirect('/login/')

