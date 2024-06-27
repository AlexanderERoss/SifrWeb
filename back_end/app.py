import yaml
from waitress import serve
import sifr_api as sifr_api

with open('./config.yml') as config_stream:
    config = yaml.safe_load(config_stream)

serve(sifr_api.app, host='127.0.0.1', port=config['network']['port'])
