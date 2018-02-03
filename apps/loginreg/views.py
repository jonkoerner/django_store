from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'loginreg/index.html')

def register(request):
    user = User.objects.validateUser(request.POST['name'], request.POST['alias'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['birthday'])
    if user[0] == True:
        request.session['user_id']= user[1].id
        request.session['user_name'] = user[1].name
        return redirect("/shoes")
    for errormessage in user[1]:
        messages.error(request, errormessage)
        print errormessage
    return redirect('/')
def login(request):
    user = User.objects.validateLogin(request.POST['email'], request.POST['password'])
    if user[0]== True:
        request.session['user_id'] = user[1].id
        request.session['user_name'] = user[1].name
        return redirect("/shoes")
    else:
        for errormessage in user[1]:
            messages.error(request, errormessage)
            print errormessage
        return redirect('/')
def current_user(request):
    if 'user_id' in request.session:
        return User.object.get(id=request.session['user_id'])

def logout(request):
    request.session.flush()
    return redirect('/') 

def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    my_productsforsale = user.products.all()
    sale = my_productsforsale.filter(buyer_id=request.session['user_id']).filter(seller_id= request.session['user_id'])
    sold = my_productsforsale.exclude(buyer_id=request.session['user_id']).filter(seller_id=request.session['user_id'])
    purchases = my_productsforsale.filter(buyer_id=request.session['user_id']).exclude(seller_id=request.session['user_id']) 
    context = {
        "myitems": my_productsforsale,
        "forsale": sale,
        "sold"   : sold,
        "purchases" : purchases
    }
    return render(request, 'loginreg/dashboard.html', context)

def quote(request):
    pass

def newproduct(request):
    product = Product.objects.validateProduct(
        request.POST['name'], request.POST['price'], User.objects.get(id=request.session['user_id']),User.objects.get(id=request.session['user_id']))
    return redirect("/shoes")

def buy(request):
    sold = request.POST["product_id"]
    solditem = Product.objects.get(id=sold)
    solditem.buyer_id = request.session['user_id']
    solditem.save()
    print solditem
    return redirect("/dashboard")

def shoes(request):
    all_produces= Product.objects.all()
    forsale= []
    solditems = []
    for item in all_produces:
        if item.seller == item.buyer:
            forsale.append(item)
        else:
            solditems =[]
    context = {
        "products" : all_produces,
        "forsale" : forsale,
        "solditems" : solditems
    }
    return render( request, 'loginreg/home.html', context)

def remove(request):
    query = request.POST["remove"]
    deleteproduct = Product.objects.get(id=query)
    deleteproduct.delete()
    return redirect("/shoes")
