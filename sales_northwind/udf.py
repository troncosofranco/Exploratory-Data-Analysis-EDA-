import sqlite3
import pandas as pd

#UDF
square = lambda n : n**2

#create context

with sqlite3.connect('northwind.db') as conn:
    
    #add function
    conn.create_function("square",1,square)
    
    #create and connect cursor
    cursor = conn.cursor()
    query = '''
    SELECT *, square(UnitPrice) as square FROM Products where UnitPrice is NOT NULL
    '''
    
    cursor.execute(query)

    results_df = pd.DataFrame(cursor.fetchall())

print(results_df)
    

