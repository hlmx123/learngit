import random
from io import BytesIO

from PIL import ImageFont, Image
from PIL.ImageDraw import ImageDraw
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from user.models import User
from user.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            # 设置用户登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname

            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')

def get_color():
    r=random.randrange(256)
    g=random.randrange(256)
    b=random.randrange(256)
    return (r,g,b)


def get_verify_code(request):
    imagesize=(200,100)
    imagecolor=get_color()
    imagefont=ImageFont.truetype('statics/fonts/ADOBEARABIC-BOLD.OTF',size=60)
    image = Image.new('RGB', imagesize, imagecolor)
    imagedraw = ImageDraw(image, 'RGB')

    source_str='123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    des_str=""
    for i in range(4):
        r=random.randrange(len(source_str))
        des_str+=source_str[r]
    print(des_str)
    request.session['varifycode']=des_str
    for i in range(4):
        imagedraw.text((20+40*i,20),des_str[i],fill=get_color(),font=imagefont)
    for i in range(2700):
        imagedraw.point((random.randrange(200),random.randrange(100)),fill=get_color())
    # imagedraw.text((20,20),'ROCK',font=imagefont)
    buffer=BytesIO()
    image.save(buffer,'png')
    return HttpResponse(buffer.getvalue(),content_type='image/png')


def login(request):
    if request.method=='POST':
        nickname=request.POST.get('nickname')
        password=request.POST.get('password')
        verify_code = str(request.POST.get('varifycode'))
        desk_code = str(request.session.get('varifycode'))
        user = User.objects.filter(nickname=nickname).first()
        if user:
            if nickname==user.nickname and check_password(password,user.password):
                if verify_code.lower() == desk_code.lower():
                    request.session['uid'] = user.id
                    request.session['nickname'] = user.nickname

                    return redirect('/user/info/')
                else:
                       error = '验证码错误'
                       return render(request, 'login.html', {'error': error})
            else:
                error='用户名或密码错误'
                return render(request, 'login.html', {'error': error})

        else:
            error = '用户名或密码错误'
            return render(request, 'login.html',{'error': error})

    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})
