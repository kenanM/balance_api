#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from flask import (
    Flask,
    jsonify,
    request,
)

app = Flask(__name__)


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


@app.route('/balance', methods=['POST'])
def update_balance():
    sms = request.form.get('sms', None)
    if sms is None:
        return make_error('SMS Message missing')
    money = find_money(sms)
    if money is None:
        return make_error(
            'SMS Message did not contain any money. Message="%s"' % sms)
    return jsonify(message=sms, money=balance)
