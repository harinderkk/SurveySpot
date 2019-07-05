from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.hashers import make_password,check_password
from miscellaneous.generic_functions import generate_string, link_send
from frontpanel.models import RoleDetails, UserRole
from frontpanel.forms import RoleDetailsForm

# Create your views here.
def admin_index(request):
    return render(request, 'admin_index.html')


def login(request):
    if request.method == 'POST':
        get_email = request.POST['email']
        get_password = request.POST['password']
        try:
            data = RoleDetails.objects.get(email= get_email)
            db_password= data.password
            db_active = data.active
            db_verify_link = data.verify_link
            role = data.role_id
            if check_password(get_password, db_password):

                if db_active == '0' and db_verify_link =='':
                    return HttpResponse('Please verify your email')
                elif db_active== '1':
                    request.session['email'] =get_email
                    request.session['name'] = data.name
                    request.session['image'] = data.image
                    request.session['role'] = role
                    if role == 1:
                        return render(request, 'admin_index.html')
                    elif role == 2:
                        pass
                return HttpResponse('y')

            else:
                return HttpResponse('Password not valid')
        except:
            return HttpResponse('<h1> Email not found</h1>')

    return render(request,'login.html')


def verify_link(request):
    get_link = request.GET['link']   #variable after ? in url
    session_mail = request.session['email']
    data = RoleDetails.objects.get(email=session_mail)
    db_verify = data.verify_link
    if get_link == db_verify:

        update = RoleDetails(email=session_mail,active=1, verify_link='')
        update.save(update_fields= ['active', 'verify_link'])
        return redirect('/update_password/')


def register(request):
    data = UserRole.objects.all()
    if request.method == "POST":
        form = RoleDetailsForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.role_id = request.POST['role']
            f.name = request.POST['name']
            f.email = request.POST['email']
            f.gender = request.POST['gender']
            string = generate_string()
            link = make_password(string)
            link = link.replace("+", "")
            f.password = make_password(string)
            f.active = str(0)
            f.verify_link = link
            f.save()
            f_link = "127.0.0.1:8000/verify_link/?link=" + str(link)
            request.session['email'] = f.email
            link_send(f.email, f_link, string)
        return render(request, "register.html", {'confirm': True})
    return render(request, 'register.html', {'data':data})


def update_password(request):
    if request.method == 'POST':
        get_password = request.POST['password']
        get_confirm_password = request.POST['confirm_password']
        session_mail = request.session['email']
        if get_password == get_confirm_password:
            update = RoleDetails(email=session_mail, password=make_password(get_confirm_password))
            update.save(update_fields=['password'])
            return redirect("/login/")
    return render(request, 'update_password.html')