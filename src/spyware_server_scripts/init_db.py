import os, json

def initDb (*args):
    default_config_file = "./config.json"
    config_file = args[0] if len(args) > 0 else None
    
    if config_file is None and not os.path.exists(default_config_file) :
        print ("[ERROR] config file not specified and default file doesn't exists")
        print (f"[*] please, create config file {default_config_file} or specify your file as an argument")
        return
    elif config_file is None :
        config_file = default_config_file
    elif config_file is not None and not os.path.exists(default_config_file) :
        print ("[ERROR] the config file specified doesn't exists")
        return

    config_file_stream = open(config_file)
    config = json.loads(config_file_stream.read())
    config_file_stream.close()
    
    print(config)
    print ("[DONE] init db")