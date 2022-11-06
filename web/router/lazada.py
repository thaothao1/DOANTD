import json
import requests
import cruds 
from msilib.schema import Class
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from base.CodeHTML import CodeHTML
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
from db.get_db import get_db
from chemas.district import DistrictCreate, DistrictUpdate


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.post("/lazada")
def getListProductShoppe(db: Session = Depends(get_db) ):

    headers_dict = {"Cookie": "__wpkreporterwid_=5ba5ec55-501b-4317-3aa1-a869147582c7; t_fv=1645335399172; cna=aMGYGjZaLWYCAQ7/m/9IHLbk; miidlaz=miidgg5qsm1g99915tiih8n; lzd_click_id=clkgg5qsm1g99915teih8e; lzd_cid=ed1893d6-5167-4189-f48f-1e6fb63efdb0; t_uid=ed1893d6-5167-4189-f48f-1e6fb63efdb0; _bl_uid=kyl0X8zw1jRna4rmsrX1tqOftez9; _gcl_au=1.1.563932938.1663167265; _ga=GA1.2.826879995.1663167281; cto_axid=Py6XbL0Au8H2UjfnyBWoSoXtGjc6qNZ4; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19280%7CMCMID%7C08667743400354860341026450300275904801%7CMCAAMLH-1666350377%7C3%7CMCAAMB-1666350377%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1665752777s%7CNONE%7CvVersion%7C5.2.0; _clck=4qw15i|1|f5p|0; sgcookie=E100nFoG2hCB5HiWAOTDYXG%2BqqsHQa4AdzBxvUHZfZYjDFBG2gnPc%2Fmm7cEq9nof%2B%2BtyvcX4Es6M2NJNaSObaP5Qp8acvVwVclxMW19BK4P%2FFko%3D; cto_bundle=vUgDN19KTFFVRFNHcndGM1g3ZFpnYURiUjJaZEVKVDFlSDVEcHBGTDNDSTZZQ1ZvWWZFZzJjSVN0UjVWcGN1UlZycVglMkZISk8zUzBXZTRDaW9hNW1FS2VpYTJTNG5HY2Yxd2VnOEFrRHFTYXhUSCUyQnEyMkNOUUVMNEZOM2pHNzNnOTFkcXRQMEpxNnFaMFdjRSUyQnhsM1h4YnhVN2clM0QlM0Q; _uetvid=20b36620920f11ec832d3f394f46af8b; t_sid=UI51IY9HIdT1w6ClgtycevfWvrwKc9Jt; utm_channel=NA; hng=VN|vi|VND|704; userLanguageML=vi; lzd_sid=1dd2a7b34eaca40b6124744d24d48eba; _m_h5_tk=14f568a3e528ff5214eecc0c7da5e8b3_1666201931214; _m_h5_tk_enc=028daefdb25f0db69bb39986aa895a8b; _tb_token_=9f87eed163be; xlly_s=1; l=eBTcdonHLLiVaWtsBOfwhurza77OGIRfguPzaNbMiOCP9QfH50zfW6yYtiLMCnMNnseWR3rp2umHB5Y3SyzHhWULJP0T6QKAOdTh.; tfstk=crrRBJs11sfkfwfn00QmT09kAAWGZ6J-tLGpvkXvAUpM1X-dilqgXBDRPvlZwtC..; isg=BDo6U5gLDeV_8oBIp8vFB_8ji2Bc677FIedmZUQzlE2YN9txLHo61J1Fh9vrpzZd; x5sec=7b22617365727665722d6c617a6164613b32223a226336343535343361323035366634643431373638353333623938336161653836434b752b774a6f47454f76326e754f4a3165715668514561446a49774d4441774f544d354e6a49334e6a73784d4a7a687837494451414d3d227d"}
    url='https://www.lazada.vn/catalog/?_keyori=ss&ajax=true&from=input&isFirstRequest=true&page=1&q=%C4%91i%E1%BB%87n%20tho%E1%BA%A1i%20di%20%C4%91%E1%BB%99ng'
    response = requests.get(url, headers=headers_dict)

    data = json.loads(response.text)
    data = data["mods"]["listItems"]
    list_data = []
    for item in data:
        text = {
            "name" : item['name'],
            "image" : item['image'],
            "price" : item['originalPriceShow'],
            "price_old" : item['priceShow'],
            "rating" : item['ratingScore'],
            "location" : item['location'],
            # "color" : item['color'],
            # "link" : "https://www.lazada.vn/{}".format(item['thumbs'])
        }
        list_data.append(text)
        # data = cruds.product.create(db , text)
    return list_data
    
