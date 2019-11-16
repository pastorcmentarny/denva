import json

path = 'configs/config.json'


def save_cfg(cfg: dict):
    with open(path, 'w') as config_file:
        config_file.write(json.dumps(cfg))


def load_cfg() -> dict:
    with open(path, 'r') as config:
        return json.load(config)


def update_healthcheck(ip: str):
    config = load_cfg()
    print(config['system']['ip'])
    config['system']['ip'] = '{}'.format(ip)
    print(config['system']['ip'])
    save_cfg(config)


def get_healthcheck_ip() -> str:
    config = load_cfg()
    return config['system']['ip']
