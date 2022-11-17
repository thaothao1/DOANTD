import json
import requests
import cruds 
# from msilib.schema import Class
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from base.getname import getname 
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
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

    headers_dict = {"Cookie": "__wpkreporterwid_=59221794-28c1-4970-003d-52cf2f146f25; t_fv=1634089722051; _bl_uid=UUlaa5hgxI2rO9cs0kg0a78f9OIs; lzd_cid=fb6cdbf3-832a-45c0-90f9-758f629be545; t_uid=fb6cdbf3-832a-45c0-90f9-758f629be545; hng=VN|vi|VND|704; userLanguageML=vi; _gcl_aw=GCL.1665904433.Cj0KCQjw166aBhDEARIsAMEyZh5bAaEKmaHKeFQhQg34IkRs-F6nm6kklVj0AHcHYlbaZib7xZDFc6IaAuyVEALw_wcB; t_sid=454h9271jL9VYLIZsZlG1hGUPKTb5hFe; utm_channel=NA; _m_h5_tk=27096d541c48129add21c164a1979996_1668265050062; _m_h5_tk_enc=c04027b15d98bb04756a153ebffd9d05; _gcl_au=1.1.335879936.1668257130; EGG_SESS=S_Gs1wHo9OvRHCMp98md7JMRnSmUXuAby1c3TjUT1lve_GPqb7A0pKwN3MlaW5DS5c3hjRDxSyUCiFCjtlr9GTgQfVTASuRc03HtfupzdEawOaIwfyYrSj1Y18usgd1jK6CWp5uYz3cTEHLJBZNB0bynu2DzIMxN3VnSJkoQ4BQ=; x5sec=7b22617365727665722d6c617a6164613b32223a223330343966653134626339386465323566626165333831396331386630393632434e624976707347454f4b2f2b5a50627875337a786745777765576e35506a2f2f2f2f2f41554144227d; lzd_sid=1be5b39bfd6336ae9f44e45f513404f5; _tb_token_=356387e3a3e1; tfstk=cUgPBQbdSULy5zcpBr4E7yiuBHNRZFy3CZPaqpqgSlYfEuEliqWLiqcTgW5VKuf..; l=eBrrkMMVgFnYy0HXBOfwourza77OSIRAguPzaNbMiOCPO3Cp571lW6rHZET9C3Mdh67BR3S8rH0MBeYBqIv8uzdMX9C7Ykkmn; isg=BAkJZauujtd_hnAqIdTTANMbGDVjVv2IvpntBKt-hfAv8ikE86YNWPckMEjEqpXA"}

    url='https://www.lazada.vn/dien-thoai-di-dong/?ajax=true&clickTrackInfo=94ab4ef5-9f79-4ca5-8773-58354cec4a2c__4518__272060244__static__0.09941919720767887__299225__7253&from=hp_categories&isFirstRequest=true&item_id=272060244&page=1&spm=a2o4n.home.categories.2.190565cbzJ6HXP&up_id=272060244&version=v2'
    response = requests.get(url, headers=headers_dict)
    # print(response.text)
    data = json.loads(response.text)
    data = data["mods"]["listItems"]
    shop = Shop(
        name = "lazada",
        link = "https://www.lazada.vn/",
  )
    idShop = cruds.shop.getByName(db , "lazada")
    if idShop is None:
        idShop = cruds.shop.create(db , shop)
    for item in data:
        thumbs = item["thumbs"]
        for index in thumbs:
            link  = "https://www.lazada.vn/{}".format(index['itemUrl'])
        name = item['name']
        image = item['image']
        priceSale = item['priceShow']
        price = item.get('originalPriceShow' , item['priceShow'])
        rating = item['ratingScore']
        if ( price == None):
            price =  item['priceShow']

        # shop = "https://www.lazada.vn/products/"
        # label = getname.getLabel(shop,link)
        # idLabel = cruds.label.getByName(db ,label)
        # if idLabel == None :
        #     createLabel = Label(
        #         name = label[2]
        #     )
        #     idLabel = cruds.label.create(db, createLabel)
        # print(label[2])
        # print(idLabel)
        product = Product(
            name = name,
            link = link,
            image = image,
            price = price,
            priceSale =  priceSale,
            rating = rating,
            shopId = idShop.id,     
        )
        cruds.product.create(db , product)
    return True
