import json
from ssl import _create_default_https_context
import string
import random
from json import JSONDecodeError

def Register(type,member_json_file,admin_json_file,Full_Name,Address,Email,Password):
    '''Register Function || Return True if registered successfully else False'''
    if type.lower()=='admin':
        f=open(admin_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Address":Address,
            "Email":Email,
            "Password":Password,
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
        return True
    elif type.lower()=='member':
        f=open(member_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Address":Address,
            "Email":Email,
            "Password":Password,
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
        return True
    else:
        return False

def Login(type,members_json_file,admin_json_file,Email,Password):
    '''Login Functionality || Return True if successfully logged in else False'''
    d=0
    if type.lower()=='admin':
        f=open(admin_json_file,'r+')
    else:
        f=open(members_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        return False
    for i in range(len(content)):
        if content[i]["Email"]==Email and content[i]["Password"]==Password:
            d=1
            break
    f.seek(0)
    f.truncate()
    json.dump(content,f)
    f.close()
    if d==0:
        return False
    return True

def AutoGenerate_ProductID():
    '''Return a autogenerated random product ID'''
    product_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=4))
    return product_ID

def AutoGenerate_OrderID():
    '''Return a autogenerated random product ID'''
    Order_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Order_ID

def Create_Product(owner,product_json_file,product_ID,product_name,manufacturer_name,price,discount,total_stock_available):
    '''Creating a product || Return True if successfully created else False'''
    # storing all the product details into a dictionary
    product_details = {
        "Created By": owner,
        "Product ID": product_ID,
        "Product Name": product_name, 
        "Manufacturer Name": manufacturer_name,
        "Price": price,
        "Discount": discount,
        "Total Stock Available": total_stock_available
    }
    file = open(product_json_file,'r+')
    content = json.load(file)
    content.append(product_details)
    file.seek(0)
    file.truncate()
    json.dump(content,file)
    file.close()
    return True

        
    

def Read_Products(owner,product_json_file):
    '''Reading Products created by the admin(owner)'''
    product = []
    file = open(product_json_file,'r+')
    content = json.load(file)
    for i in range(len(content)):
        if content[i]["Created By"] == owner:
            product.append(content[i])
        else:
            pass
    file.close()
    return product

    

def Read_Product_By_ID(product_json_file,product_ID,Details):
    '''Reading product by ID'''
    file = open(product_json_file,'r+')
    content = json.load(file)
    for i in range(len(content)):
        if content[i]["Product ID"] == product_ID:
            Details.append(content[i])
        else:
            pass
    file.close()
    return Details
    

def Update_Product(product_json_file,product_ID,detail_to_be_updated,new_value):
    '''Updating Product || Return True if successfully updated else False'''
    file = open(product_json_file,'r+')
    content = json.load(file)
    for i in range(len(content)):
        if content[i]["Product ID"] == product_ID:
            content[i][detail_to_be_updated] = new_value
    file.seek(0)
    file.truncate()
    json.dump(content,file)
    file.close()
    return True


    
def Delete_Product(product_json_file,product_ID):
    '''Deleting Product || Return True if successfully deleted else False'''
    file = open(product_json_file,'r+')
    content = json.load(file)
    for i in range(len(content)):
        if content[i]["Product ID"] == product_ID:
             del content[i]
    file.seek(0)
    file.truncate()
    json.dump(content,file)
    file.close()
    return True

    

def Update_Member(member_json_file,name,detail_to_be_updated,new_value):
    '''Updating Member Details || Return True if successfully updated else False'''
    file = open(member_json_file,'r+')
    content = json.load(file)
    for i in range(len(content)):
        if content[i]["Full Name"] == name:
            content[i][detail_to_be_updated] = new_value
    file.seek(0)
    file.truncate()
    json.dump(content,file)
    file.close()
    return True

    

def Place_Order(order_json_file,ordered_by,delivery_address,product_json_file,product_ID,Quantity,Order_ID):
    '''Placing Order, Calculate the Price after discount and Total cost of the order || Return True if order placed successfully else False'''
    file = open(product_json_file,'r+')
    content = json.load(file)
    for i in range(len(content)):
        if content[i]["Product ID"] == product_ID:
            product_name = content[i]["Product Name"]
            price = content[i]["Price"]
            discount = content[i]["Discount"]
            Discount = discount.rstrip(discount[-1])
            price_after_discount = (int(Discount)*price)/100
            totalcost = price_after_discount*Quantity
            content[i]["Total Stock Available"] -= Quantity
    file.seek(0)
    file.truncate()
    json.dump(content,file)
    file.close()       
    order_details = {
        "Order ID": Order_ID,
        "Product Name": product_name,
        "Price": price, 
        "Discount": Discount,
        "Price after Discount":price_after_discount,
        "Quantity": Quantity, 
        "Total Cost": totalcost, 
        "Ordered By": ordered_by, 
        "Delivering to":delivery_address
    }
    order_file = open(order_json_file,'r+')
    content1 = json.load(order_file)
    content1.append(order_details)
    order_file.seek(0)
    order_file.truncate()
    json.dump(content1, order_file)
    order_file.close() 
    return True
    
    

def Order_History(order_json_file,Name,details):
    '''Append the order information into details list'''
    file = open(order_json_file,'r+')
    content = json.load(file)
    for i in range(len(content)):
        if content[i]["Ordered By"] == Name:
            details.append(content[i])
    file.close
    return details