from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.timezone import now, timedelta
from collections import defaultdict, OrderedDict
from django.db.models.functions import TruncDate
from .models import VisitLog, UserInfo, PageVisitCount  # 假设你记录访问日志的模型是这个
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    return render(request, 'frontend/index.html')

# Create your views here.


def custom_404(request, exception):
    return render(request, 'general/404.html', status=404)


def analytics_view(request):
    # 获取设备统计数据
    device_counts = VisitLog.objects.values(
        'device').annotate(count=Count('device'))

    # 获取按日期统计的访问趋势
    date_counts = VisitLog.objects.annotate(date=TruncDate('timestamp')).values(
        'date').annotate(count=Count('id')).order_by('date')

    # 提取设备统计信息
    device_labels = [entry['device'] for entry in device_counts]
    device_data = [entry['count'] for entry in device_counts]

    # 提取按日期统计的访问趋势
    date_labels = [entry['date'].strftime('%Y-%m-%d') for entry in date_counts]
    date_data = [entry['count'] for entry in date_counts]

    # 传递到模板
    context = {
        'device_labels': device_labels,
        'device_data': device_data,
        'date_labels': date_labels,
        'date_data': date_data,
    }

    return render(request, 'frontend/analytics.html', context)


class LoginView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            user_login_form = UserLoginForm()
            context = {'form': user_login_form}
            return render(request, 'userprofile/login.html', context)

        return redirect("frontend:index")

    def post(self, request, *args, **kwargs):
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(
                username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("frontend:index")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("frontend:index")


# 用户注册
class RegisterView(View):

    def get(self, request):
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)

    def post(self, request):
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("frontend:index")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")


@method_decorator(login_required, name="dispatch")
class User_delete(View):
    def post(self, request, id):
        user = UserInfo.objects.get(id=id)
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            # 退出登录，删除数据并返回博客列表
            logout(request)
            user.delete()
            return redirect("frontend:index")
        else:
            return HttpResponse("你没有删除操作的权限。")


# 编辑用户信息
@method_decorator(login_required, name="dispatch")
class Profile_edit(View):

    def post(self, request, id):
        user = UserInfo.objects.get(id=id)
        # user_id 是 OneToOneField 自动生成的字段
        if UserInfo.objects.filter(id=id).exists():
            profile = UserInfo.objects.get(id=id)
        else:
            profile = UserInfo.objects.create(user=user)

        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            # 取得清洗后的合法数据

            profile_cd = profile_form.cleaned_data

            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]

            profile.mobile = profile_cd['mobile']
            profile.bio = profile_cd['bio']
            profile.save()
            # 带参数的 redirect()
            return redirect("edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    def get(self, request, id):

        user = UserInfo.objects.get(id=id)
        # print("USER: ", UserInfo)
        # user_id 是 OneToOneField 自动生成的字段
        # profile = Profile.objects.get(user_id=id)

        if UserInfo.objects.filter(id=id).exists():
            profile = UserInfo.objects.get(id=id)
        else:
            profile = UserInfo.objects.create(user=user)

        profile_form = ProfileForm()
        context = {'profile_form': profile_form,
                   'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)


@api_view(['GET'])
def get_visit_count(request, page_url=None):
    print(f"Received request for page_url: {page_url}")  # 添加调试日志
    
    # 如果是首页访问
    if page_url is None:
        page_url = '/'
    # 如果是文章页面
    elif not page_url.startswith('/'):
        page_url = f"/article/{page_url}/"
    
    print(f"Normalized page_url: {page_url}")  # 添加调试日志
    
    try:
        count_obj = PageVisitCount.objects.get(page_url=page_url)
        print(f"Found existing count: {count_obj.visit_count}")  # 添加调试日志
        return Response({'count': count_obj.visit_count})
    except PageVisitCount.DoesNotExist:
        print(f"Creating new count record for: {page_url}")  # 添加调试日志
        # 如果记录不存在，创建一个新的记录
        count_obj = PageVisitCount.objects.create(
            page_url=page_url,
            visit_count=1  # 第一次访问，计数为 1
        )
        return Response({'count': 1})
