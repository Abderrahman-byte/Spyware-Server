from .init_db import initDb
from .add_access import add_access

class Command :
    def __init__(self, name :str, description: str, callback : callable) :
        self.name = name
        self.description = description
        self.callback = callback
    
    def run (self, *args, **kwargs) :
        self.callback(*args, **kwargs)


commands_list = []

commands_list.append(Command("init-db", "Initialize database tables", initDb))
commands_list.append(Command("add-access", "Add credentials access", add_access))