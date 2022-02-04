from connection import *
from datetime import date,datetime
import bcrypt
from mysql.connector import Error
import random
from tkinter import messagebox as mb

connection = db_connect()
cursor = connection.cursor()

def create_id():
    return random.randint(112122,278396)

    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
    ## ************************************************************************##
    ##       User Creation Codes and functionality Starts Here!!               ##
    ##                                                                         ##
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##

def get_keys(dictionary):
    keys = []
    for key in dictionary.keys():
        keys.append(key)
    return keys

class Store: 
    _sales_record = {}
    _rec = []
    def __init__(self,name):
        self.name = name
        self.record = self.get_record()
        self._sales_record = self._sales_record
        # self.customer = Customer()
        self.get_record()
        
    # Return details of goods in store
    def stock_quantity(self):
        return Products._stocks

    
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
    ## This is a function that converts the order_dictionary into a tuple of   ##
    ## item_name,item_prrice,total of quantity of item purchased               ##
    ## this is then used to print out the receipt of purchase                  ##
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##

    def list_items(self,order_item):
        all_items = []
        for item in order_item:
            price_result = []
            get_this_price = """
                SELECT price FROM products
                WHERE title = '%s'
                """%(item)
            cursor.execute(get_this_price)
            for pdt in cursor.fetchall():
                u,*z = pdt
                price_result.append(u)
            x = (item,order_item[item],price_result[0],order_item[item]*price_result[0])
            all_items.append(x)
        return all_items

    # a function to print out customer's order after purchase
    def get_customer_order_detail(self,customer,order_detail):
        m_record = {}
        total = 0
        customer_name = customer.firstname +' '+ customer.lastname

        ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
        ##         create a dictionary linking the date to the customer            ##
        ##    then create another dictionary linking the customer to his order     ##
        ##     using the customer name as key and the his order as the value       ##
        ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
        ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
        today = date.today()
        today= today.strftime("%b %d %Y")
        time = datetime.now()
        time = time.strftime('%H:%M:%S')
        x = {}
        record = {customer_name: self.list_items(order_detail)}
        x.update(record)
        v = {}
        v.update(x)
        m_record[today] = v
        # print('Reco: ',m_record[today])
        print('Sales Record for: ',today,time )

        ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
        ## get_keys() is a predefined function for obtaining the key of a dictionary ##
        ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##

        print('Customer\'s Name: %s ' %(get_keys(m_record[today])[0]))
        print('---'*10)
        print('{:9} {:7} {:5} {} '.format('Title','Unit','Qty','Total'))
        for detail in m_record[today][get_keys(m_record[today])[0]]:
            total += detail[3]
            print('{:10} {:d} {:>7d} {:>7d} '.format(detail[0],detail[1],detail[2],detail[3]))
        print('***' * 10)
        print('{:18} {:10d}'.format('Order Total :',total))
        print('***' * 10)
    

    def get_record(self):
        _sales_account_record = {}
        record_list = self._rec
        details = []
        for item in self._rec:
            if get_keys(item)[0] == date:
                self.details.append(item[date][0])
        _sales_account_record.update({date:details})
        return _sales_account_record
        
    # Sell a particular commodity
    def sell_item(self,customer,*items):
        if type(items) != list:
            items = list(items) 
        
        order_list = {}

          ## # # # # # # # # # # # # # # # # # # # # # # ##
          ## Convert shopping list tuples to dictionary  ##
          ## # # # # # # # # # # # # # # # # # # # # # # ##
        for products in items: 
            for item,quantity in products:
                item = item.lower()
                order_list[item] = quantity

        for item in order_list.keys():
            # stock result is in the order:- title,barcode,quantity,price
            stock_result = []
        
            get_current_quantity = """
                SELECT title,barcode,quantity FROM stock
                WHERE title = '%s'
                """%(item)
            
            get_current_price = """
                SELECT price FROM products
                WHERE title = '%s'
            """%(item)
            
            cursor.execute(get_current_quantity)
            for pdt in cursor.fetchall():
                a,b,c,*d = pdt
                stock_result.append(a)
                stock_result.append(b)
                stock_result.append(c)
            
            cursor.execute(get_current_price)
            for price in cursor.fetchall():
                x,*y = price
                stock_result.append(x)

            if item in stock_result:
                if stock_result[2] < order_list[item]:   ## Check if the requested quantity of item is greater than the available quantity
                    print('Order greater than available quantity')
                    print('Available Quantity: ',item,' ',stock_result[2])
                    raise ValueError('Cannot complete Purchase!')
                else:
                    new_qty = stock_result[2] - order_list[item]
                    barcode = stock_result[1]
                    total = stock_result[3] * order_list[item]
                    sales_date = date.today()
                    s_time = datetime.now()
                    sales_time = s_time.strftime("%H:%M:%S")
                    update_stock_sales = """
                    UPDATE stock
                    SET quantity = '%s'
                    WHERE title = '%s'
                    """%(new_qty,item)
                    update_sales_record = """
                    INSERT INTO sales_record(date,time,barcode,title,price,quantity,total)
                    VALUES(%s,%s,%s,%s,%s,%s,%s)
                    """
                    record = [(sales_date,sales_time,barcode,stock_result[0],stock_result[3],order_list[item],total)]
                    cursor.execute(update_stock_sales)
                    cursor.executemany(update_sales_record,record)
                    connection.commit()                
            else:
                raise ValueError('Item out of Stock!')
                # print(item,'is out of Stock!')

        data = []
        self.get_customer_order_detail(customer,order_list)
        mdate = date.today().strftime("%b %d %Y")
        data.append(order_list)
        s_record = {mdate:data}     ## Create a dictionary of date to order_list
        self._rec.append(s_record)  ## Add the current sales record to the record list
        details = []
        for item in self._rec:
            # print(item)                      ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
            if get_keys(item)[0] == mdate:     ## check if the key of the record stored in the record list is the same as the present date  ##
                                               ## "item[mdate][0]" references the order list * * * * * * * * * * * * * * * * * * * * * * *  ##
                details.append(item[mdate][0]) ## if yes, add that record to the details list which is to be later printed  * * * * * * * * ##
        self._sales_record.update({mdate:details})
        print('Purchase Succesfully Completed!')  
        print('Thanks For Your Patronage')
        print('Kindly Visit Next Time! \n')
        

class Products:
    _stocks = {}
    def __init__(self,product_name):
        self.title = product_name.lower()

    @classmethod
    def get_price(cls,item):
        return cls._stocks[item][1]


class User:
    def __init__(self,firstname,lastname,email,password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def __setattr__(self,name,value):
        if (name=='firstname'):
            if isinstance(value,str):
                self.__dict__['firstname'] = value.lower()
            else:
                raise TypeError('Firstname should be a string')
        elif (name=='lastname'):
            if isinstance(value,str):
                self.__dict__['lastname'] = value.lower()
            else:
                raise TypeError('Lastname should be a string')
        elif (name=='password'):
            if isinstance(value,str) or isinstance(value,int):
                self.__dict__['password'] = value.lower()
            else:
                raise TypeError('Lastname should be a string')
        elif (name=='email'):
            if isinstance(value,str):
                self.__dict__['email'] = value
            else:
                raise TypeError('Expected a string for email')

    def create_user(self):
        user_id = create_id()
        user_firstname = self.firstname
        user_lastname = self.lastname
        user_email = self.email
        user_pass = self.password.encode()
        # user_pass = user_pass
        hashed = bcrypt.hashpw(user_pass,bcrypt.gensalt(10))
        register_user_query = """
        INSERT INTO users (uid,firstname,lastname,email,password)
        VALUES(%s,%s,%s,%s,%s)
        """
        
        user_details = (user_id,user_firstname,user_lastname,user_email,hashed)
        try:
          
            cursor.execute(register_user_query,user_details)
            connection.commit()
            mb.showinfo('Information',f'Registration Successful! \n Your user Id is {user_id} kindly save it for later purposes')
        except Error as err:
            if err.errno == 1062:
                print('This email is taken, kindly enter another email address!')
            print('Something went wrong: {}'.format(err))
     

    def get_admin_id(self):
        get_id_query = """
        SELECT id FROM admin
        WHERE email = '%s'
        """ %(self.email)
        cursor.execute(get_id_query)
        for id in cursor.fetchall():
            x,*y = id
            return x    ## x here refers to the admin id

        ## # # # # # # # # # # # # # # # # # # # # # # ##
        ##   Check if admin user exists in database    ##
        ## # # # # # # # # # # # # # # # # # # # # # # ##
    def validate_admin(self):
        results = []
        check_admin = """
        SELECT email FROM admin
        WHERE email = '%s'
        """%(self.email)
        cursor.execute(check_admin)
        for id in cursor.fetchall():
            x,*y = id
            results.append(x)
        if self.email in results:
            return True
        else:
            return False
    
    def add_to_stock(self,barcode,title,quantity,price=0):
        if self.validate_admin() is True:
            title = title.lower()
            self.barcode = barcode
            self.price = price
            self.quantity = quantity
            results = []
            check_stock_query = """
            SELECT barcode FROM stock
            WHERE barcode = '%s'
            """ %(barcode)
            with connection.cursor() as cursor:
                cursor.execute(check_stock_query)
                for query in cursor.fetchall():
                    x,*y = query
                    results.append(x)
                if barcode in results: #Check if item is already in stock and update quantity if yes
                    # update the quantity
                    get_current_quantity = """
                    SELECT quantity FROM stock
                    WHERE barcode = '%s'
                    """%(barcode)
                    qty_list = []
                    cursor.execute(get_current_quantity)
                    for qty in cursor.fetchall():
                        a,*b = qty
                        qty_list.append(a)
                    new_quantity = qty_list[0] + quantity
                    update_stock_query = """
                    UPDATE stock
                    SET quantity = '%s'
                    WHERE barcode = '%s'
                    """%(new_quantity,barcode)
                    cursor.execute(update_stock_query)
                    connection.commit()
                else: #Add item as new
                    add_to_stock_query = """
                    INSERT INTO stock (barcode,admin_id,title,quantity)
                    VALUES (%s,%s,%s,%s)
                    """
                    create_product_query = """
                    INSERT INTO products (barcode,title,price)
                    VALUES (%s,%s,%s)
                    """
                    products_values = [(barcode,title,price)]
                    stock_values = [(barcode,self.get_admin_id(),title,quantity,)]
                    cursor.executemany(add_to_stock_query,stock_values)
                    cursor.executemany(create_product_query,products_values)
                    connection.commit()
        else:
            raise ValueError('This user does not have admin privileges')



class Customer(Store):
    def __init__(self,firstname,lastname,username):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self._shopping_list = set()
        self._purchased_items = set()

    def shopping_list(self):
        return self._shopping_list
    
    def purchased_items(self):
        return self._purchased_items
        
    def purchase_item(self,*items):
        if type(items) != list:
            items = list(items)
        return super().sell_item(Customer(self.firstname,self.lastname,self.username),*items)

class Account:
    _sales_account_record = Store._sales_record

    date = date.today().strftime("%b %d %Y")
    def __init__(self):
        self.__sales_account = self._sales_account_record

