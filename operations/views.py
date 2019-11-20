from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from .models import *
from .forms import *
from users.models import ShopAddress
from datetime import datetime

# Create your views here.

class FlowListView(View):
    def get(self,request):
        #判断用户是否登录
        if request.user.is_authenticated:
            #当前用户的购物车所含商品信息
            goods_list = ShoppingCart.objects.filter(user=request.user)
            # name = 10
            # addtime = datetime.now()
            # 购物车总价
            all_price = 0
            for good in goods_list:
                xiaoji = good.goods.actual_price * good.numbers
                all_price += xiaoji

            return render(request,'flow.html',{
                'goods_list':goods_list ,
                'all_price': all_price,
                # 'name':name,
                # 'addtime':addtime,
            })
        else:
            return render(request,'login.html')

class Flow2ListView(View):
    def get(self,request):
        #判断用户是否登录
        if request.user.is_authenticated:
            #当前用户的购物车所含商品信息
            goods_list = ShoppingCart.objects.filter(user=request.user)
            # name = 10
            # addtime = datetime.now()
            # 购物车总价
            all_price = 0
            for good in goods_list:
                xiaoji = good.goods.actual_price * good.numbers
                all_price += xiaoji
            return render(request,'flow2.html',{
                'goods_list':goods_list ,
                'all_price': all_price,
                # 'name':name,
                # 'addtime':addtime,
            })
        else:
            return render(request,'login.html')

class FlowAddView(View):
    def get(self,request,good_id,nums):
        # 判断用户是否登录
        if request.user.is_authenticated:
            #逻辑：判断该商品是否加购过： 否：新增一条商品数据  是：该用户该商品的数量+nums
            thegood = ShoppingCart.objects.filter(user=request.user).filter(goods=good_id)
            if thegood:
                thegood = ShoppingCart.objects.get(goods=good_id)
                thegood.numbers = thegood.numbers+nums
                thegood.save()  # 异常捕获
                return redirect(reverse('operations:flow'))
            else:
                cart = ShoppingCart()
                cart.numbers = nums
                cart.user=request.user
                cart.created_time =datetime.now()
                #通过good_id获取商品对象
                good = Goods.objects.get(pk=good_id)
                cart.goods = good
                cart.save() #异常捕获
                return redirect(reverse('operations:flow'))

        else:
            return render(request,'login.html')

#删除购物车数据
class DeleteFlowView(View):
    def post(self,request):
        flowid = request.POST.get('flowid','')
        flow = ShoppingCart.objects.get(id= flowid)
        flow.delete()
        return render(request,'flow.html')

#确认并填写订单
class AddOrderView(View):
    def get(self,request,goodids,goodnums,all_price):
        """"
        0.判断用户是否登录
        1.获取用户的收获地址
        2.根据提交的goodids,goodnums获取商品信息 numbers（2，3，）
          2.1 去除字符串的最后一个字符goodids[:-1]
          2.2 将字符串切割为一个列表 idlist = str.split(',')
          2.3 获取数据Goods.objects.filter(pk__in=idlist)
        """
        if request.user.is_authenticated:
            # 获取用户的收获地址
            address = ShopAddress.objects.filter(user= request.user)
            # 根据提交的goodids获取商品信息
            goodids = goodids[:-1]
            goodnums = goodnums[:-1]
            idlist = goodids.split(',')
            numlist = goodnums.split(',')
            idlist1 = list(map(int,idlist))
            numlist1 = dict(zip(idlist,numlist))
            goodslist = Goods.objects.filter(pk__in = idlist1)
            #添加购买数量属性
            for good in goodslist:
                good.nums = numlist1[str(good.id)]

            return render(request, 'flow2.html', {
                'address': address,
                'goodslist':goodslist,
                'all_price':all_price,
            })
        else:
            return render(request,'login.html',{})

#增加收货地址
class AddAddressView(View):
    def post(self,request):
        address_form = AddAddressForm(request.POST)
        if address_form.is_valid():
            name = request.POST.get('name','')
            address = request.POST.get('sheng','')+request.POST.get('shi','')+request.POST.get('xian','')
            detailedaddress = request.POST.get('detailedaddress','')
            zipcode = request.POST.get('zipcode','')
            tel = request.POST.get('tel','')

            newaddress = ShopAddress()
            newaddress.user = request.user
            newaddress.name = name
            newaddress.tel = tel
            newaddress.address = str(address + detailedaddress)
            newaddress.zipcode = zipcode
            newaddress.save()

        else:
            return redirect(reverse('operations:addorder'))

#确认收货地址,添加订单
class OrderListView(View):
    def get(self,request,goodids,goodnums,all_price,theaddress):
        """"
        0.判断用户是否登录
        1.获取用户的收获地址
        2.根据提交的goodids获取商品信息 numbers（2，3，）
          2.1 去除字符串的最后一个字符goodids[:-1]
          2.2 将字符串切割为一个列表 idlist = str.split(',')
          2.3 获取数据Goods.objects.filter(pk__in=idlist)
        3.实例化订单表，存储数据
        4实例化订单详情表，存储数据
        """
        if request.user.is_authenticated:
            # 获取用户的收获地址
            address = ShopAddress.objects.get(address=theaddress)
            # 实例化订单表，存储数据
            order = Orders()
            order.user = request.user
            order.address = address
            order.status = 1
            order.order_time = datetime.now()
            order.total_price = all_price
            order.save()

            # 根据提交的goodids获取商品信息
            goodids = goodids[:-1]
            goodnums = goodnums[:-1]
            idlist = goodids.split(',')
            numlist = goodnums.split(',')
            idlist1 = list(map(int,idlist))
            numlist = dict(zip(idlist,numlist))
            goodslist = Goods.objects.filter(pk__in = idlist1)
            # 添加购买数量属性
            for good in goodslist:
                good.nums = numlist[str(good.id)]

                # 实例化订单详情表，存储数据
                detorder = OrderGoodsShip()
                theorderid = Orders.objects.get(id=order.id)
                detorder.orders= theorderid
                detorder.goods = int(good.nums)
                detorder.numbers = 1
                detorder.save()

            return render(request, 'order.html', {
                'goodslist':goodslist,
                'all_price':all_price,
            })
        else:
            return render(request,'login.html',{})

class FavoriteListView(View):
    def get(self,request):
        #判断用户是否登录
        if request.user.is_authenticated:
            #当前用户的购物车所含商品信息
            goods_list = Favor.objects.filter(user=request.user)
            # name = 10
            # addtime = datetime.now()

            return render(request,'favorite.html',{
                'goods_list':goods_list ,
                # 'name':name,
                # 'addtime':addtime,
            })
        else:
            return render(request,'login.html')

#添加收藏夹
class FavoriteAddView(View):
    def get(self,request,good_id,nums):
        # 判断用户是否登录
        if request.user.is_authenticated:
            # 逻辑：判断该商品是否加收藏过： 否：新增一条商品数据  是：该用户该商品的数量+nums
            thegoodid = Favor.objects.filter(goods=good_id)
            if thegoodid:
                thegoodid.numbers = thegoodid.numbers + nums
                thegoodid.save()  # 异常捕获
                return redirect(reverse('operations:favorite'))
            else:
                fav = Favor()
                fav.user=request.user
                fav.created_time =datetime.now()
                #通过good_id获取商品对象
                good = Goods.objects.get(pk=good_id)
                fav.goods = good
                fav.save() #异常捕获
                return redirect(reverse('operations:favorite'))

        else:
            return render(request,'login.html')
