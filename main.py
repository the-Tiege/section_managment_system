from tactical_server import create_app
import os  

if __name__ == "__main__":
    basdir = os.path.abspath(os.path.dirname(__file__))
    db_uri = 'sqlite:///' + \
    os.path.join(basdir, 'test_db.sqlite')

    app = create_app()