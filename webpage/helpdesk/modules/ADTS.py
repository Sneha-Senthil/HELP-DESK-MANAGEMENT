# Python ADTs for facilitating and storing the data in data
# structures with the help of Linkedlist, hashtable, heap-priority queue


from collections.abc import Iterable    # imports


class Node:
    """
    Node object is used for constructing linked list

    data members : _item, _next

    class methods : __init__ 
    """
    __slots__ = ["_next", "_item"]

    def __init__(self, item = None, next = None):
        """
        Constructor of Node class

        item : any value
        next : node 

        return : None
        """
        self._next = next
        self._item = item


    def set_next(self, next):
        """
        To set the next value of the node

        next : node

        return : None
        """
        self._next = next


    def set_item(self, item):
        """
        To set the item value of the node

        item : any value

        return : None
        """
        self._item = item


    def get_next(self):
        """
        To retrun the next node

        return : node
        """
        return self._next
    
   
    def get_item(self):
            """
            To retrun the item of the node

            return : item
            """
            return self._item


class LinkedList:
    """
    Implementation of LinkedList with dummy header

    data members : _head, _end, _size

    class methods : __init__, __len__, __getitem__, __setitem__, __iter__
    find, append, insert, delete, insert_by_prev__value, delete_by_prev_val  
    """
    __slots__ = ["_head", "_end", "_size"]

    def __init__(self, arg = None):
        """
        Constructor of LinkedList ADT

        return : None
        """
        self._end = Node()
        self._head = Node(next = self._end)
        self._size = 0

        # Copy constructor
        if arg != None:
            assert(isinstance(arg, Iterable)), """An iterable object can alone
            be converted in linked list"""
            for i in arg:
                self.append(i)


    def __len__(self):
        """
        special function that returns length of the list

        return : length
        """
        return self._size
    

    def __getitem__(self, pos):
        """
        To get the item of node given by pos

        pos     : a node in the list

        return  : item
        """
        # validation of pos
        assert(isinstance(pos, Node)), """pos must 
        be a Node"""
        return pos.get_item()


    def __setitem__(self, pos, item):
        """
        This method sets the item at a given pos

        item    : any value
        pos     : a node in the list

        return  : None
        """
        # validation of pos
        assert(isinstance(pos, Node)), """pos must 
        be a Node"""
        temp = self._head.get_next()
        while temp.get_next() is not None:
            if temp == pos:
                temp.set_item(item)
            temp = temp.get_next()
        if self._end == pos:
            self._end.set_item(item)


    def __iter__(self):
        """
        Iterator of linked list

        yields : current element of linked list
        """
        pos = self._head.get_next()
        for count in range(len(self)):
            yield pos.get_item()
            pos = pos.get_next()


    def __repr__(self):
        """
        This method displays the linkedlist

        return : None 
        """
        # If list is empty
        if self._size == 0:
            return "[]"
        else:
            lst_str = '['
            for i in self:
                lst_str += f"{i}, "
            return lst_str[:-2] + "]"


    def is_empty(self):
        """
        returns if the list is empty or not

        return : True or False
        """
        return self._size == 0


    def find(self, item):
        """
        This method returns the node of the given item

        item : a value in linked list

        return : pos(node)
        """
        pos = self._head.get_next()
        while pos.get_next() is not None:
            if pos.get_item() == item:
                return pos
            pos = pos.get_next()
        if self._end.get_item() == item:
            return self._end
        return None


    def append(self, item):
        """
        To add the item at last of the linked list

        item    : any value

        return : None
        """
        if self.is_empty():
            self._end.set_item(item)
        else:
            new_node = Node(item)
            self._end.set_next(new_node)
            self._end = new_node
        self._size += 1


    def insert(self, item, pos = None):
        """
        To insert a item at given pos.
        if pos = None, then item is insertesd at head

        item    : any value
        pos     : node or None

        return  : None
        """
        # validation of pos
        assert(isinstance(pos, Node) or pos == None), """pos must 
        be a Node or None"""
        # To insert at end in the list is empty
        if self.is_empty():
            self.append(item)
        # To insert at head if pos is None
        elif pos is None:
            self._head.set_next(Node(item, self._head.get_next()))
        else:
            temp = self._head
            while temp.get_next() is not None:
                if temp.get_next() == pos:
                    temp.set_next(Node(item, pos))
                    break
                temp = temp.get_next()
        self._size += 1


    def delete(self, pos):
        """
        To delete the item at a given pos

        pos     : Node or None

        return  : None
        """
        # validation of pos
        assert(isinstance(pos, Node) or pos == None), """pos must 
        be a Node or None"""

        # If empty list throw an error
        assert(not(self.is_empty())), "The list is empty!"
        # If pos is None do nothing
        if pos is None:
            return 
        temp = self._head
        while temp.get_next() is not None:
            if temp.get_next() == pos:
                temp.set_next(temp.get_next().get_next())
                break 
            temp = temp.get_next()
        self._size -= 1


    def insert_by_prev_val(self , val, item):
        """
        This function inserts the item after the val

        val     : a value in the list
        item    : item to be inserted after val

        return  : None
        """
        pos = self._head
        while pos.get_next() is not None:
            if pos.get_item() == val:
                pos.set_next(Node(item, pos.get_next()))
                break
            pos = pos.get_next()
            # ie appending after the last element
        if self._end.get_item() == val:
            self.append(item)
        self._size += 1
        

    def delete_by_prev_val(self, val):
        """
        To delete an item after given value

        val     : any value in the given list

        return  : None
        """
         # If empty list throw an error
        assert(not(self.is_empty())), "The list is empty!"

        temp = self._head
        while temp.get_next() is not None:
            if temp.get_item() == val:
                temp.set_next(temp.get_next().get_next())
                break
            temp = temp.get_next()
        self._size -= 1


class Item:
    """
    Properties of base items that a PQueue object should have
    is defined here

    attributes  : _item, _p_val

    methods     : __init__, __gt__
    """
    __slots__ = ['_item', '_p_val_1', '_p_val_2']
    
    def __init__(self, item, p_val_1 = 0, p_val_2 = 0):
        """item refers to the data, p_val_1, p_val_2 refers to the priority"""
        if isinstance(item, Item):      # copy constructor
            self._item  = item._item
            self._p_val_1 = item._p_val_1
            self._p_val_1 = item._p_val_2
        else: 
            self._item  = item
            self._p_val_1 = p_val_1
            self._p_val_2 = p_val_2


    def __gt__(self, other)->bool:
        """to compare if self is greater than other"""
        if self._p_val_1 == other._p_val_1:
            return self._p_val_2 > other._p_val_2
        return self._p_val_1 > other._p_val_1


    def copy(self):
        """To return a copy of the item details"""
        return Item(self._item, self._p_val_1, self._p_val_2)


class Max_Heap_PQueue(Item):
    """
    This is the implementation of priority queue based
    heap ADT using python list as wrapper.

    attributes          : _data

    pubplic methods     : 
    protected methods   : 
    """
    __slots__ = ['_data']
    # -----------------------protected behaviors---------------------
    def _parent(self, i:int)->int:
        """returns the parent index of 'i' th index"""
        return (i-1)//2
    

    def _left(self, i:int)->int:
        """returns the left child index of 'i' th index"""
        return 2*i + 1


    def _right(self, i:int)->int:
        """returns the right child index of 'i' th index"""
        return 2*i + 2
    

    def _has_left(self, i:int)->bool:
        """checks if left child is present to the index i"""
        return self._left(i) < len(self._data)
    

    def _has_right(self, i:int)->bool:
        """checks if left child is present to the index i"""
        return self._right(i) < len(self._data)
    

    def _swap(self, i:int, j:int):
        """To swap the items at the indices i and j"""
        self._data[i], self._data[j] = self._data[j], self._data[i]
    

    def _up_heap(self, i:int):
        """To up heap the item at i'th index"""
        parent = self._parent(i)
        # if i is 0 then it has no parent, so its an exception
        while self._data[parent] < self._data[i] and i > 0:
            self._swap(parent, i)
            i = parent
            parent = self._parent(i)


    def _down_heap(self, i:int):
        """To down heap the index at i'th index"""
        if self._has_left(i):                       # base case
            large_child_index = self._left(i)
            if self._has_right(i):
                if (self._data[self._right(i)] >
                    self._data[large_child_index]):
                    large_child_index = self._right(i)
            if self._data[large_child_index] > self._data[i]:
                self._swap(large_child_index, i)
                self._down_heap(large_child_index)  # recursive call
    
    # -----------------------public behaviors------------------------
    def __init__(self, arg=None):
        """constructor of PQueue"""
        if isinstance(arg, Max_Heap_PQueue):  # self copy constructor
            self._data = []
            for tup in arg:
                self._data.append(Item(tup[0], tup[1]), tup[2])
        elif isinstance(arg, Iterable):       # copy constructor
            self._data = []
            for seq in arg:
                assert((isinstance(seq, Iterable)
                       and len(seq) == 3) and 
                       isinstance(seq[1], (float, int))), "Unexpected iterable format"
                self.add(seq[0], seq[1], seq[2])
        else:
            self._data = []


    def __len__(self)->int:
        """returns the size of the PQueue"""
        return len(self._data)
    

    def is_empty(self)->bool:
        """returns if the queue is empty or not"""
        return len(self._data) == 0


    def __iter__(self)->tuple:
        """iterator for PQueue class"""
        for obj in self._data:
            yield (obj._item, obj._p_val_1, obj._p_val_2)
    

    def add(self, item:any, p_val_1:float=0, p_val_2:float=0):
        """To add a new item, p_val pair to PQueue"""
        self._data.append(Item(item, p_val_1, p_val_2))
        self._up_heap(len(self._data)-1)        # up heaping the new pair


    def max(self)->tuple:
        """To return the highest priority item, p_val pair"""
        assert not self.is_empty(), "The Priority queue is empty"
        max_item = self._data[0]
        return (max_item._item, max_item._p_val_1, max_item._p_val_2)
    

    def pop(self)->tuple:
        """To remove and return the highest priority item, p_val pair
        from the PQueue"""
        assert not self.is_empty(), "The Priority queue is empty"
        self._swap(0, len(self._data)-1) # put minimum item at the end
        max_item = self._data.pop()
        self._down_heap(0)               # down heaping the item at root
        return (max_item._item, max_item._p_val_1, max_item._p_val_2)
    

    def raise_priority(self, item:any, p_val:float=1.0):
        """To raise the prority of an item by p_val and then up heap it"""
        assert(isinstance(p_val, (float, int))), "p_val must be a float or int"
        for i, item_obj in enumerate(self._data):
            if item_obj._item == item:     # checking if the item is in the list
                item_obj._p_val_1 += p_val # raising its priority by p_val
                # up heaping the item to hold the structure
                self._up_heap(i)         
                break


    def __repr__(self)->tuple:
        """To print the pqueue in items with highest priority
        as first element and others not in order"""
        if self.is_empty():
            return '[]'
        Pqueue_str = '['
        for tup in self:
            Pqueue_str += f"{tup}, "
        return Pqueue_str[:-2] + ']'


    def copy(self):
        """copies the priority queue and returns a new object"""
        pqueue = Max_Heap_PQueue()
        for item in self._data:
            pqueue._data.append(Item(item))
        return pqueue


class hashTable():
    """Hash table ADT is used for doing the operations in less time
    
    Attributes : hashTable
    
    methods    : __init__, __setitem__, __getitem__, update, delete,
    __repr__, keys, values, items, __iter__"""
    __slots__ = ["hashTable"]

    def __init__(self, capacity):
        """constructor of hashtable"""
        self.hashTable = [[] for i in range(capacity)]


    def hashFunc(self,key):
        """hashFunc generates a key"""
        sum = 0
        for char in key:
            sum = sum + ord(char)
        index = sum % 10
        return index


    def __setitem__(self, key, value):
        """sets a key to the given value"""
        index = self.hashFunc(str(key))
        lis = self.hashTable[index]
        for i in range(len(lis)):
            if lis[i][0] == key:
                lis[i] = (key, value)
                return
        self.hashTable[index].append((key,value))
        return


    def __getitem__(self, key):
        """returns the value of the given key"""
        index = self.hashFunc(str(key))
        if len(self.hashTable[index]) == 0:
            print("KEY ERROR")
            return
        
        for lis in self.hashTable[index]:
            if lis[0] == key:
                return lis[-1]


    def update(self, key, value):
        """updates the key value pair"""
        index = self.hashFunc(key)
        lis = self.hashTable[index]
        length = len(lis)
        for i in range(length):
            if lis[i][0] == key:
                lis[i] = (key,value)
    

    def delete(self, key):
        """deletes the specified key along with the value"""
        index = self.hashFunc(key)
        if len(self.hashTable) == 0:
            print("KEY ERROR")
            return
        
        lis = self.hashTable[index]
        length = len(self.hashTable[index])
        for i in range(length):
            if lis[i][0] == key:
                lis.pop(i)


    def __repr__(self):
        """returns a str of hash table"""
        content = ""
        for lis in self.hashTable:
            if len(lis) == 0:
                continue
            elif len(lis) == 1:
                content += str(lis[0][0]) + " : " + str(lis[0][-1]) + " , "
            else:
               for chain in lis:
                   content +=str(chain[0]) + " : " + str(chain[-1]) + " , "
        return "{" + content.strip(" , ") + "}"
   

    def keys(self):
        """returns the list of keys"""
        result = []
        for lis in self.hashTable:
            if len(lis) == 0:
                continue
            
            elif len(lis) == 1:
                result.append(lis[0][0])
                
            else:
                for chain in lis:
                    result.append(chain[0])
        return result
    

    def values(self):
        """returns the list of values"""
        result = []
        for lis in self.hashTable:
            if len(lis) == 0:
                continue
            
            elif len(lis) == 1:
                result.append(lis[0][-1])
                
            else:
                for chain in lis:
                    result.append(chain[-1])
        return result
    

    def items(self):
        """returns the key, value pair items"""
        result = []
        for lis in self.hashTable:
            if len(lis) == 0:
                continue
            
            elif len(lis) == 1:
                result.append(lis[0])
                
            else:
                for chain in lis:
                    result.append(chain)
        return result
    
    
    def __iter__(self):
        """iterator for hash function"""
        for key in self.keys():
            yield key
        return
    
