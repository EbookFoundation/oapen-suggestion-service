#!/usr/bin/python
import os


def config():
    db_env_params = {
        "POSTGRES_HOST": "host",
        "POSTGRES_PORT": "port",
        "POSTGRES_DB_NAME": "dbname",
        "POSTGRES_USERNAME": "user",
        "POSTGRES_PASSWORD": "password",
        "POSTGRES_SSLMODE": "sslmode"
    }

    db_params = {}
    for env_var, db_param in db_env_params.items():
        if env_var in os.environ:
            db_params[db_param] = os.environ[env_var]
        else:
            raise Exception(
                "Environment variable {} was not found. Please specify it in the .env file.".format(
                    env_var
                )
            )

    return db_params
