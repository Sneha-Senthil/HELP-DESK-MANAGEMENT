#  Imports
from helpdesk.modules.ADTS import LinkedList 
import datetime

# for timezone()
import pytz


# class User, Agent, Ticket are used to maintain the state of
# the system and improve functionality.


class Ticket:
    """
    Ticket class describes the data of a ticket and provides method for
    retrieving, updating, etc..

    Atrributes  : _ticket_no, _booking_date, _category, _status, _issue

    Methods     : __init__, view_status, update_status, get_ticket_no,
    get_attributes, get_priority, can_raise_priority, get_category,
    get_raised
    """
    __slots__ = ["_ticket_no", "_booking_date", "_category", "_status",
                  "_issue", "_priority", "_raised", "_room_no",
                    "_booking_time", "_last_raise_hrs"]
    TOTAL_TICKETS = 0
    TIME_DIFF = 2 # in hrs, 0.01666667 hrs = 1 min
    STARTING_TICKET_NO = 134587


    def __init__(self, category=None, issue=None, room_no=None, tup = ()):
        """
        The constructor of ticket class intializes the Atrributes.

        category    : The type of category in which the issue falls under (str)
        issue       : Description of the problem in detail (str)
        room_no     : str representing room number
        tup         : it consists of all the data of attributes (tuple)[optional]

        return      : None
        """
        Ticket.TOTAL_TICKETS += 1
        
        # If the data are giving in tuple
        if tup != ():
            self._ticket_no      = int(tup[0])
            self._booking_date   = tup[1]
            self._priority       = float(tup[2])
            self._category       = tup[3]
            self._status         = tup[4]
            self._issue          = tup[5]
            self._raised         = float(tup[6])
            self._room_no        = tup[7]
            self._booking_time   = tup[8]
            self._last_raise_hrs = float(tup[9])

        # Creating a new object
        else:
            self._category      = category
            self._issue         = issue
            self._status        = "Yet to be viewed"
            self._room_no       = room_no
            # Assigning a valid ticket no according to the existing tickets
            if Ticket.TOTAL_TICKETS == 0:
                self._ticket_no = Ticket.STARTING_TICKET_NO
            else:
                self._ticket_no = Ticket.STARTING_TICKET_NO + Ticket.TOTAL_TICKETS
            date, time = current_time()
            hrs1 = hrs(date, time)
            # reversing the priority, cuz early booked ticket has less hrs
            priority = 8800 - hrs1    # 8784 hrs = 366x24 hrs in yr
            self._priority      = priority
            self._raised        = 0.0
            self._booking_date  = date
            self._booking_time   = time
            self._last_raise_hrs = hrs(date, time)


    def update_status(self, status):
        """
        To update the status of the ticket

        return : None
        """
        self._status = status
        

    def get_status(self):
        """
        This method returns the status of the ticket

        return : status of the ticket
        """
        return self._status


    def get_ticket_no(self):
        """
        To return the ticket no of the ticket object

        return : ticket no (int)
        """
        return self._ticket_no


    def get_attributes(self):
            """
            This method returns the attributes of the object for writing

            return : tuple of objects
            """
            return (self._ticket_no, self._booking_date, self._priority,
                    self._category, self._status, self._issue, self._raised,
                    self._room_no, self._booking_time, self._last_raise_hrs)


    def get_priority(self)->float:
        """returns the priority"""
        return self._priority


    def get_category(self)->str:
        """returns the category of the ticket"""
        return self._category


    def get_raised(self)->float:
        """returns the priority"""
        return self._raised


    def can_raise_priority(self)->bool:
        """raises and returns bool value if priority
        can be raised"""
        booking_hrs = hrs(self._booking_date, self._booking_time)
        date, time = current_time()
        curr_hrs = hrs(date, time)
        diff = curr_hrs - self._last_raise_hrs
        if diff >= Ticket.TIME_DIFF*(self._raised +1):
            self._raised += 1
            self._last_raise_hrs = curr_hrs
            return True
        return False


class User:
    """
    User class describes the access methods and stores the data of 
    the user

    Attributes  : _user_name, _password, _gmail,_mobile_no, _ticket_no_lst

    Methods     : __init__, validate_credentials, validate_ticket_no, 
    get_attributes, get_username, get_mobile_no, get_mail, add_ticket_no,
    get_tnl
    """
    __slots__ = ["_user_name", "_password", "_gmail", "_mobile_no",
                  "_ticket_no_lst"]


    def __init__(self, user_name = None, password = None,
                  gmail = None, mobile_no=None, tup = ()):
        """
        The constructor of user class. It intializes the attributes 
        of user class.

        user_name       : name of the user (str)
        password        : password of the user (str)
        gmail           : gmail of the user (str)
        mobile_no       : mobile number of the user
        tup             : it consists of all the data of attributes
          (tuple)[optional]

        return          : None
        """
        # If the data are giving in tuple (ie storing all old 
        # objects fronm csv)
        if tup != ():
            self._user_name     = tup[0]
            self._password      = tup[1]
            self._gmail         = tup[2]
            self._mobile_no     = tup[3]
            self._ticket_no_lst = LinkedList()
            for ticket_no in tup[4]:
                self._ticket_no_lst.append(int(ticket_no))

        # Creating a new object
        else:
            self._user_name     = user_name
            self._password      = password
            self._gmail         = gmail
            self._mobile_no     = mobile_no
            self._ticket_no_lst = LinkedList()


    def validate_credentials(self, user_mail, password):
        """
        To validate credentials which are passed as arguments

        user_mail   : name of the user or mail id
        password    : paswword

        return      : True or False (bool) 
        """
        return ((self._user_name == user_mail or self._gmail == user_mail) 
                and self._password == password)


    def validate_ticket_no(self, ticket_no):
        """To validate if the ticket no is in the user tnl"""
        if ticket_no in self._ticket_no_lst:
            return True
        else:
            return False


    def get_attributes(self):
        """
        This method returns the attributes of the object for writing

        return : tuple of objects
        """
        return (self._user_name, self._password, self._gmail,
                self._mobile_no, self._ticket_no_lst)


    def get_username(self):
        """returns the user name"""
        return self._user_name


    def get_mobile_no(self):
        """returns user mobile no"""
        return self._mobile_no


    def get_email(self):
        """returns the gmail of the user"""
        return self._gmail


    def add_ticket_no(self, ticket_no):
        """to add the created ticket no to the user list"""
        self._ticket_no_lst.append(ticket_no)


    def get_tnl(self)->LinkedList:
        """to return ticket no list"""
        return LinkedList(self._ticket_no_lst)


def current_time()->tuple:
    """date, time, returns current time in hrs excluding the years"""
    # using now() to get current time
    current_time        = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    date  = str(current_time)[:-21]
    time = str(current_time)[11:-13]
    return date, time


def hrs(date:str, time:str)->float:
    """converts the date nd time into hrs"""
    # coverting everything into hrs
    #               month                           days
    hrs = float(date[5:7])*720 + float(date[8:])*24
    #               hrs                     minutes             seconds
    hrs += float(time[:2]) + float(time[4:5])/60 + float(time[6:])/3600
    return hrs

