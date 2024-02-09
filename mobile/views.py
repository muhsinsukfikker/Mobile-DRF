from django.shortcuts import render,redirect
from django.views.generic import View
from mobile.models import Mobiles
from mobile.forms import MobileForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators  import method_decorator

# Create your views here.

# class MobileCreateView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request,'mobile_add.html')
    
#     def post(self, request, *args, **kwargs):
#         Mobiles.objects.create(
#             name=request.POST.get('name'),
#             price=request.POST.get('price'),
#             brand=request.POST.get('brand'),
#             specs=request.POST.get('specs'),
#             display=request.POST.get('display'),
#         )
#         return render(request,'mobile_add.html')

def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'invalid session')
            return redirect('signin')
           
        else:
            return fn(request, *args, **kwargs)
    return wrapper


@method_decorator(signin_required,name='dispatch')
class MobileCreateView(View):
    def get(self, request, *args, **kwargs):
        form = MobileForm()

        return render(request,'mobile_add.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = MobileForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mobile  was successfully created')
            return redirect('mobile-all')
    
        else:
            messages.error(request,'mobile creation failed')
            return render(request,'mobile_add.html',{'form':form})

@method_decorator(signin_required,name='dispatch')
class MobileListView(View):
    def get(self, request, *args, **kwargs):
        qs=Mobiles.objects.all()
        if "brand"in request.GET:
            val=request.GET.get("brand")
            qs=qs.filter(brand__iexact=val)
        if "display"in request.GET:
            val=request.GET.get("display")
            qs=qs.filter(display__iexact=val)

        if "price_gt"in request.GET:
            val=request.GET.get("price_gt")
            qs=qs.filter(price__lte=val)

        return render(request,'mobile_list.html',{'data':qs})


@method_decorator(signin_required,name='dispatch')
class MobileDetailView(View):
    def get(self, request, *args, **kwargs):
        # id=2
        if not request.user.is_authenticated:
                return redirect('signin') 
        id=kwargs.get('pk')
        qs=Mobiles.objects.get(id=id)
        return render(request,'mobile_detail.html',{'data':qs})
        


@method_decorator(signin_required,name='dispatch')
class MobileDeleteView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')       
        id=kwargs.get('pk')
        Mobiles.objects.get(id=id).delete()
        messages.success(request,"Mobile deleted")
        return redirect('mobile-all')

@method_decorator(signin_required,name='dispatch')
class MobileUpdateView(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(instance=obj)
        return render(request,'mobile_edit.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        obj=Mobiles.objects.get(id=id)

        form=MobileForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            messages.success(request,"Mobile updated")
            form.save()
            return redirect('mobile-all')
        else:
            messages.error(request,'mobile update failed')
            return render(request,'mobile_edit.html',{'form':form})
        

class SingUpView(View):
    def get(self, request, *args, **kwargs):
        form=RegistrationForm()
        return render(request,'register.html',{'form':form})


    def post(self, request, *args, **kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request, 'Registerd succcessfully')
            
            return redirect('signin')
        else:
            messages.error(request, 'failed to register')
            return render(request, 'register.html',{'form':form})

 
class SingInView(View):
    def get(self, request, *args, **kwargs):
        form=LoginForm()
        return render(request, 'login.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            passwd=form.cleaned_data.get('password')
            user_obj=authenticate(request,username=uname,password=passwd)
            if user_obj :
                print('valid credentials')
                login(request,user_obj)
                print(request.user)
                return redirect('mobile-all')
                
            else:
                print('Invalid credentials')
            print(uname,passwd)
            return render(request, 'login.html',{'form':form})
        else:
            return render(request, 'login.html',{'form':form})   


@method_decorator(signin_required,name='dispatch')
class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('signin')
                                         