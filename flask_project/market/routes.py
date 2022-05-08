from market import app
from flask import render_template, redirect, url_for, flash, request    # redirect use is on line 79 in register_page() route. flask's request module lets me manipulate the GET and POST requests
from market.models import Item, User   # reason for market.models is bc models is not in the __init__ file
from market.forms import PurchaseItemForm, RegisterForm, LoginForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user # current_user to let me assign purchased item to user line 41

# this decorator lets flask connect the URL ('/home') to the response(function)
@app.route('/')
@app.route('/home')
def homepage():
    # what you put here will be displayed on this page(the function is called a ROUTE in flask terms)
    return render_template("homepage_tags.html")


'''NOTE: By convention, Flask prefers that you don't include the html tags (<h1></h1>) in the routes but rather creater a separate folder to put 
the html templates in it then you can refer the routes to the tags in the templates folder.
For this connection to work, import another module called "render_template"
NOTE: By convention again, you have to name the folder templates so the flask package knows that there're html tags in it.
NOTE: you create a a html file for every new route you make'''

# this was before I created the execution.py
''' NOTE: To run this application for develpoment:
* Open Command Prompt
* Type set FLASK_APP=ypur_filename_here.py
* Type flask run
you will then get the URL for your app
NOTE:To let the app refresh itself whenever updates are made to the file (market.py):
* Type set FLASK_DEBUG=1    (this is because the Debug mode is set to off when you first type flask run)
NOTE: 
DO NOT TURN THE DEBUG MODE ON WHEN YOU FINSIH BUILDING THE APP FOR PRODUCTION BC IT WOULD BREED ERRORS'''


@app.route('/market', methods=['GET', 'POST'])
@login_required #to take user to login page after they click Begin! button
def market_page():
    purchase_form = PurchaseItemForm() # for buttons_modals purchase confirmation in forms.py class PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST': # so I don't get a submission info anytime I restart the page
        purchased_item = request.form.get('purchased_item') # request module will let me get the value of the purchased item
        p_item_object = Item.query.filter_by(name=purchased_item).first() #to filter by item's value
        if p_item_object: #to assign purchased item to user
            if current_user.allowed_to_purchase(p_item_object): #line 68 in models.py so user cannot buy if budget is less than price
                p_item_object.buy_item(current_user) #code is in class Item's method line 18 
                flash(f'Congratulations on purchasing {p_item_object.name} at ${p_item_object.price}', category='success')
            else:
                flash(f'Unfortunaly, budget is insufficient to purchase {p_item_object.name}', category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.allowed_to_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations on your sale of {s_item_object.name}", category='success')
            else:
                flash(f"Unfortunately, item sale couldn't execute {s_item_object.name}", category='danger')
                
        return redirect(url_for('market_page')) #to go back to market page after purchase (POST request) is made
    # to put more stuff on the market page, add them here as a list of dictionairies and in the render_template, add a variable=variable argl
    '''items = [
        {'name': 'Rolex Oyster Perpetual', 'barcode': '683498487890', 'price': 7450},
        {'name': 'iPhone', 'barcode': '893212299897', 'price': 500},
        {'name': 'HP Laptop', 'barcode': '123985473165', 'price': 900},
        {'name': 'ZL Keyboard', 'barcode': '231985128446', 'price': 150}
    ]'''
    # But now that the sqlite file has been created, just link this page to the db file by querying all the observations in the table of choice (Item)
    if request.method == 'GET': # to stop the resubmission info after each page refresh
        items = Item.query.filter_by(owner=None) #filter_by 'owner=None' so items with no owners will be dispalyed on the available left section
        #items = Item.query.all() #I will use this if there aren't many items available otherwise, there will no be item left to display
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market_tags.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)
    # this will appear on the page as the value items so we need Boostrap & Jinja syntax to style the items on the page
    # NOTE : {% %} (only one curly bracket) for logicals like for loops, if statements,etc in Jinja syntax
    # NOTE : {{variable goes here}} (two curly brackets

    # return render_template('marketpage_tags.html', item ="Phone") previous code for 1 item
'''NOTE: to make the "Phone" appear on this page, you need to use jinja syntax which is for Flask's default jinja package.
Jinja connects the item in the route to the html design file
Place the syntax under the sentence or tag you want.'''

# creating a page for the register form so thee users can register there
# for this to work, import forms.py so this file will recognize it 
# the user_to_create will let the "create account" button go to the next page if only these fields(conditions) are filled
@app.route('/register', methods=['GET', 'POST']) #these methods let the user post info to the server and get specific fields info back
def register_page():
    form = RegisterForm() # this RegisterForm() is the regsiter form class in the forms file
    if form.validate_on_submit():   #saying if validation conditions are met, send the user info to User table in the database
        # creating the user in the User model(table in db)
        user_to_create = User(username=form.username.data,  #connecting the POST info in the form to the User() model in my db
                              email_address=form.email_address.data,  # the .data here is attached to the DataRequired line11 in forms.py
                              password=form.password1.data) # this line connects to @password setter in models.py; its sent as a plain text password in the plain_text_password paremeter
                            #there's a problem, line 76 variable is password not password_hash inorder for the bcrypt password hash to work
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)  #so user won't be taken to login page after registering due to using login_required
        flash(f'succesfully registered as {user_to_create.username}', category='success')
        return redirect(url_for('market_page')) # after everything's met, send user to market page route line 47 
        #form.errors (dictionary built) will store user entries that do not meet the validation requirements 
    if form.errors != {}: #If there are errors from valditions
        for err_msg in form.errors.values():
            flash(f'sorry, problem with entry: {err_msg}', category='danger')   
            #this is the error feedback message that the user gets. flask default error message handler is flash module. the 'danger' connects to a bootsrap tag in base.html to give the feedback red color customization
    return render_template('register_tags.html', form=form)

# login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    #now, am writing the validation to check if the username already exists
    if form.validate_on_submit(): #saying; after the user has met the requirements (in User model) as they click sign-in(submit):
        attempted_user=User.query.filter_by(username=form.username.data).first()
        #saying; check if the entered data in the field is same as in the User model {first() will grab it}
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):#this is for the hashed password section
        #after these conditions are met, login user by:
            login_user(attempted_user)
            flash(f'login successful {attempted_user.username}', category='success') #'info' to encapsulate feedback message in green
            return redirect(url_for('market_page'))
        else:
            flash('credentials do not match, please retry', category='danger') #'info' to encapsulate feedback message in red

    return render_template('login_tags.html', form=form)

# logout page
@app.route('/logout')
def logout_page():
    #using logout_user module to log out the user
    logout_user()
    flash('Logged out successfuly!', category='info') #'info' to encapsulate feedback message in blue
    return redirect(url_for('homepage')) #take user to homepage after logging out

