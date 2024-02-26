###############################################################################
# SifrWeb API
###############################################################################
# API that runs on Flask to serve parsed Sifr Caculations, requires the parser
# located in the same folder to parse the formulae.
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
                          radix=web_input['RadixPoint']
                          )

        def __init__(self, sifr: str):
            self.sifr = sifr
            self.no_digits = len(sifr)
            self.is_neg = sifr[0] == web_input["NegativeSign"]
    try:
        result = parser.calculate(web_input['Formula'], SetSifr)
        resp = Response("{\"Response\":200,\"Result\":\"" + result + "\"}")
        resp.headers["Content-Type"] = 'application/json'
    except Exception as e:
        print("ERROR: ", print(e))
        try:
            resp = Response("{\"Response\":422,\"Result\":\""
                            + e.message + "\"}")
        except Exception:
            resp = Response("{\"Response\":422,\"Result\": \""
                            + "Raw Error -- " + str(e) + "\"}")
        resp.headers["Content-Type"] = 'application/json'
    return resp


@app.route(config['network']['address'] + "test/calculate_sifr")
def calculate_sifr_test():

    class SetSifr(Sifr):
        ssys = SifrSystem(digit_list='0123456789',
                          neg_sym='-',
                          radix='.')

        def __init__(self, sifr: str):
            self.sifr = sifr
            self.no_digits = len(sifr)
            self.is_neg = sifr[0] == '-'

    logging.debug(SetSifr.ssys.digit_list)
    try:
        result = parser.calculate('5+4*3-2', SetSifr)
        return jsonify({'Response': 200,
                        'Result': result})
    except Exception as e:
        return jsonify({'Response': 422,
                        'Result': e.message})
