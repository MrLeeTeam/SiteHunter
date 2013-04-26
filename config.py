import sys
import ConfigParser

data = dict()
db = dict()


def init():
    global data, db
    config = ConfigParser.RawConfigParser()
    try:
        config.read("sitehunter.ini")
    except:
        print>>sys.stderr, 'not found config file'
        raise SystemExit

    try:
        data["ground_type"] = config.get("sitehunter", "ground_type")
        data["ground_index"] = config.get("sitehunter", "ground_index")

        db["host"] = config.get("database", "host")
        db["id"] = config.get("database", "id")
        db["pw"] = config.get("database", "pw")
        db["database"] = config.get("database", "database")

    except ConfigParser.Error, e:
        print>>sys.stderr, e.message
        raise SystemExit


def get_ground_type():
    return data["ground_type"]

def get_ground_index():
    return data["ground_index"]

def get_database_info():
    return db