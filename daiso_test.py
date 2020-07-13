from django.shortcuts import render
from selenium import webdriver
import time
import pandas as pd

'''

'''
driver = webdriver.Chrome('/Users/user/dev/driver/chromedriver')

driver.implicitly_wait(2)
driver.get("https://www.starbucks.co.kr/menu/drink_list.do")
products = driver.find_elements_by_css_selector("li.menuDataSet > dl > dt > a")
# name = driver.find_el
# print(products[0].find_element_by_tag_name('img').get_attribute('alt'))
prod_cd = [ [pr.get_attribute('prod') , pr.find_element_by_tag_name('img').get_attribute('alt') ] for pr in products]

# 9200000002745 안됨, 아이스 돌체 블랙 밀크티, 돌체 블랙 밀크티, 아이스 유자 민트티, 유자 민트 

result = []

# 조회 불가 상품 삭제
for i,v in enumerate(prod_cd):
    if v[1] == '아이스 유자 민트 티':
        del prod_cd[i]
        print("아이스 유자 민트티 삭제")
    
    if v[1] == '유자 민트 티':
        del prod_cd[i]
        print("유자 민트티 삭제")
    
    if v[1] == '돌체 블랙 밀크 티':
        del prod_cd[i]
        print("돌체 블랙 밀크 티 삭제")
    
    if v[1] == '아이스 돌체 블랙 밀크 티':
        del prod_cd[i]
        print("아이스 돌체 블랙 밀크 티 삭제")
    
    if v[1] == '블랙 와플칩 크림 프라푸치노':
        del prod_cd[i]
        print("블랙 와플칩 크림 프라푸치노 삭제")

# driver.get('https://www.starbucks.co.kr/menu/drink_view.do?product_cd=9200000002950')
# al = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[3]/p').text
# al_data = al.partition(':')[2].lstrip()
# print(al_data)


for prod in prod_cd:
    print(prod)
    container = dict()
    cd = prod[0]
    
    driver.get("https://www.starbucks.co.kr/menu/drink_view.do?product_cd={prod_cd}".format(prod_cd = cd))
    
    # category
    category            =       driver.find_element_by_css_selector('a.cate').text
    print(category)

    # drink
    drink               =       prod[1]
    
    # size
    size                =       driver.find_element_by_class_name('selectTxt2').text

    # Nutrition
    one_serving_kcal    =       driver.find_element_by_css_selector('li.kcal > dl > dd').text
    sodium_mg           =       driver.find_element_by_css_selector('li.sodium > dl > dd').text
    saturated_fat_g     =       driver.find_element_by_css_selector('li.sat_FAT > dl > dd').text
    sugars_g            =       driver.find_element_by_css_selector('li.sugars > dl > dd').text
    protein_g           =       driver.find_element_by_css_selector('li.protein > dl > dd').text
    caffeine_mg         =       driver.find_element_by_css_selector('li.caffeine > dl > dd').text

    # 알레르기
    cause               =       driver.find_element_by_css_selector("div.product_factor > p").text.partition(':')[2].lstrip()

    # description
    description         =       driver.find_element_by_css_selector("div.product_view_wrap2").text

    # image
    image_list          =       driver.find_elements_by_css_selector("ul.product_thum > li > a")
    # print(len(image_list))
    image_url           =       ""
    for i, v in enumerate(image_list):
        image_url           +=       v.get_attribute('data-image')
        if len(image_list) > 1 and i < len(image_list):
            image_url           +=      ","
    # print(description) 

    # driver.get('https://www.starbucks.co.kr/menu/drink_list.do')
    # cate_list        =       driver.find_elements_by_css_selector('div.product_list >  dl > dt > a')
    # category = ""
    # for v in cate_list:
    #     category        =       v.text
    

    container['category']               =       category
    container['drink']                  =       drink
    container['size']                   =       size
    container['one_serving_kcal']       =       one_serving_kcal
    container['sodium_mg']              =       sodium_mg
    container['saturated_fat_g']        =       saturated_fat_g
    container['sugars_g']               =       sugars_g
    container['protein_g']              =       protein_g
    container['caffeine_mg']            =       caffeine_mg
    container['cause']                  =       cause
    container['description']            =       description
    container['image_url']              =       image_url
    
    result.append(container)

print(result)

df = pd.DataFrame(result)
df.to_csv('./starbucks.csv', index = False)


driver.close()

# shop_list = driver.find_elements_by_css_selector('li.store-item')
    # time.sleep(2)
    container = dict()
    # name
    name = value.find_element_by_class_name('store-item__name').text
    print(name)
    # address
    address = value.find_element_by_class_name('store-item__address').text
    # contact
    contact = value.find_element_by_class_name('store-item__tel').text
    container['name'] = name
    container['address'] = address
    container['contact'] = contact
    result.append(container)
    if value.find_element_by_css_selector('span.badge').text == '5':
        print('if절 시작')
        next_page = driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div/div[1]/div[2]/button[{page}]').format(page=trriger)
        if driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div/div[1]/div[2]/button[6]/span[1]') =='5':
            print("page 넘김")
            driver.find_element_by_css_selector('button.page.page--next').click()
            trriger=2
        else:
            print("버튼 클릭")
            next_page.click()
            trriger += 1