from bs4 import BeautifulSoup
from functools import wraps
import asyncio
import aiohttp
from app import db
from app.models import Errors, Prices


def get_price(func):
    @wraps(func)
    async def wrapper(session, url, *args, **kwargs):
        async with session.get(url) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, "html.parser")

        res = await func(session, soup, *args, **kwargs)

        if res:
            price = res.text
            price = int(''.join(i for i in price if i.isdigit()))
        else:
            price = 'error parse'

        return price

    return wrapper


async def get_data_mvideo(session, url):

    price = 0
    product_id = url[url.rfind('-') + 1:]

    cookies = {
        '__lhash_': 'e8614bb49074d9107748360d7c33bdba',
        'MVID_AB_PERSONAL_RECOMMENDS': 'true',
        'MVID_AB_UPSALE': 'true',
        'MVID_ACCESSORIES_PDP_BY_RANK': 'true',
        'MVID_ALFA_PODELI_NEW': 'true',
        'MVID_CASCADE_CMN': 'true',
        'MVID_CHAT_VERSION': '4.16.4',
        'MVID_CITY_ID': 'CityCZ_975',
        'MVID_CREDIT_DIGITAL': 'true',
        'MVID_CREDIT_SERVICES': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_DISPLAY_ACCRUED_BR': 'true',
        'MVID_EMPLOYEE_DISCOUNT': 'true',
        'MVID_FILTER_CODES': 'true',
        'MVID_FILTER_TOOLTIP': '1',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_GEOLOCATION_NEEDED': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_INTERVAL_DELIVERY': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_KLADR_ID': '7700000000000',
        'MVID_LAYOUT_TYPE': '1',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_NEW_MBONUS_BLOCK': 'true',
        'MVID_PODELI_PDP': 'true',
        'MVID_PROMO_PAGES_ON_2': 'true',
        'MVID_REGION_ID': '1',
        'MVID_REGION_SHOP': 'S002',
        'MVID_SERVICES': '111',
        'MVID_SERVICE_AVLB': 'true',
        'MVID_SINGLE_CHECKOUT': 'true',
        'MVID_SP': 'true',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_TYP_CHAT': 'true',
        'MVID_WEB_SBP': 'true',
        'SENTRY_ERRORS_RATE': '0.1',
        'SENTRY_TRANSACTIONS_RATE': '0.5',
        'MVID_ENVCLOUD': 'prod1',
        'mindboxDeviceUUID': '615ee4bf-4f34-4266-a91a-6c2431f99331',
        'directCrm-session': '%7B%22deviceGuid%22%3A%22615ee4bf-4f34-4266-a91a-6c2431f99331%22%7D',
        '_ym_uid': '170655851558015523',
        '_ym_d': '1706558515',
        '_ga': 'GA1.1.173428318.1706558515',
        'uxs_uid': '42136370-bee1-11ee-a188-c95be0cf884d',
        'tmr_lvid': '5232fcea7f8d65d6d4eab8cdf97e66f2',
        'tmr_lvidTS': '1706558518071',
        'flocktory-uuid': '1919e9fd-13be-4815-a433-2db56e0da8f7-6',
        'gdeslon.ru.__arc_domain': 'gdeslon.ru',
        'gdeslon.ru.user_id': 'cab60ffb-fe2e-47ff-a459-c9e5511626d0',
        'advcake_track_id': 'bac37b52-76f9-84bb-11d0-cdc57c4f220d',
        'advcake_session_id': 'ebdae27d-4192-837f-acbc-f5350e75c9c9',
        'flacktory': 'no',
        'BIGipServeratg-ps-prod_tcp80': '1141169162.20480.0000',
        'bIPs': '-826759811',
        'adrcid': 'A8pCMqsA2IlivLGO3TPZBMQ',
        '_gpVisits': '{"isFirstVisitDomain":true,"idContainer":"100025D5"}',
        'adid': '170655851916577',
        'afUserId': 'a6d58cb2-3b97-4103-9f30-d2e84f9b1b05-p',
        'AF_SYNC': '1706558521005',
        '__hash_': '00e04373bf4751f7676c3a08b94a4484',
        'gsscgib-w-mvideo': '8xgcc0UCOWk3pytxyv0JVAif1Dl8I1ZEcCgzzb/RlY3h8wI8K6HFT43mCSTE3cUo0I1Okte2NDZoXMP1kGLnF6TAzG4iCqFujnL7Ve7m+qaus/faQVFBVVZDdjRzmMdOyUBPOXCn9J0oMl6jO9pA7yH0bQ7a7e/VomQddH4K5LO6cFUO8+BlLW33mhXl+liudAONxNhaCYZH2TYk0XAB8+Np4DPF5niSSXzdOH7hVRDsLVG59x9t0oGN11FzUA==',
        'gsscgib-w-mvideo': '8xgcc0UCOWk3pytxyv0JVAif1Dl8I1ZEcCgzzb/RlY3h8wI8K6HFT43mCSTE3cUo0I1Okte2NDZoXMP1kGLnF6TAzG4iCqFujnL7Ve7m+qaus/faQVFBVVZDdjRzmMdOyUBPOXCn9J0oMl6jO9pA7yH0bQ7a7e/VomQddH4K5LO6cFUO8+BlLW33mhXl+liudAONxNhaCYZH2TYk0XAB8+Np4DPF5niSSXzdOH7hVRDsLVG59x9t0oGN11FzUA==',
        '_sp_ses.d61c': '*',
        '_ym_isad': '2',
        '_ga_CFMZTSS5FM': 'GS1.1.1706693533.4.0.1706693533.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1706693533.4.0.1706693533.60.0.0',
        '_sp_id.d61c': '28110bc9-21e0-4688-ac00-653164770ad9.1706558515.3.1706693537.1706605717.16ce5ef8-b2f9-468c-814d-ec24a9715235.13e715b2-2695-44fb-871b-8b81dce86218.9e77620e-4292-41c0-a203-0782a95f1d2f.1706693533283.7',
        '_gp100025D5': '{"hits":1,"vc":1}',
        'tmr_detect': '0%7C1706693539257',
        'fgsscgib-w-mvideo': '7bp6511548d45d78d37fd6f33b039d4dd3b634d4',
        'fgsscgib-w-mvideo': '7bp6511548d45d78d37fd6f33b039d4dd3b634d4',
        'gsscgib-w-mvideo': '19yumlJB+LTOvYJy27E8sFRwUNLnjg4hHgEgwSs/qTNwQlWxOo9Yt6AhGfnIS4llgPrk1fV0tGDLU0/kBFaEgdMy2Vs48DSlzsAtU1qsmz9j12QJV+iBeMCrdnIgtSAfsQdr5VGSCrQtB90Xdm1NaPb68CNsLaJ/KyGECCeziN6F5YAYwd8LFom5d+aILE/VkFlMibpsqXlZ2R7ZmHs6AeyMm2vQQhxQjt5GwKG4kazTSueT55SEDb5M6YsYhA==',
        'cfidsgib-w-mvideo': 'mmTjV6mFxzI+vSd1xyRaETLq5wfHUsJsMHsL9G9taLjVYXB0hHYLVMNrVZXsNJVZ4zaoT+GqHkHduKPUWdRi+1bBwGyCitNw6NKe4cwA5lYmjdIXbJL27mRH4lOOOHW4FR1DZIP7//qVqA50iNMZvRKkUQ7VUmoZGgEfi5o=',
    }

    headers = {
        'authority': 'www.mvideo.ru',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'cookie': '__lhash_=e8614bb49074d9107748360d7c33bdba; MVID_AB_PERSONAL_RECOMMENDS=true; MVID_AB_UPSALE=true; MVID_ACCESSORIES_PDP_BY_RANK=true; MVID_ALFA_PODELI_NEW=true; MVID_CASCADE_CMN=true; MVID_CHAT_VERSION=4.16.4; MVID_CITY_ID=CityCZ_975; MVID_CREDIT_DIGITAL=true; MVID_CREDIT_SERVICES=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_DISPLAY_ACCRUED_BR=true; MVID_EMPLOYEE_DISCOUNT=true; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GTM_ENABLED=011; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7700000000000; MVID_LAYOUT_TYPE=1; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PODELI_PDP=true; MVID_PROMO_PAGES_ON_2=true; MVID_REGION_ID=1; MVID_REGION_SHOP=S002; MVID_SERVICES=111; MVID_SERVICE_AVLB=true; MVID_SINGLE_CHECKOUT=true; MVID_SP=true; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; MVID_ENVCLOUD=prod1; mindboxDeviceUUID=615ee4bf-4f34-4266-a91a-6c2431f99331; directCrm-session=%7B%22deviceGuid%22%3A%22615ee4bf-4f34-4266-a91a-6c2431f99331%22%7D; _ym_uid=170655851558015523; _ym_d=1706558515; _ga=GA1.1.173428318.1706558515; uxs_uid=42136370-bee1-11ee-a188-c95be0cf884d; tmr_lvid=5232fcea7f8d65d6d4eab8cdf97e66f2; tmr_lvidTS=1706558518071; flocktory-uuid=1919e9fd-13be-4815-a433-2db56e0da8f7-6; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=cab60ffb-fe2e-47ff-a459-c9e5511626d0; advcake_track_id=bac37b52-76f9-84bb-11d0-cdc57c4f220d; advcake_session_id=ebdae27d-4192-837f-acbc-f5350e75c9c9; flacktory=no; BIGipServeratg-ps-prod_tcp80=1141169162.20480.0000; bIPs=-826759811; adrcid=A8pCMqsA2IlivLGO3TPZBMQ; _gpVisits={"isFirstVisitDomain":true,"idContainer":"100025D5"}; adid=170655851916577; afUserId=a6d58cb2-3b97-4103-9f30-d2e84f9b1b05-p; AF_SYNC=1706558521005; __hash_=00e04373bf4751f7676c3a08b94a4484; gsscgib-w-mvideo=8xgcc0UCOWk3pytxyv0JVAif1Dl8I1ZEcCgzzb/RlY3h8wI8K6HFT43mCSTE3cUo0I1Okte2NDZoXMP1kGLnF6TAzG4iCqFujnL7Ve7m+qaus/faQVFBVVZDdjRzmMdOyUBPOXCn9J0oMl6jO9pA7yH0bQ7a7e/VomQddH4K5LO6cFUO8+BlLW33mhXl+liudAONxNhaCYZH2TYk0XAB8+Np4DPF5niSSXzdOH7hVRDsLVG59x9t0oGN11FzUA==; gsscgib-w-mvideo=8xgcc0UCOWk3pytxyv0JVAif1Dl8I1ZEcCgzzb/RlY3h8wI8K6HFT43mCSTE3cUo0I1Okte2NDZoXMP1kGLnF6TAzG4iCqFujnL7Ve7m+qaus/faQVFBVVZDdjRzmMdOyUBPOXCn9J0oMl6jO9pA7yH0bQ7a7e/VomQddH4K5LO6cFUO8+BlLW33mhXl+liudAONxNhaCYZH2TYk0XAB8+Np4DPF5niSSXzdOH7hVRDsLVG59x9t0oGN11FzUA==; _sp_ses.d61c=*; _ym_isad=2; _ga_CFMZTSS5FM=GS1.1.1706693533.4.0.1706693533.0.0.0; _ga_BNX5WPP3YK=GS1.1.1706693533.4.0.1706693533.60.0.0; _sp_id.d61c=28110bc9-21e0-4688-ac00-653164770ad9.1706558515.3.1706693537.1706605717.16ce5ef8-b2f9-468c-814d-ec24a9715235.13e715b2-2695-44fb-871b-8b81dce86218.9e77620e-4292-41c0-a203-0782a95f1d2f.1706693533283.7; _gp100025D5={"hits":1,"vc":1}; tmr_detect=0%7C1706693539257; fgsscgib-w-mvideo=7bp6511548d45d78d37fd6f33b039d4dd3b634d4; fgsscgib-w-mvideo=7bp6511548d45d78d37fd6f33b039d4dd3b634d4; gsscgib-w-mvideo=19yumlJB+LTOvYJy27E8sFRwUNLnjg4hHgEgwSs/qTNwQlWxOo9Yt6AhGfnIS4llgPrk1fV0tGDLU0/kBFaEgdMy2Vs48DSlzsAtU1qsmz9j12QJV+iBeMCrdnIgtSAfsQdr5VGSCrQtB90Xdm1NaPb68CNsLaJ/KyGECCeziN6F5YAYwd8LFom5d+aILE/VkFlMibpsqXlZ2R7ZmHs6AeyMm2vQQhxQjt5GwKG4kazTSueT55SEDb5M6YsYhA==; cfidsgib-w-mvideo=mmTjV6mFxzI+vSd1xyRaETLq5wfHUsJsMHsL9G9taLjVYXB0hHYLVMNrVZXsNJVZ4zaoT+GqHkHduKPUWdRi+1bBwGyCitNw6NKe4cwA5lYmjdIXbJL27mRH4lOOOHW4FR1DZIP7//qVqA50iNMZvRKkUQ7VUmoZGgEfi5o=',
        'referer': url,
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    }

    params = {
        'productIds': product_id,
        'isPromoApplied': 'true',
        'addBonusRubles': 'true',
    }

    response = await session.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                     headers=headers, allow_redirects=False)

    redirect_url = response.headers['Location']

    async with session.get(redirect_url, headers=headers, cookies=cookies, allow_redirects=True) as response_redirect:
        prices_json = await response_redirect.json()

        if 'errors' in prices_json:
            price = ''.join(prices_json.get('errors'))
        else:
            prices = prices_json.get('body').get('materialPrices')

            for product_price in prices:
                if product_price.get('productId') == product_id:
                    price = product_price.get('price').get('salePrice')
                    break

    return price


@get_price
async def get_data_redfox(session, soup):
    div_price = soup.find('div', class_='detail-price')
    price_soup = div_price.find(class_='price_sale')
    if not price_soup:
        price_soup = div_price.find(class_='price')

    return price_soup


@get_price
async def get_data_citycycle(session, soup):
    div_price = soup.find('div', class_='big-price-table-cell')
    price_soup = div_price.find(class_='big-price-value')
    price_soup = price_soup.find('big')

    return price_soup


@get_price
async def get_data_doublesports(session, soup):
    div_price = soup.find('span', class_='woocommerce-Price-amount amount')
    price_soup = div_price.find('bdi')

    return price_soup


@get_price
async def get_data_velosport(session, soup):
    div_price = soup.find('div', class_='product-item-detail-pay-block')
    price_soup = div_price.find(class_='product-item-detail-price-current')

    return price_soup


@get_price
async def get_data_kant(session, soup):
    price_soup = None
    div_price = soup.find('span', class_='CatalogProduct_currentPrice__3kJLc')
    if div_price:
        price_soup = div_price.find('span')

    return price_soup


@get_price
async def get_data_sportmarafon(session, soup):
    price_soup = None
    div_price = soup.find('div', class_='q-product-prices__left')
    if div_price:
        price_soup = div_price.find('div', class_='q-product-prices__value')

    return price_soup


async def get_data(session, url):
    price = ''

    if url.startswith('https://redfoxmsk.ru/'):
        price = await get_data_redfox(session, url)
    if url.startswith('https://www.mvideo.ru/'):
        price = await get_data_mvideo(session, url)
    if url.startswith('https://citycycle.ru/'):
        price = await get_data_citycycle(session, url)
    if url.startswith('https://double-sports.ru/'):
        price = await get_data_doublesports(session, url)
    if url.startswith('https://velosport.ru/'):
        price = await get_data_velosport(session, url)
    if url.startswith('https://www.kant.ru/'):
        price = await get_data_kant(session, url)
    if url.startswith('https://sport-marafon.ru/'):
        price = await get_data_sportmarafon(session, url)

    return {'url': url, 'price': price}


async def async_save_price(urls_products):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls_products:
            task = asyncio.create_task(get_data(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)

    try:
        for res in results:
            price_url = res['price']
            url = res['url']
            product_id = urls_products[url]

            if type(price_url) is str:
                error = Errors(product_id=product_id, text=price_url, url=url)
                db.session.add(error)
            else:
                price = Prices(product_id=product_id, price=price_url, url=url)
                db.session.add(price)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def save_price(urls_products):
    asyncio.run(async_save_price(urls_products))

