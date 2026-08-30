import functions
    
options = "a"
while options != "0":
    print("\nMenu:\n0. Exit\n1. Product register\n2. Find product\n3. Filter products\n4. Show product list\n5. Import from API\n")
    print("If the product is registered and if u want to upload or delete... u must choose the option 2")
    options = input("\nOption: ")

    if options == "0":
        print("See yaa")
        break

    if options == "1":
        quantity = int(input("Quantity products: "))
        for i in range(quantity):
            name_product = input("Name product: ")
            id_product = input("ID product: ")
            prize_product = input("Prize product: ")
            stock_product = input("Stock product: ")
            statement = functions.get_valid_statement()
            functions.product(name_product, id_product, prize_product, stock_product, statement)

        choose = input("Show the register?\n1. Yes\n2. No\n")
        if choose == "1":
            print(functions.products)
        elif choose == "2":
            continue
        else: 
            print("That option doesn't exist")

    elif options == "2":
        search_type = input("Search by:\n1. ID\n2. Name\n")
        
        if search_type == "1":
            finder_product = input("Enter ID product: ")
            found_product = functions.find_by_id(finder_product)
            
            if found_product:
                print(f"This is the product: {found_product}")
                choose = input("1. Upload\n2. Delete\n3. Menu\n")
                if choose == "1":
                    info1 = input("Name product: ")
                    info2 = input("ID product: ")
                    info3 = input("Prize product: ")
                    info4 = input("Stock product: ")
                    info5 = functions.get_valid_statement()
                    found_product.update({
                        "Name": info1,
                        "ID": info2,
                        "Prize": info3,
                        "Stock": info4,
                        "Statement": info5,
                    })
                    choose = input("Show?\n1. Yes\n2. No\n")
                    if choose == "1":
                        print(found_product)
                    elif choose == "2":
                        continue
                    else:
                        print("Hey loco, qué pazza valemía, ombee")
                elif choose == "2":
                    print(f"{found_product} has been deleted")
                    found_product.clear()
                elif choose == "3":
                    continue
                else:
                    print("That option doesn't exist")
            else:
                print("Not found")
                
        elif search_type == "2":
            finder_product = input("Enter product name: ")
            found_products = functions.find_by_name(finder_product)
            
            if found_products:
                print(f"Found {len(found_products)} product(s):")
                for idx, prod in enumerate(found_products, 1):
                    print(f"{idx}. {prod}")
                
                try:
                    product_choice = int(input("Select product number to edit (0 to cancel): "))
                    if product_choice == 0:
                        continue
                    if 1 <= product_choice <= len(found_products):
                        selected_product = found_products[product_choice - 1]
                        choose = input("1. Upload\n2. Delete\n3. Menu\n")
                        if choose == "1":
                            info1 = input("Name product: ")
                            info2 = input("ID product: ")
                            info3 = input("Prize product: ")
                            info4 = input("Stock product: ")
                            info5 = functions.get_valid_statement()
                            selected_product.update({
                                "Name": info1,
                                "ID": info2,
                                "Prize": info3,
                                "Stock": info4,
                                "Statement": info5,
                            })
                            print("Product updated")
                        elif choose == "2":
                            print(f"{selected_product} has been deleted")
                            selected_product.clear()
                        elif choose == "3":
                            continue
                    else:
                        print("Invalid selection")
                except ValueError:
                    print("Invalid input")
            else:
                print("Not found")
        else:
            print("That option doesn't exist")
    
    elif options == "3":
        filter_type = input("Filter by:\n1. Status (active/inactive)\n2. Stock range\n3. All products\n")
        
        if filter_type == "1":
            statement = input("Enter status (active/inactive): ")
            filtered = functions.filter_by_statement(statement)
            if filtered:
                print(f"Products with status '{statement}':")
                for prod in filtered:
                    print(prod)
            else:
                print("No products found with that status")
                
        elif filter_type == "2":
            try:
                min_stock = int(input("Enter minimum stock: "))
                max_stock = int(input("Enter maximum stock: "))
                filtered = functions.filter_by_stock_range(min_stock, max_stock)
                if filtered:
                    print(f"Products with stock between {min_stock} and {max_stock}:")
                    for prod in filtered:
                        print(prod)
                else:
                    print("No products found in that stock range")
            except ValueError:
                print("Invalid input")
        elif filter_type == "3":
            if functions.products:
                print("All products:")
                for prod in functions.products:
                    print(prod)
            else:
                print("No products registered")
        else:
            print("That option doesn't exist")
    
    elif options == "4":
        if functions.products:
            print("\nComplete product list:")
            for idx, prod in enumerate(functions.products, 1):
                print(f"{idx}. {prod}")
        else:
            print("No products registered")
    
    elif options == "5":
        print("\n--- Import Products from API ---")
        print("Make sure the API server is running: python api_server.py")
        api_url = input("Enter API URL (press Enter for default 'http://localhost:5000/api/products'): ").strip()
        if not api_url:
            api_url = "http://localhost:5000/api/products"
        
        print(f"Connecting to: {api_url}")
        if functions.sync_products_from_api(api_url):
            print("✓ Import completed successfully!")
        else:
            print("✗ Import failed. Check the API server and try again.")
    
    else:
        print("That option doesn't exist")