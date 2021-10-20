import os, json

# Get Config data from file specified in argv and verify it
def get_config (*args):
    default_config_file = "./config.json"
    config_file = args[0] if len(args) > 0 else None
    
    if config_file is None and not os.path.exists(default_config_file) :
        print ("[ERROR] config file not specified and default file doesn't exists")
        print (f"[*] please, create config file {default_config_file} or specify your file as an argument")
        return None
    elif config_file is None :
        config_file = default_config_file
    elif config_file is not None and not os.path.exists(default_config_file) :
        print ("[ERROR] the config file specified doesn't exists")
        return None

    config_file_stream = open(config_file)
    config = json.loads(config_file_stream.read())
    config_file_stream.close()

    if 'db' not in config :
        print ("[ERROR] db field is not in config file")
        return None
    
    return config