import json
import requests
import cruds 
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.category import Category
from models.label import Label
from models.shop import Shop
from router.utils import custom_reponse
from sqlalchemy.orm import Session
from db.get_db import get_db
from models.product import Product


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/lazada")
def getListProductLazada(db: Session = Depends(get_db) ):
    try:
        headers_dict = {"Cookie": "__wpkreporterwid_=16f57696-fc75-4461-3851-f663d47d47a2; lzd_cid=df798465-c838-4af4-dd17-8df9a06422be; t_uid=df798465-c838-4af4-dd17-8df9a06422be; hng=VN|vi|VND|704; userLanguageML=vi; t_fv=1668435671171; _bl_uid=khlpgaqRgt6vmbiIjr0j6d7bR5zh; cna=1zz5G4XEx0YCASpzc0kbO12R; _gcl_au=1.1.1607850565.1668435671; xlly_s=1; _fbp=fb.1.1669299914979.446593310; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19321%7CMCMID%7C54073696294758083143550424436731232245%7CMCAAMLH-1669904715%7C3%7CMCAAMB-1669904715%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1669307115s%7CNONE%7CvVersion%7C5.2.0; _uetsid=d00354206c0311edaae51960dadec13b; _uetvid=d003afa06c0311ed9b08ddac2f35e1c1; t_sid=VZhzhtiwVx7SD5OPlOO5YVBcxox8Fss5; utm_origin=https://www.google.com/; utm_channel=SEO; lzd_sid=1b05fd4dc38d58c7a8fa89c462c28b9a; _m_h5_tk=87c2d6dc6c90eb9b7240bf154285e3fe_1669368322564; _m_h5_tk_enc=60d9d1d16e6f4cbeb728a67c3f482a1c; _tb_token_=ee395845d8bee; _gcl_aw=GCL.1669359684.CjwKCAiAyfybBhBKEiwAgtB7foUizhPzbcgSH8twJpW8ZmAA69zrJEy8u0Yqed1b6ekt45OUyxnRNxoCSBoQAvD_BwE; x5sec=7b22617365727665722d6c617a6164613b32223a226464313263616263626535636638393961376533393832326333313161623964434d5851675a7747454c2b35384a667237347243585444423561666b2b502f2f2f2f38425141493d227d; tfstk=cPrVBuNWceKWKPi1JmiaY4xy8jnAZXw0I3kIo1YFhraVTx0cirdtEFBrUA9ysqf..; l=eBE8aTQ7T1GK5uvhBOfwourza77OSIRAguPzaNbMiOCP_V1p5KmRW65vXLT9C3MNh626R3u4g_J9BeYBYIv8uzdMX9C7Ykkmn; isg=BNvb70JVPOKxrEBk85-qCzSyajZFsO-yprTG0c0Yt1rxrPuOVYB_AvkqRhQijEeq"}

        lables = [
            "dien-thoai-di-dong",
            "laptop"
        ]
        shop = Shop(name = "lazada", link = "https://www.lazada.vn/")
        idShop = cruds.shop.getByName(db , "lazada")
        shops = []
        if idShop is None:
            idShop = cruds.shop.create(db , shop)
        list_data = []
        for label in lables:
            try:
                if ( label == "dien-thoai-di-dong"):
                    idCategory = cruds.category.getByName(db , "Điện thoại")
                    if idCategory is None:
                        data = Category(
                            name = "Điện thoại"
                        )
                        idCategory = cruds.category.create(db , data)      
                print(idCategory.name)
                if ( label == "laptop"):
                    idCategory = cruds.category.getByName(db , "Laptop")
                    if idCategory is None:
                        data = Category(
                            name = "Laptop"
                        )
                        idCategory = cruds.category.create(db , data)
                for i in range(1,2) : 
                    url='https://www.lazada.vn/{}/?ajax=true&clickTrackInfo=94ab4ef5-9f79-4ca5-8773-58354cec4a2c__4518__272060244__static__0.09941919720767887__299225__7253&from=hp_categories&isFirstRequest=true&item_id=272060244&page={}&spm=a2o4n.home.categories.2.190565cbzJ6HXP&up_id=272060244&version=v2'.format(label, i)
                    response = requests.get(url, headers=headers_dict)
                    data = json.loads(response.text)
                    data = data["mods"]["listItems"]
                    for item in data:
                        thumbs = item["thumbs"]
                        for index in thumbs:
                            link = "https://www.lazada.vn/{}".format(index['itemUrl'])
                        name = item['name']
                        image = item['image']
                        priceSale = item['priceShow']
                        price = item.get('originalPriceShow' , item['priceShow'])
                        ratingScore =  item['ratingScore']    
                        product = Product(
                            name = str(name),
                            link = str(link),
                            image = str(image),
                            price = str(price),
                            priceSale =  str(priceSale),
                            rating = str(ratingScore),
                            labelId = None,
                            shopId = idShop.id,
                            categoryId = idCategory.id,     
                        )
                        data_name = None
                        try:
                            data_name = cruds.product.getByName(db , name)
                        except Exception as e:
                            return name
                        if ( data_name != None):
                            cruds.product.update(db , data_name.id , product)
                        else:
                            cruds.product.create(db , product)
                        list_data.append(product)
            except Exception as e:
                return "{} {}".format(i , label)
        return custom_reponse(http_status=200 , data= list_data)
    except Exception as e:
        return HTTPException(status_code=400 , detail="Crawl data Lazada error")
