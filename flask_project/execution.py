from market import app

# to check if this file has executed without importing from the package file (__init__)
if __name__ == '__main__': 
    app.run(debug=True) # To run the app, (debug=True) skips all the setup envs (set FLASK_APP=file.py, set FLASK_DEBUG=1, flask run)