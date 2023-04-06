from flask_app import app 
from flask_app.controllers import flavors, users, ice_cream_shops

if __name__=="__main__":
    app.run(debug=True)