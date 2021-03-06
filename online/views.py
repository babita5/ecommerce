from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.views.generic.base import View
from online.models import Category, Slider, Ad,Item, Brand, Cart, Contact
from django.contrib.auth.models import User
from django.contrib import messages, auth
# Create your views here.
class BaseView(View):
    views={}

class HomeView(BaseView):
    def get(self, request):
        self.views['categories']=Category.objects.all()
        self.views['sliders']=Slider.objects.all()
        self.views['brands']=Brand.objects.all()
        self.views['ads1']=Ad.objects.filter(rank= 1)
        self.views['ads2'] = Ad.objects.filter(rank=2)
        self.views['ads3'] = Ad.objects.filter(rank=3)
        self.views['ads4'] = Ad.objects.filter(rank=4)
        self.views['ads5'] = Ad.objects.filter(rank=5)
        self.views['ads6'] = Ad.objects.filter(rank=6)
        self.views['ads7'] = Ad.objects.filter(rank=7)
        self.views['ads8'] = Ad.objects.filter(rank=8)
        self.views['items']=Item.objects.all()
        self.views['new_items']=Item.objects.filter(label= 'new')
        self.views['hot_items']=Item.objects.filter(label='hot')
        self.views['sale_items']=Item.objects.filter(label='sale')

        return render(request, 'index.html',self.views)

class SearchView(BaseView):
    def get(self,request):
        query=request.GET.get('query',None)
        if not query:
            return redirect("/")
        self.views['search_query']= Item.objects.filter(
           description__icontains=query
        )
        self.views['searched_for']=query
        return render(request, 'search.html',self.views)

class ProductDetailView(BaseView):
    def get(self,request,slug):
        category=Item.objects.get(slug=slug).category
        self.views['detail_item']= Item.objects.filter(slug=slug)
        self.views['related_item']=Item.objects.filter(category=category)
        self.views['categories']=Category.objects.all()
        self.views['brands']=Brand.objects.all()
        return render(request,'product-detail.html',self.views)

class CategoryView(BaseView):
    def get(self,request,slug):
        cat=Category.objects.get(slug=slug).id
        self.views['category_items']=Item.objects.filter(category=cat)

        return render(request,'category.html',self.views)

class BrandView(BaseView):
    def get(self,request,name):
        brand=Brand.objects.get(name=name).id
        self.views['brand_items']=Item.objects.filter(brand=brand)

        return render(request,'brand.html',self.views)

def Register(request):
    if request.method=='POST':
        first_name= request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        c_password=request.POST['c_password']

        if password==c_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'The username is already used.')
                return redirect('online:signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'The email is already used.')
                return redirect('online:signup')
            else:
                data=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                data.save()
                messages.error(request, 'Signed up Successfully')
                return redirect('online:signup')
        else:
            messages.error(request, 'Password Not Matched')
            return redirect('online:signup')

    return render(request,'signup.html')


class CartView(BaseView):
    def get(self,request):
        self.views['carts']=Cart.objects.filter(user=request.user.username)
        return render(request,'cart.html',self.views)


def cart(request,slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exists():
        quantity=Cart.objects.get(slug=slug, user=request.user.username).quantity
        quantity=quantity+1
        price = Item.objects.get(slug=slug).price
        discounted_price = Item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total=discounted_price*quantity
        else:
            total=price*quantity

        Cart.objects.filter(slug=slug,user=request.user.username).update(quantity=quantity, total=total)

    else:
        price = Item.objects.get(slug=slug).price
        discounted_price = Item.objects.get(slug=slug).discounted_price
        if discounted_price>0:
            total=discounted_price
        else:
            total=price
        data=Cart.objects.create(
            user=request.user.username,
            slug=slug,
            item=Item.objects.filter(slug=slug)[0],
            total=total
        )
        data.save()
    return redirect('online:mycart')

def deletecart(request,slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exits():
        Cart.objects.filter(slug=slug, user=request.user.username).delete()
        messages.success(request, 'The item is deleted.')
    return redirect('online:mycart')

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request, "Username and password do not match.")
            return redirect('online:signin')
    return render(request,'signin.html')

def delete_single_cart(request,slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exists():
        quantity=Cart.objects.get(slug=slug, user=request.user.username).quantity
        quantity=quantity-1
        price = Item.objects.get(slug=slug).price
        discounted_price = Item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total=discounted_price*quantity
        else:
            total=price*quantity

        Cart.objects.filter(slug=slug,user=request.user.username).update(quantity=quantity, total=total)
    return redirect('online:mycart')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']

        data=Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        data.save()
        messages.success(request,'Message is submitted.')

        html_content=f'<p> The customer having name {name}, mail address {email} and subject {subject} has some message and the message is {message}'
        msg = EmailMultiAlternatives(subject, message, 'babitas550@gmail.com', ['babitas550@gmail.com'])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return render(request, 'contact.html')