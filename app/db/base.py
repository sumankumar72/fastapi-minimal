import os
import importlib
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def import_all_models():
    model_dir = os.path.dirname(__file__)
    for module_name in os.listdir(model_dir):
        if module_name.endswith(".py") and module_name != "__init__.py":
            module_name = module_name[:-3]
            importlib.import_module(f"app.db.{module_name}")


# Here we are collecting all models defined in the db dir to migrate the db changes
import_all_models()
