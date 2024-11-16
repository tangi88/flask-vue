import uuid
from sqlalchemy import select, func
from app import app, db
from flask import jsonify, request
from app.models import Products, Prices
from app.parse import save_price


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/products', methods=['GET', 'POST'])
def all_products():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        message = 'Product added!'
        try:
            product = Products(id=uuid.uuid4().hex, name=post_data.get('name'), active=post_data.get('active'),
                               url_1=post_data.get('url_1'), url_2=post_data.get('url_2'), url_3=post_data.get('url_3'),
                               url_4=post_data.get('url_4'), url_5=post_data.get('url_5'))
            db.session.add(product)
            db.session.commit()
        except:
            db.session.rollback()
            message = 'Product not added!'
        response_object['message'] = message
    else:
        subquery_max_date = (
            select(
                Prices.product_id,
                Prices.url,
                func.max(Prices.date).label('date'),
                )
            .select_from(Prices)
            .group_by(Prices.product_id)
            .group_by(Prices.url)
            .subquery('max_date')
        )

        cte_last_prices = (
            select(
                subquery_max_date.c.product_id,
                subquery_max_date.c.url,
                subquery_max_date.c.date,
                Prices.price
                )
            .select_from(subquery_max_date)
            .join(Prices, (subquery_max_date.c.product_id == Prices.product_id)
                  & (subquery_max_date.c.url == Prices.url)
                  & (subquery_max_date.c.date == Prices.date))
            .cte('last_prices')
        )

        subquery_min_price = (
            select(
                cte_last_prices.c.product_id,
                func.min(cte_last_prices.c.price).label('price'),
                )
            .select_from(cte_last_prices)
            .group_by(cte_last_prices.c.product_id)
            .subquery('min_price')
        )

        cte_min_prices = (
            select(
                subquery_min_price.c.product_id,
                subquery_min_price.c.price,
                func.min(cte_last_prices.c.url).label('url')
                )
            .select_from(subquery_min_price)
            .join(cte_last_prices, (subquery_min_price.c.product_id == cte_last_prices.c.product_id)
                  & (subquery_min_price.c.price == cte_last_prices.c.price))
            .group_by(subquery_min_price.c.product_id)
            .group_by(subquery_min_price.c.price)
            .cte('min_prices')
        )

        query = (
            select(
                Products.id,
                Products.name,
                Products.active,
                Products.url_1,
                Products.url_2,
                Products.url_3,
                Products.url_4,
                Products.url_5,
                cte_min_prices.c.price,
            )
            .select_from(Products)
            .join(cte_min_prices, Products.id == cte_min_prices.c.product_id, isouter=True)
        )

        # print(query.compile(compile_kwargs={'literal_binds': True}))

        res = db.session.execute(query)

        data = [{'id': p.id, 'name': p.name, 'active': p.active,
                 'url_1': p.url_1, 'url_2': p.url_2, 'url_3': p.url_3,
                 'url_4': p.url_4, 'url_5': p.url_5,
                 'price': p.price} for p in res]

        response_object['products'] = data

    return jsonify(response_object)


@app.route('/products/<product_id>', methods=['PUT', 'DELETE'])
def single_product(product_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        message = 'Product updated!'
        try:
            product = Products.query.get(product_id)
            product.name = post_data.get('name')
            product.active = post_data.get('active')
            product.url_1 = post_data.get('url_1')
            product.url_2 = post_data.get('url_2')
            product.url_3 = post_data.get('url_3')
            product.url_4 = post_data.get('url_4')
            product.url_5 = post_data.get('url_5')
            db.session.commit()
        except:
            db.session.rollback()
            message = 'Product not updated!'

        response_object['message'] = message
    if request.method == 'DELETE':
        message = 'Product removed!'
        try:
            product = Products.query.get(product_id)
            db.session.delete(product)
            db.session.commit()
        except:
            db.session.rollback()
            message = 'Product not removed!'

        response_object['message'] = message
    return jsonify(response_object)


@app.route('/checkPrice', methods=['POST'])
def check_price():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        urls_products = {}
        active_products = Products.query.filter_by(active=True)

        for product in active_products:
            product_id = product.id

            for i in range(1, 6):
                url = product.get_url(i)
                if url:
                    urls_products[url] = product_id

        save_price(urls_products)

        response_object['message'] = ''

    return jsonify(response_object)


@app.route('/priceProduct/<product_id>', methods=['GET'])
def price_product(product_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        message = ''
        chartData = {'labels': [],
                     'datasets': []}

        try:
            product = Products.query.get(product_id)
            prices = []
            for price in product.prices:
                chartData['labels'].append(price.date)
                prices.append(price.price)

            chartData['datasets'].append({'label': 'Price',
                                        'backgroundColor': '#f87979',
                                        'data': prices})
        except:
            message = 'Product not found!'

        response_object['chartData'] = chartData
        response_object['message'] = message

    return jsonify(response_object)

