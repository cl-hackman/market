from click import password_option
from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin #for line 61 flask_login doc (in link)
#mainly for the classes(UserMixin&AnonymousUserMixin) and properties; is_active,is_authenticated,is_anonymous as mentioned in the doc (link)

# for the database storage:
class Item(db.Model): # Item() is the table, db.model let's python know that am creating a class that SQLalchemy will translate into a database table on line
    id = db.Column(db.Integer(), primary_key=True)  # if primary_key = False, it will be a reference key
    name = db.Column(db.String(length=40), nullable=False, unique=True)# a method creating a string column (for table schema sake) that accepts into the database names of max 25 characters, rejects items with no names(nullable=F), and rejects duplicate names (unique) 
    price = db.Column(db.Float(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=200), nullable=False, unique=True)
    # since I am relating this table to the User model, I need to add a Foreign key column that will reference the primary key in the User model
    owner = db.Column(db.Integer(), db.ForeignKey('user.id')) # db.ForeignKey('user.id') refrences the primary_key id in the User model ('user.id')
# now that we have created the db, we need to let flask know that this is a sqlite db by congiguring the Flask(__name__)

    def buy_item(self, user):
        self.owner = user.id # remember line 15 in models.py
        user.budget -= self.price #to deduct user's budget after each item purchase
        db.session.commit()

# To create the sqlite database file
'''
First change cmd prompt to python shell by typing python in the cmd terminal ( we do this so we can import the database info in this file)
Second, from this file import the variable with the SQLAlchemy(app) (so we can run the following commands)
Type db.create_all() (this will create an empty database file)
Now, import the db.model(which will become a table in this db file): from file import class (here, we have Item as the only class)
Now, create varaiables to add rows of items to the fields that you set in the Item class object
Then add the table configs to the db file by typing: db.session.add(variable name) 
Then, finalize the addition to the db file/session type: db.session.commit()
To check the number of items (variables) in the Item table type: Item.query.all()
Then, type exit() to end
'''

# Now, am creating a database table (model) that will have info about the users' usernames and passwords
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=15), nullable=False, unique=True) # nullable=F table schema means the field shouldn't be empty
    email_address = db.Column(db.String(length=20), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False) # I set length to 60 bc it's a flask requirement for the hashing algorithm that will be applied l8r to encrypt this column
    budget = db.Column(db.Integer(), nullable=False, default=1000) # am setting the default money for users to be 1000
    #now, I want to make sure that the users are linked to the items they own in the Items model. I will create a  relational db that won't be stored as a field
    items = db.relationship('Item', backref='owned_user', lazy=True) # 'item' since I am relating it to the Item model, backref's 'owned.user' will return the user that owns the item, lazy is an SQLAlchemy arg that will let sqlalchemy run this as a relational db

    #making my budget coins (on nav bar in base html line 35) get formatted with commas as decimal places increases
    @property 
    def pretty_budget(self):
        if len(str(self.budget)) >= 4: # if budget has more than 4 decimal places:
            return f"${self.budget:.2f}"
            # the line below is giving me problems so I stick to the above code for now
            # return f"${str(self.budget)[:-3]},{str(self.budget)[-3:]}" # will return 1000 as 1,000 pay attention to the [:-3] and [-3:] 
        else:
            return f"${self.budget}"

    #Creating hash (encrypted) passwords

    @property   #class function getter used to get, set, or del an attribute value in this case, to GET specific input from the user 
    def password(self):
        return self.password    #return it back if user asks or I search for the password

    @password.setter    #am setting the returned passowrd in the function above to a bcrypt generated encryption which is then decode into standard english (utf-8)
    def password(self, plain_text_password):  #take the user entered password  
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') # override its storage as a hash password instead of the unhashed one
    #still on the User model:
    # REMEMBER TO CHECK ON THE BCRYPT SECTION: passwords aren't hashing in the database.
    '''
    from the bcrypt functionality:
    to check if the hashed passwords match the entered password on the login page, use function below since passwords are hashed'''
    def check_password_correction(self,attempted_password):   #creating a func that will check if DB password is same as the entered password 
        return bcrypt.check_password_hash(
            self.password_hash,attempted_password
            )

    def allowed_to_purchase(self, item_obj): # used in routes.py line 42 to let users purchase on the boolean condition below
        return self.budget >= item_obj.price

# link to know this part: https://flask-login.readthedocs.io/en/latest/#how-it-works
@login_manager.user_loader  #for flask to seperate the differing user sessions by refreshing
def load_user(user_id):
    return User.query.get(int(user_id))   #converting to integer not unicode as recom'ded in doc bc of how others hv been returned

# flask requirement: is inherited in line 32
class UserMixin():
    """
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    """

    # Python 3 implicitly set __hash__ to None if we override __eq__
    # We set it back to its default implementation
    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class AnonymousUserMixin:
    """
    This is the default object for representing an anonymous user.
    """

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return

