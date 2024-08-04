# Functionalities module contains the necessary functions for the
# Frame Work of the prototype and enchances the performance of the
# help desk system


# Imports
from helpdesk.modules.Classes import User, Ticket
from helpdesk.modules.ADTS import LinkedList, hashTable, Max_Heap_PQueue
from collections.abc import Iterable
import csv


def validate_credentials(user_mail, password, objs_lst):
    """
    This validates if a user or agent is registered
    and return the object if it exists

    user_mail   : user name or mail id
    password    : password of the account
    objs_lst    : objects of user or agent

    return      : True or False, obj
    """
    for obj in objs_lst:
        if obj.validate_credentials(user_mail, password):
            return True, obj
    return False, None


# csv reading and writing functions
def heap_reader(path:str, class_obj_lst:Iterable)->Max_Heap_PQueue:
    """reads heap dsa from csv file in the given path"""
    # converts the ticket no list into heap by retrieving the
    # data from tickets obj list
    def converter(row):
        heap = Max_Heap_PQueue()
        for ticket_no in row:
            for obj in class_obj_lst:
                if int(ticket_no) == obj.get_ticket_no():
                    heap.add(obj, obj.get_raised(), obj.get_priority())
        return heap
    # creates the 3 catagories of heap
    with open(path, 'r',newline='') as file:
        reader = csv.reader(file)
        tup = tuple(reader)
        elec_heap = converter(tup[0]) 
        furn_heap = converter(tup[1]) 
        plumb_heap = converter(tup[2])
        file.close()
    return elec_heap, furn_heap, plumb_heap


def heap_writer(path:str, heap_tup:tuple):
    """writes the heap back into the csv files"""
    lst = LinkedList()
    for heap in heap_tup:
        tnl_lst = LinkedList()
        for tup in heap:
            tnl_lst.append(tup[0].get_ticket_no())
        lst.append(tnl_lst)
    with open(path, 'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lst)


def objs_lst_reader(path:str, class_name, path_tnl:str = None)->LinkedList:
    """
    This method reads the info into the csv file

    path        : path of the csv file
    class_name  : name of the class

    return      : a list of objects of the given class
    """
    class_obj_lst = LinkedList()

    with open(path,'r') as file:
        objs_data = tuple(csv.reader(file))
        file.close()

    # To read the ticket_no list if it exists
    if path_tnl is not None:
        with open(path_tnl, 'r') as file:
            ticket_no_lst = tuple(csv.reader(file))
            file.close()
        zipped = tuple(zip(objs_data, ticket_no_lst))
        for tup in zipped:
            attribute_tup = tuple(tup[0]) + (tup[1],)
            class_obj_lst.append(class_name(tup = attribute_tup))

    # To store tickets in the ticket_object_list
    else:
        for tup in objs_data:
            print(tup)
            class_obj_lst.append(class_name(tup = tup))
    return class_obj_lst
             

def objs_lst_writer(path:str, class_obj_lst, path_tnl = None):
    """
    This method writes the info into the csv file

    path            : path of the csv file
    class_obj_lst   : a list of class objects

    return          : None
    """
    obj_file = open(path, 'w', newline='')
    obj_writer = csv.writer(obj_file)

    # To write the objects and ticket no list also
    if path_tnl is not None:
        tnl_file = open(path_tnl, 'w', newline='')
        tnl_writer = csv.writer(tnl_file)
        for obj in class_obj_lst:
            row = obj.get_attributes()
            obj_writer.writerow(row[:-1])
            tnl_writer.writerow(row[-1])
        tnl_file.close()

    # To write the objects of ticket class
    else:
        for obj in class_obj_lst:
            obj_writer.writerow(obj.get_attributes())
    obj_file.close()

