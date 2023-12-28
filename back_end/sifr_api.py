###############################################################################
#
###############################################################################

# Dependency packages
from sifr import Sifr, SifrSystem
from flask import Flask, jsonify, request, Response
import yaml
import logging
from flask_cors import CORS, cross_origin

# Local imports
import back_end.parser as parser

logging.getLogger().setLevel(logging.WARNING)


with open('./back_end/config.yml') as config_stream:
    config = yaml.safe_load(config_stream)

app = Flask(__name__)
cors = CORS(app)


@app.route(config['network']['address'] + 'config')
def do():
    return jsonify(config)


@app.route(config['network']['address'] + "calculate_sifr", methods=['POST'])
@cross_origin()
def calculate_sifr():
    web_input = request.get_json()
    logging.warning(str(web_input))

    class SetSifr(Sifr):
        ssys = SifrSystem(digit_list=web_input['CharacterSet'],
                          neg_sym=web_input['NegativeSign'],
                          sep_point=web_input['XcimalSeparator']
                          )

        def __init__(self, sifr: str):
            self.sifr = sifr
            self.no_digits = len(sifr)
            self.is_neg = sifr[0] == web_input["NegativeSign"]

    result = parser.calculate(web_input['Formula'], SetSifr)
    resp = Response("{\"Result\":\"" + result + "\"}")
    resp.headers["Content-Type"] = 'application/json'
    return resp


@app.route(config['network']['address'] + "test/calculate_sifr")
def calculate_sifr_test():

    class SetSifr(Sifr):
        ssys = SifrSystem(digit_list='0123456789',
                          neg_sym='-',
                          sep_point='.')

        def __init__(self, sifr: str):
            self.sifr = sifr
            self.no_digits = len(sifr)
            self.is_neg = sifr[0] == '-'

    logging.debug(SetSifr.ssys.digit_list)
    result = parser.calculate('5+4*3-2', SetSifr)

    return jsonify({'Result': result})
