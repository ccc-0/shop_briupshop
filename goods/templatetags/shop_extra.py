from django import template
from goods.models import *

register = template.Library()

#自定义模板标签
@register.simple_tag
def TypeTag():
    # 分类信息获取
    typelist = GoodsType.objects.all()  # =>  [<>,<>]
    all_types = []
    for one in typelist:
        if one.level == 1:
            one_type = {}
            one_type['id'] = one.id
            one_type['name'] = one.name
            one_type['two'] = []
            for two in typelist:
                # 拿到所有的二级分类并且是该一级分类下的二级分类
                if two.level == 2 and two.uper_type_id == one.id:  # 外键查找多种方法
                    two_type = {}
                    two_type['id'] = two.id
                    two_type['name'] = two.name
                    two_type['three'] = []
                    for three in typelist:
                        # 拿到所有的三级分类并且是该一级分类下的三级分类
                        if three.level == 3 and three.uper_type_id == two.id:
                            three_type = {}
                            three_type['id'] = three.id
                            three_type['name'] = three.name
                            two_type['three'].append(three_type)
                    one_type['two'].append(two_type)
            all_types.append(one_type)
    # pprint(all_types)
    return all_types

