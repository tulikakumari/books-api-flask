def validbookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

validObject ={
    "name":"f",
    "price":5.99,
    "isbn":12344567
}

missing_isbn ={
     "name":"f",
     "price":5.99
}
missing_price={
    "name":"f",
    "isbn":12344567
} 
missing_name= {
    "price":5.99,
    "isbn":12344567
}
empty_dictonary={}