#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from datetime import (
    date,
    datetime,
)
from io import StringIO
import re

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)

from balance.database import db_session
from balance.models import Balance

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def make_error(message, status_code=400):
    response = jsonify(status=status_code, message=message)
    response.status_code = status_code
    return response


def find_money(sms):
    """Extract the first mention of money from a string"""
    pattern = '£([\d]+\.[\d]{2})'
    matches = re.findall(pattern, sms)
    if matches:
        return matches[0]


def parse_date(date_str, fallback):
    """Parse a date"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return fallback


@app.route('/balance', methods=['POST'])
def update_balance():
    sms = request.form.get('sms', None)
    date_ = parse_date(request.form.get('date'), date.today())
    if sms is None:
        return make_error('SMS Message missing')
    money = find_money(sms)
    if money is None:
        return make_error(
            'SMS Message did not contain any money. Message="%s"' % sms)
    db_session.add(Balance(date=date_, amount=money))
    db_session.commit()
    return jsonify(ok=True, message='Balance updated', amount=money)


@app.route('/balance', methods=['GET'])
def get_balances():
    start = parse_date(request.args.get('start'), date.min)
    end = parse_date(request.args.get('end'), date.today())
    balances = Balance.query.filter(Balance.date >= start, Balance.date <= end)
    with StringIO() as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Date', 'Amount'])
        for balance in balances:
            writer.writerow((balance.date, balance.amount))
        response = make_response(csv_file.getvalue())
    filename = 'balances-from-{0}-to-{1}.csv'.format(
        start.isoformat(),
        end.isoformat(),
    )
    response.headers['Content-Disposition'] = (
        'attachment; filename={0}'.format(filename)
    )
    return response
