from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import *
from pprint import pprint
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# 分类信息获取
def typelistinfo():
    typelist = GoodsType.objects.all()   # =>  [<>,<>]
    # [
    #     {'id': 1, 'name': '服装', 'two': [
    #         {'id': 3, 'name': '男装', 'three': [
    #             {}, {}, ...]
    #          },
    #         {'id': 4, 'name': '女装', 'three': [
    #             {}, {}, ...]
    #          }
    #     ]
    #      },
    #     {},
    #     {},
    # ]
    all_types = []
    for one in typelist:
        if one.level==1:
            one_type ={ }
            one_type['id'] = one.id
            one_type['name']= one.name
            one_type['two'] = []
            for two in typelist:
                # 拿到所有的二级分类并且是该一级分类下的二级分类
                if two.level==2 and two.uper_type_id==one.id: #外键查找多种方法
                    two_type = {}
                    two_type['id'] = two.id
                    two_type['name']=two.name
                    two_type['three']= []
                    for three in typelist:
                        # 拿到所有的三级分类并且是该一级分类下的三级分类
                        if three.level==3 and three.uper_type_id==two.id:
                            three_type = {}
                            three_type['id']=three.id
                            three_type['name']=three.name
                            two_type['three'].append(three_type)
                    one_type['two'].append(two_type)
            all_types.append(one_type)
    # pprint(all_types)
    return all_types

def index(request):
    # return HttpResponse('helllo ccc')
    # return render(request,'goods/index.html',{ })
    return render(request,'index.html',{ })

class IndexView(View):
    def get(self,request):
        #特别推荐
        recgoods = Goods.objects.all().order_by('-comment_nums')[:4]
        #新品上架
        newgoods = Goods.objects.all().order_by('-id')[:4]
        #热门商品
        hotgoods = Goods.objects.all().order_by('-sale_nums')[:4]
        #服装商品
        fuzhuang = Goods.objects.filter(one_typename=1).order_by('-id')[:6]

        # 分类信息获取 调用上面的函数
        all_types=typelistinfo()

        #构造函数
        # areal = {'newgoods':newgoods,
        #          'hotgoods':hotgoods}
        return render(request,'index.html',{
            'recgoods':recgoods,
            'newgoods':newgoods,
            'hotgoods':hotgoods,
            'all_type':all_types,
            #'areal':areal
        })

class GoodsDetail(View):
    def get(self,request,id):
        #获取商品详情
        goodsinfo = Goods.objects.get(pk=id)  #get 返回对象 filter返回列表
        #商品详情展示图
        # dispaly = GoodsDisplayFiles.objects.filter(goods=goodinfo)
        # dispaly = GoodsDisplayFiles.objects.filter(goods_id__exact=id) #对外键查询特别
        dispaly = goodsinfo.goodsdisplayfiles_set.all() #反向查找
        return render(request,'goods.html',{
            'goodsinfo':goodsinfo,
            'display':dispaly,
        })

class GoodsList(View):
    def get(self,request,id):
        #获取满足条件的分类下的商品
        gooods_list = Goods.objects.filter(Q(one_typename_id= id)|Q(two_typename_id= id)|Q(three_typename_id=id) )

        #分页实现
        # 异常捕获
        try: # 获取当前页码
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(gooods_list,2, request=request)
        goods_page = p.page(page)
        return render(request,'list.html',{ 'goods_page':goods_page })


