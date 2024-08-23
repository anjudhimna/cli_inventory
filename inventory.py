import psycopg2
import pathlib
import csv
import pandas as pd

host = "localhost"
database = "cli_inventory"
user = "openpg"
password = "openpgpwd"
port = 5432

conn = psycopg2.connect(
host = host,
dbname = database,
user = user,
password = password,
port = port
)
cur = conn.cursor()

print("Datbase connection successfully done...")
choice = 0
print("1) Product List")
print("2) Add Product")
print("3) Delete Product")
print("4) Update Product")
choice = input("Enter Choice : ")
choice = choice.strip()


def delete_row_from_csv(input_file, output_file, row_to_delete):
    # Read the CSV file and store its contents
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Filter out the row to delete (e.g., delete the row containing 'row_to_delete' in the first column)
    updated_rows = [row for row in rows if row[0] != row_to_delete]

    # Write the updated data back to a new CSV file
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(updated_rows)

def update_row_in_csv(input_file, output_file, row_identifier, updates):
    # Read the CSV file and store its contents
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Update the specified row
    for row in rows:
        if row['ProductId'] == row_identifier:  # Replace 'id' with the actual column name used for identification
            for column, new_value in updates.items():
                if column in row:
                    row[column] = new_value

    # Write the updated data back to a new CSV file
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if (choice == "1"):
    print("Select product list")
    cur.execute("select * from product")
    print("Here is the product list: Product Name,Brand,SKU,Quantity")
    for records in cur.fetchall():
         print(records)

elif(choice == "2"):
    print("Add new product")
    addProduct = input("Enter Product Name >>> ")
    prodbrand = input("Enter Product Brand >>> ")
    prodsku = input("Enter Product SKU >>> ")
    prodquantity = input("Enter Product Quantity >>> ")

    #check if sku already exist
    sqlselect = f"select * from product where product_sku = '{prodsku}'"
    cur.execute(sqlselect)
    conn.commit()
    if cur.fetchall():
        print("Product SKU already exist, enter another SKU")
    else:
        product_add = "INSERT INTO product(product_name,product_sku, brand, quantity) VALUES (%s,%s,%s,%s) RETURNING id"
        record_to_insert = (addProduct, f"POO{prodsku}", prodbrand, prodquantity)
        result = cur.execute(product_add, record_to_insert)
        conn.commit()
        lastInsertID = cur.fetchone()[0]
        print(lastInsertID)
        print("Record inserted successfully")
        conn.close()

        datawithHeaders = (("ProductId" , "Product Name", "SKU", "Brand", "quantity"), (lastInsertID , addProduct, f"POO{prodsku}", prodbrand, prodquantity))
        dataNoHeaders = (lastInsertID , addProduct, f"POO{prodsku}", prodbrand, prodquantity)

        # check if csv file exist
        my_file = pathlib.Path("product.csv")

        # if file not exist create new file
        if my_file.is_file():
            with open('Product.csv', "a", newline="") as file:
                if file.writable():
                    print("Product.csv file exist")
                    # append data in csv file
                    writer = csv.writer(file)
                    # Writing the data
                    writer.writerows([dataNoHeaders])
                    print(f"Data written to file")
                else:
                    print("File is not writable")
        else:
            print("file does not exist")
            # create csv file
            with open('Product.csv', 'x') as file:
                print("file created successfully")
                # for line in data:
                print(datawithHeaders)
                writer = csv.writer(file)
                # Writing the data
                writer.writerows(datawithHeaders)
                print(f"Data written to file")

elif(choice == "3"):
    print("Choice selected to delete the product")
    productId = input("Enter product id to delete>>>")
    if(productId):
        # check if ID exist in DB or not
        sqlselectId = f"select * from product where id= '{productId}'"
        cur.execute(sqlselectId)
        conn.commit()
        if cur.fetchall():
            # delete from DB and file
            sqlDelete = f"delete from product where id={productId}"
            cur.execute(sqlDelete)
            conn.commit()
            print(f"{productId} productid delete from Database")

            # delete row from csv file as well
            input_file = 'Product.csv'
            output_file = 'Product.csv'
            row_to_delete = productId  # Replace with the identifier of the row you want to delete
            delete_row_from_csv(input_file, output_file, row_to_delete)
            print(f"{productId} productid delete from CSV file")
        else:
            print("The product id you enter is not correct.......")
    else:
        print("Please enter product id")
elif(choice == "4"):
    print("Update product choice selected.....")
    productId = input("Enter product id to be update>>>")
    # check if ID exist in DB or not
    sqlselectId = f"select * from product where id= '{productId}'"
    cur.execute(sqlselectId)
    conn.commit()
    if cur.fetchall():
        # update product in DB and file
        # get  product information from user
        prdName = input("Enter new name of product>>")
        prdBrand = input("Enter new brand of product>>")
        prdquantity = input("Enter new Quantity of product>>")

        dataToUpdate = (prdName, prdBrand, prdquantity)

        sqlUpdate = (f"update product set product_name='{prdName}' , brand='{prdBrand}' , quantity={prdquantity} where "
                     f"id={productId}")
        cur.execute(sqlUpdate)
        conn.commit()
        print(f"{productId} productID Update in Database")

        # update row from csv file as well
        input_file = 'Product.csv'
        output_file = 'Product.csv'
        row_to_update = productId  # Replace with the identifier of the row you want to delete
        updates = {
            'Product Name': prdName,
            'Brand': prdName,
            'quantity' :prdquantity

        }
        update_row_in_csv(input_file, output_file, row_to_update, updates)
        print(f"{productId} productID Update in CSV file")

    else:
        print("The product id you enter is not correct.......")

else:
    print("You did not select a correct choice,start again")






