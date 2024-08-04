from django.shortcuts import render
from django.http import HttpResponse
from helpdesk.modules.Functionalities import *
from helpdesk.modules.ADTS import LinkedList

# Create your views here.

# data stored here
# Global variabals to maintain states
USER_OBJECTS_LST    = []
TICKET_OBJECTS_LST  = []
USER                = None
LOGGED_IN           = False
CURRENT_HEAP        = None
CURRENT_TICKET_NO   = None
Elec_agent  = hashTable(10)
Furn_agent  = hashTable(10)
Plumb_agent = hashTable(10)
heap        = hashTable(10)
# loading the data from csv files
USER_OBJECTS_LST    = objs_lst_reader(
            ".\\helpdesk\\CSV_Files\\user_objs.csv", User,
            ".\\helpdesk\\CSV_Files\\user_tnl.csv")
TICKET_OBJECTS_LST  = objs_lst_reader(
        ".\\helpdesk\\CSV_Files\\ticket_objs.csv", Ticket)
# creating hash tables to store agent details
# electrical category
heap_tuple = heap_reader(".\\helpdesk\\CSV_Files\\agent_tnl.csv",
                          TICKET_OBJECTS_LST)
Elec_agent['agent_name']   = 'elec#agent'
Elec_agent['mail']         = 'elecagent@gmail.com'
Elec_agent['password']     = 'elec#agent'
heap['Electrical']         = heap_tuple[0]
# furniture category
Furn_agent['agent_name']   = 'furn#agent'
Furn_agent['mail']         = 'furnagent@gmail.com'
Furn_agent['password']     = 'furn#agent'
heap['Furniture']          = heap_tuple[1]
# plumbing category
Plumb_agent['agent_name']  = 'plumb#agent'
Plumb_agent['mail']        = 'plumbagent@gmail.com'
Plumb_agent['password']    = 'plumb#agent'
heap['Plumbing']           = heap_tuple[2]


def home(request):
    """Home page html function"""
    # make suring every global state variable is None or False at home
    global LOGGED_IN, USER, LOGGED_IN, CURRENT_HEAP
    global CURRENT_TICKET_NO
    LOGGED_IN = False
    USER = None
    CURRENT_HEAP = None
    CURRENT_TICKET_NO = None
    return render(request, 'home.html')


def log_in(request):
    global USER, LOGGED_IN
    # if request came from home page 
    if request.method == 'POST':
        email_user  = request.POST['email_user']
        password    = request.POST['password']
        # validating password
        validated, USER = validate_credentials(email_user, password, USER_OBJECTS_LST)
        print(f"email \t: {email_user}\npassword \t: {password}\nvalidated \t: {validated}")
        if not validated:
            return render(request, 'log-in.html', {'error': True})
        LOGGED_IN = True
        request.method = 'GET'
        # calling user html
        return user_tickets(request)
    # if request came from home page page
    LOGGED_IN = False
    return render(request, 'log-in.html')


def create_ticket(request):
    global TICKET_OBJECTS_LST, USER
    if request.method == 'POST':
        issue    = request.POST['description']
        category = request.POST['issue-category']
        room_no  = request.POST['room-no']
        ticket = Ticket(category, issue, room_no)
        TICKET_OBJECTS_LST.append(ticket)
        print("details\n")
        USER.add_ticket_no(ticket.get_ticket_no())
        heap[category].add(ticket, ticket.get_raised(),
                            ticket.get_priority())
        writer()    # to write the created data
        request.method = 'GET'
        return user_tickets(request) 
    print("in")
    return render(request,'create-ticket.html', 
        {'user_name':USER.get_username(), 'mail':USER.get_email()})


def agent_log_in(request):
    global LOGGED_IN, CURRENT_HEAP
    LOGGED_IN = False
    # To check if its a valid agent credentials
    if request.method == 'POST':
        email_name = request.POST['email-name']
        password   = request.POST['password']

        if ((Elec_agent['agent_name'] == email_name or
            Elec_agent['mail'] == email_name ) 
            and Elec_agent['password'] == password):
            CURRENT_HEAP = heap['Electrical']
            LOGGED_IN = True

        elif ((Furn_agent['agent_name'] == email_name or
            Furn_agent['mail'] == email_name ) 
            and Furn_agent['password'] == password):
            CURRENT_HEAP = heap['Furniture']
            LOGGED_IN = True

        elif ((Plumb_agent['agent_name'] == email_name or
            Plumb_agent['mail'] == email_name ) 
            and Plumb_agent['password'] == password):
            CURRENT_HEAP = heap['Plumbing']
            LOGGED_IN = True

        if LOGGED_IN:
            request.method = 'GET'
            return agent_tickets(request)
        # if invalid credentials
        return render(request, 'agent-log-in.html', {'error':True})
    
    return render(request, 'agent-log-in.html')


def sign_up(request):
    if request.method == 'POST':
        pass
    return render(request, 'sign-up.html')


def check_ticket_status(request):
    global LOGGED_IN, CURRENT_TICKET_NO
    # if the reuest came from the check ticket status page
    if request.method == 'POST':
        ticket_no = int(request.POST['ticket-no'])
        user_mail = request.POST['email-user'] 
        for user in USER_OBJECTS_LST:
            if (user_mail == user.get_username() 
            or user_mail == user.get_email()):
                if user.validate_ticket_no(ticket_no):
                    # making sure user is not logged in
                    LOGGED_IN = False
                    # assigning ticket no to the global
                    CURRENT_TICKET_NO = ticket_no
                    request.method = 'GET'
                    return ticket_details(request)
        # invalid details
        return render(request, 'check-ticket-status.html', {'error':True})
    # request came from home page
    return render(request, 'check-ticket-status.html')


def ticket_details(request):
    for ticket in TICKET_OBJECTS_LST:
        if ticket.get_ticket_no() == CURRENT_TICKET_NO:
            attr_tup = ticket.get_attributes()
    # returning the ticket details 
    return render(request, 'ticket-details.html',
                   {'tup':attr_tup})    


def user_tickets(request):
    print(LOGGED_IN)
    # to display the prompt message
    prompt = ''
    if request.method == 'POST':
        ticket_no = int(request.POST['ticket-no'])
        print(ticket_no)
        if ticket_no == "Ticket No":
            # if not selected the page is reload
            pass
        else:
            for ticket_obj in TICKET_OBJECTS_LST:
                if ticket_no == ticket_obj.get_ticket_no():
                    # checking if the ticket priority can be raised
                    if ticket_obj.can_raise_priority():
                        print("yes increased priority")
                        print(f"{ticket_no}")
                        crr_heap = heap[ticket_obj.get_category()]
                        # special method in heap dsa is called
                        crr_heap.raise_priority(ticket_obj)
                        writer() # saving the changes
                        prompt = (f"The ticket no {ticket_no}" +
                                  " has been successfully raised")
                    else:
                        prompt = (f"The ticket can't be " + 
                        f"raised again within {Ticket.TIME_DIFF} hours")
                    break

    if LOGGED_IN:
        # getting user tnl info
        tnl = USER.get_tnl()
        print(tnl)
        ticket_obj_attr_lst = LinkedList()
        for ticket_no in tnl:
            for obj in TICKET_OBJECTS_LST:
                if ticket_no == obj.get_ticket_no():
                    # creating a Linkedlist to pass it to the html page
                    ticket_obj_attr_lst.append(obj.get_attributes())
        print("inside")
        return render(request, 'user-tickets.html',
                       {'obj_lst':ticket_obj_attr_lst, 'prompt':prompt})


def agent_tickets(request):
    # if the request comes form agent log in page
    if request.method == "POST":
        status = request.POST['status']
        print(status)
        # current heap is a global variable 
        max_tup = CURRENT_HEAP.max()
        max_tup[0].update_status(status)
        if status == 'Closed':
            CURRENT_HEAP.pop()
        writer() # to save the changes
        request.method = 'GET'
        return agent_tickets(request)

    if LOGGED_IN:
        ticket_tup_lst = []
        for tup in CURRENT_HEAP:
            attr_tup = tup[0].get_attributes()
            for user in USER_OBJECTS_LST:
                # checking if ticket no is in the user tnl list
                if attr_tup[0] in user.get_tnl():   
                    attr_tup += (user.get_username(),
                                  user.get_mobile_no())
            ticket_tup_lst.append(attr_tup)
        return render(request, 'agent-ticket-details.html',
                     {'max':ticket_tup_lst[0],'ticlst':ticket_tup_lst[1:]})


def help_support(request):
    """rendering the help support page"""
    return render(request, 'help-support.html')


# writer to write the objects back as soon as created
def writer():
    """This function writes the data into csv files back"""
    global USER_OBJECTS_LST, TICKET_OBJECTS_LST
    global heap
    objs_lst_writer(".\\helpdesk\\CSV_Files\\user_objs.csv",
     USER_OBJECTS_LST, ".\\helpdesk\\CSV_Files\\user_tnl.csv")
    objs_lst_writer(".\\helpdesk\\CSV_Files\\ticket_objs.csv",
     TICKET_OBJECTS_LST )
    heap_writer(".\\helpdesk\\CSV_Files\\agent_tnl.csv", 
                (heap['Electrical'], heap['Furniture'], heap['Plumbing']))
    
