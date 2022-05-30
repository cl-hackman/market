from market import application #can be app not needed

# to check if this file has executed without importing from the package file (__init__)
if __name__ == '__main__': 
    application.run('localhost',5000,debug=True) # To run the app, (debug=True) skips all the setup envs (set FLASK_APP=file.py, set FLASK_DEBUG=1, flask run)

#('localhost',5000): beanstalk needs this identifier to run it other than on the standard http PORT 80