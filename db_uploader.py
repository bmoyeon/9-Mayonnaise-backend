import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE","laneige.settings")
django.setup()

#여기서 원하면 모델 추가하기
from product.models import *
CSV_PATH_PRODUCTS='laneige_test.csv'

# Menu.objects.create(name ="브랜드")
# Menu.objects.create(name ="베스트/신상품"),Menu.objects.create(name ="스킨케어")
# Menu.objects.create(name ="옴므"),Menu.objects.create(name ="이벤트")

# Type.objects.create(name ="클렌징")
# Type.objects.create(name ="스킨/미스트"),Type.objects.create(name ="로션/에멀젼")
# Type.objects.create(name ="세럼/에센스"),Type.objects.create(name ="젤/크림")
# Type.objects.create(name ="마스크/팩"),Type.objects.create(name ="아이케어")
# Type.objects.create(name ="선케어"),Type.objects.create(name ="립케어")

# Type.objects.create(name ="밸런싱"),Type.objects.create(name ="수분/보습")
# Type.objects.create(name ="민감/진정"),Type.objects.create(name ="브라이트닝")
# Type.objects.create(name ="안티에이징"),Type.objects.create(name ="피지/모공")
# Type.objects.create(name ="자외선차단")

# Type.objects.create(name ="래디언-C"),Type.objects.create(name ="클리어-C")
# Type.objects.create(name ="베이직케어"),Type.objects.create(name ="워터뱅크")
# Type.objects.create(name ="포커스 액티브 앰플"),Type.objects.create(name ="퍼펙트리뉴")
# Type.objects.create(name ="타임프리즈"),Type.objects.create(name ="슬리핑케어")
# Type.objects.create(name ="프레시카밍"),Type.objects.create(name ="크림 스킨")
# Type.objects.create(name ="화이트듀")

# Type.objects.create(name ="크림")
# Type.objects.create(name ="BB"),Type.objects.create(name ="주름/탄력/보습")
# Type.objects.create(name ="액티브워터"),Type.objects.create(name ="블루에너지")
# Type.objects.create(name ="오일컨트롤")

# types = Type.objects.all()

# for tt in types :
    
#     Category.objects.create(menu =(Menu.objects.get(name="스킨케어")),
#                     type_name =(Type.objects.get(name = tt.name)))

# for homme in types :
        
#     Category.objects.create(menu =(Menu.objects.get(name="옴므")),
#                     type_name =(Type.objects.get(name = homme.name)))


# with open(CSV_PATH_PRODUCTS) as in_file:
#     data_reader = csv.reader(in_file)

#     next(data_reader,None)
#     for row in data_reader:
       
#         tags = row[3]
#         tags = tags.split(',')
#         for tag in tags:
#             tag_name = tag.strip('[]"\' ')
            
#             if not Tag.objects.filter(name = tag_name).exists():
#                 Tag.objects.create(name = tag_name)

#         product_name_ko = row[4]
#         product_id = Product.objects.get(name_ko = product_name_ko).id

#         tags = row[3]
#         tags = tags.split(',')
#         for tag in tags:
#             tag_name = tag.strip('[]"\' ')
#             tag_id = Tag.objects.get(name = tag_name).id

#             if not ProductTag.objects.filter(
#                 product_id = product_id,
#                 tag_id = tag_id
#                 ).exists():
#                 ProductTag.objects.create(
#                     product_id = product_id,
#                     tag_id = tag_id
#                 )
    
#         image_str= row[10]
#         image_strip = image_str.strip("[]")
#         image_rep = image_strip.replace("'","")
#         image_aa = image_rep.replace(" ","")
#         image_list = image_aa.split(",")
        
#         for image in image_list :
        
#             Image.objects.create(
#                 image_url = image,
#                 product = Product.objects.get(name_ko=row[4])
          
#         )

#         Product.objects.create(
#             name_ko          = row[4],
#             name_en          = row[5],
#             description      = row[6],
#             price            = row[8],
#             volume           = row[7],
#             ingredient       = row[9],
#             feature          = row[11]  
#         )

       
#         type_num = Type.objects.filter(name=row[0])
        
#         for i in type_num :
#             product_id = Product.objects.get(name_ko=row[4]).id
            
#             typpp = Type.objects.get(name=i.name).id
#             type_num = Category.objects.get(type_name=typpp).id
            
            
#             ProductCategory.objects.create(
#                 product= Product.objects.get(name_ko=row[4]),
#                 category = Category.objects.get(type_name=typpp)
#                 )
        
#         type_num = Type.objects.filter(name=row[1])
        
#         for i in type_num :
#             product_id = Product.objects.get(name_ko=row[4]).id
            
#             typpp = Type.objects.get(name=i.name).id
#             type_num = Category.objects.get(type_name=typpp).id
           
            
#             ProductCategory.objects.create(
#                 product= Product.objects.get(name_ko=row[4]),
#                 category = Category.objects.get(type_name=typpp)
#                 )
            
#         type_num = Type.objects.filter(name=row[2])
        
#         for i in type_num :
#             product_id = Product.objects.get(name_ko=row[4]).id
            
#             typpp = Type.objects.get(name=i.name).id
#             type_num = Category.objects.get(type_name=typpp).id
            
            
#             ProductCategory.objects.create(
#                 product= Product.objects.get(name_ko=row[4]),
#                 category = Category.objects.get(type_name=typpp)
#                 )
            
        
 