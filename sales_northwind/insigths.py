#1 import modules
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def bar_plot(df,x_col,y_col):
    plt.barh(df[x_col], df[y_col])
    plt.title(f'{y_col} vs {x_col}')
    plt.xlabel(y_col)
    plt.gca().invert_yaxis()
    plt.show()


with sqlite3.connect('northwind.db') as conn:
    #create and connect cursor
    cursor = conn.cursor()
    
    #Top 10 products
    query_top_product = '''
        select ProductName, sum(od.UnitPrice*Quantity*(1-Discount)) as Revenue FROM OrderDetails od
        JOIN Products p on p.ProductID = od.ProductID
        group by od.ProductID
        order by Revenue desc
        limit 10
    '''
    top_products_df = pd.read_sql_query(query_top_product,conn)
    print(top_products_df)

    #Top 10 Sellers
    query_top_seller = '''
    select LastName || " " || FirstName as FullName, round(sum(od.UnitPrice*Quantity*(1-Discount)),1) as Revenue FROM OrderDetails od
    JOIN Orders o on o.OrderID = od.OrderID
    JOIN Employees e on e.EmployeeID = o.EmployeeID
    group by e.EmployeeID
    order by Revenue desc
    limit 10
    '''
    top_sellers_df = pd.read_sql_query(query_top_seller,conn)

    #Top 10 employees with more sales number
    query_top_seller_number = '''
    select FirstName || " " || LastName as Employee, count(*) as total_sales from Orders o
    JOIN Employees e on e.EmployeeID = o.EmployeeID
    group by o.EmployeeID
    order by total_sales desc
    LIMIT 10
    '''
    top_sellers_number_df = pd.read_sql_query(query_top_seller_number,conn)

bar_plot(top_products_df, "ProductName","Revenue")
bar_plot(top_sellers_df, "FullName", "Revenue")
bar_plot(top_sellers_number_df, "Employee", "total_sales")


