# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql_query('''
                            SELECT firstName, lastName
                            FROM employees
                            WHERE officeCode IN (
                                SELECT officeCode 
                                FROM offices
                                WHERE city = 'Boston'
                              )                           
                              
''', conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql_query('''
                            SELECT *
                            FROM employees
                            RIGHT JOIN offices USING (officeCode) 
                            GROUP BY officeCode 
                            HAVING COUNT(employeeNumber) = 0                     
                              
''', conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql_query('''
                            SELECT firstName, lastName, city, state
                            FROM employees
                            LEFT JOIN offices USING (officeCode) 
                            ORDER BY firstName ASC          
                              
''', conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql_query('''
                            SELECT contactFirstName, contactlastName, phone, salesRepEmployeeNumber
                            FROM customers
                            LEFT JOIN orders USING (customerNumber) 
                            GROUP BY customerNumber 
                            HAVING COUNT(orderNumber) = 0
                            ORDER BY contactLastName ASC                     
                              
''', conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql_query('''
                            SELECT contactFirstName, contactlastName, amount, paymentDate
                            FROM customers
                            JOIN payments USING (customerNumber)
                            ORDER BY CAST(amount AS INTEGER) DESC                
                              
''', conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql_query('''
                            SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS number_of_customers
                            FROM employees e
                            LEFT JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
                            GROUP BY e.employeeNumber
                            HAVING AVG(c.creditLimit) > 90000
                            ORDER BY number_of_customers DESC
                            LIMIT 4
                              
''', conn)


# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql_query('''
                                SELECT productName, COUNT(orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits
                                FROM products
                                JOIN orderdetails USING (productCode)  
                                GROUP BY productCode
                                ORDER BY  totalunits DESC                         
''', conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql_query('''
                                SELECT productName, productCode, COUNT(DISTINCT customerNumber) AS numpurchasers
                                FROM products
                                JOIN orderdetails USING (productCode)
                                JOIN orders USING (orderNumber)
                                GROUP BY productCode  
                                ORDER BY numpurchasers DESC             
''', conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql_query('''
                            SELECT COUNT(customerNumber) AS n_customers, officeCode, offices.city
                            FROM customers
                            JOIN employees ON salesRepEmployeeNumber = employeeNumber 
                            JOIN offices USING (officeCode) 
                            GROUP BY officeCode           
                              
''', conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql_query('''
                            SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, e.officeCode
                            FROM employees e
                            JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
                            JOIN orders ord ON ord.customerNumber = c.customerNumber
                            JOIN orderdetails od ON od.orderNumber = ord.orderNumber
                            JOIN offices o ON o.officeCode = e.officeCode
                            WHERE od.productCode IN (
                                SELECT od2.productCode
                                FROM orderdetails od2
                                JOIN orders ord2 ON ord2.orderNumber = od2.orderNumber
                                GROUP BY od2.productCode
                                HAVING COUNT(DISTINCT ord2.customerNumber) < 20
                            )
                            ORDER BY e.lastName, e.firstName
''', conn)
print(df_under_20)

conn.close()