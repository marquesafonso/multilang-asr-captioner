import yaml

def api_configs(config_file):
    with open(config_file, 'r') as f:
        db_config = yaml.safe_load(f)
    return db_config["api_config"]