from tactical_server import create_app
import os  


basdir = os.path.abspath(os.path.dirname(__file__))
db_uri = 'sqlite:///' + os.path.join(basdir, 'data.sqlite')

app = create_app(db_uri)

if __name__ == "__main__":
    app.run(debug=True)

