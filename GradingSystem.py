# Anderson Lee, CSW8 (F21)

def print_main_menu(the_menu):
    """
    Takes a dictionary menu as input
    and prints the options from the
    dictionary line by line.
    """
    print(26 * '*')
    print('What would you like to do?')
    for key, value in the_menu.items():
        print(f"{key} - {value}")
    print(26 * '*')

def check_option(option, menu):
    """
    Returns "invalid" if the provided `option`
    is not one of the keys in the given `menu`.
    Returns "valid" otherwise.
    """
    validity = 'invalid'
    str_option = str(option)
    for key in menu:
        if option == key:
            validity = 'valid'
    if str_option.isdigit() == False:
        print(f"WARNING: `{option}` is not an integer.\nPlease enter an integer.")
    elif validity == 'invalid':
        print(f"WARNING: `{option}` is an invalid option.\nPlease enter a valid option.")
    return validity
    
def list_categories(grade_dict, showID = False):
    """
    The function takes two arguments: a dictionary
    and a Boolean flag that indicates whether to
    display the category IDs.
    The first argument is a dictionary, that stores a
    numeric ID as a key for each category;
    the corresponding value for the key is
    a list that contains a category item
    with 3 elements arranged as follows: 
    * `'name'` - the name of the category,
        e.g., "quiz", "participation";
    * `'percentage'` - the percentage of the total grade,
        e.g., 25, 5, 10.5; 
    * `'grades'` - a list of numeric grades.

    By default, displays the dictionary values as
    CATEGORY NAME : PERCENTAGE%
    If showID is True, the values are displayed as
    ID - CATEGORY NAME : PERCENTAGE%
    If a dictionary is empty, prints "There are no categories."
    If a dictionary has a single category,
    prints "There is only 1 category:"
    Otherwise, prints "There are X categories:"
    where X is the number of records in the dictionary.
    Returns the number of records.
    """
    if grade_dict == {}:
        print("There are no categories.")
    elif len(grade_dict) == 1:
        print("There is only 1 category:")
    else:
        print(f"There are {len(grade_dict)} categories:")
    if showID == True:
        for key, value in grade_dict.items():
            print(f"{key} - {value[0].upper()} : {value[1]}%")
    else:
        for key, value in grade_dict.items():
            print(f"{value[0].upper()} : {value[1]}%")
    return len(grade_dict)

def create_id(grade_dict, offset = 0):
    """
    Return an integer ID that would be generated 
    for the next value inserted into the `db`.
    """
    key_list = []
    if grade_dict == {}:
        return offset
    else:
        for key in grade_dict:
            key_list.append(key)
        maximum = max(key_list)
        return maximum + offset + 1

def is_numeric(val):
    """
    Returns True if the string `val`
    contains a valid integer or a float.
    """
    counter = 0
    for char in val:
        if char == '.':
            counter += 1
    float_val = val.replace('.', '')
    float_val = val.replace(' ', '')
    if float_val.isdigit() == True and counter <= 1:
        return True

def add_category(db, cid, info_str):
    info_list = info_str.split()
    if len(info_list) != 2:
        return -2
    if is_numeric(info_list[1]) != True:
        return -1
    else:
        float_per = float(info_list[1])
        db[cid] = [info_list[0], float_per]
        return cid

def add_categories(db, max_num, id_offset):
    """
    Prompts the user to enter a single-word category name
    and the corresponding percentage of the total grade.
    Calls `create_id()` to get the ID for the category.
    Calls `add_category()`, and keeps asking the user to
    input the correct value for that category, if
    its percentage is not a number (int or float).
    """
    cur_cat = 1
    print(f"You can add up to {max_num} categories.")
    print("::: How many categories will you add?")
    num_cat = input("> ")
    while num_cat.isdigit() == False:
        print(f"`{num_cat}` is not a valid integer.")
        num_cat = input("::: Enter a valid number of categories you plan to add\n>")
    int_num_cat = int(num_cat)
    if len(db) + int_num_cat > max_num:
        print(f"WARNING: Adding {len(db) + int_num_cat} categories would exceed the allowable max.\nYou can store up to {max_num} categories.\nCurrent total of categories is {len(db)}.")
        return
    for cat in range(int_num_cat):
        user_input = input(f"::: Enter the category {cur_cat} name (no spaces) followed by its percentage\n<")
        add_id = create_id(db, id_offset)
        while add_category(db, add_id, user_input) == -1 or add_category(db, add_id, user_input) == -2:
            print("WARNING: invalid input for the name and percentage.")
            user_input = input(f"::: Enter the category {cur_cat} name (no spaces) followed by its percentage\n::: or enter M to return back to the menu.\n")
            if user_input == 'M' or user_input == 'm':
                break
        add_category(db, add_id, user_input)
        cur_cat += 1

def update_category(db):
    """
    Prompts the user to enter the category ID
    and then asks to enter the updated information:
    name and the corresponding percentage of the total grade.
    Calls list_categories() at the beginning of the function,
    and add_category() to update the info.
    """
    print("Below is the info for the current categories.")
    list_categories(db, True)
    exists = False
    if len(db) != 0:
        print("::: Enter the category ID that you want to update")
        user_ID = input("> ")
        while exists == False:
            for key in db:
                if int(user_ID) == key:
                    exists = True
                    print(f"Found a category with ID `{user_ID}`:")
                    print("::: Enter the updated info:\n    category name followed by the percentage.")
                    user_cat = input('< ')
                    if add_category(db, int(user_ID), user_cat) == -2:
                        print("WARNING: insufficient information for the update.")
                        print(f"Record with ID `{user_ID}` was not updated!")
                    elif add_category(db, int(user_ID), user_cat) == -1:
                        print("WARNING: invalid input for the name and/or percentage.")
                        print(f"Record with ID `{user_ID}` was not updated!")
                    else:
                        add_category(db, int(user_ID), user_cat)
                else:
                    print(f"WARNING: `{user_ID}` is not an ID of an existing category.")
                    print("::: Enter the ID of the category you want to update")
                    print("::: or enter M to return back to the menu.")
                    user_ID = input("> ")
                    if user_ID == 'M' or user_ID == 'm':
                        return
                    else:
                        for key in db:
                            if int(user_ID) == key:
                                exists = True
                                print(f"Found a category with ID `{user_ID}`:")
                                print("::: Enter the updated info:\n    category name followed by the percentage.")
                                user_cat = input('< ')
                                if add_category(db, int(user_ID), user_cat) == -2:
                                    print("WARNING: insufficient information for the update.")
                                    print(f"Record with ID `{user_ID}` was not updated!")
                                elif add_category(db, int(user_ID), user_cat) == -1:
                                    print("WARNING: invalid input for the name and/or percentage.")
                                    print(f"Record with ID `{user_ID}` was not updated!")
                                else:
                                    add_category(db, int(user_ID), user_cat)
    return

def delete_category(db):
    """
    Calls list_categories() at the beginning of the function.
    Prompts the user to enter the category ID
    and then verifies the information and selection by printing 
    that record from the `db`.
    Deletes the category and its info, once the user confirms.
    """
    print("Below is the info for the current categories.")
    list_categories(db, True)
    key_list = []
    exists = False
    if len(db) != 0:
        print("::: Enter the category ID that you want to delete")
        user_ID = input('> ')
        while exists == False:
            for key in db:
                key_list.append(key)
            if int(user_ID) in key_list:
                exists = True
                print(f"Found a category with ID `{user_ID}`:")
                print(db[int(user_ID)])
                print("::: Are you sure? Type Y or N")
                user_resp = input('> ')
                if user_resp == 'Y':
                    del db[int(user_ID)]
                    print("Deleted")
                else:
                    print("Looks like you aren\'t 100% sure.\nCancelling the deletion.")  
            else:
                print(f"WARNING: `{user_ID}` is not an ID of an existing category.")
                print("::: Enter the category ID that you want to delete")
                print("::: or enter M to return back to the menu.")
                user_ID = input('> ')
                if user_ID == 'M' or user_ID == 'm':
                    return
    return                            

def add_grades(db):
    """
    Calls list_categories() at the beginning of the function.
    Prompts the user to enter the category ID
    and then asks to enter the grades for that category. 
    Convert the grades string to the list of float values.
    Calls add_category_grades() to insert the record.
    Does not add the grades if not all provided grades
    contain numeric scores.
    """
    key_list = []
    print("Below is the info for the current categories.")
    list_categories(db, True)
    exists = False
    if len(db) != 0:
        print("::: Enter the category ID for which you want to add grades")
        user_ID = input('> ')
        while exists == False:
            for key in db:
                key_list.append(key)
            if int(user_ID) in key_list:
                exists = True
                print(f"You selected a {db[int(user_ID)][0].upper()} category.")
                print("::: Enter space-separated grades")
                print("::: or enter M to return back to the menu.")
                user_grades = input('> ')
                if user_grades == 'M' or user_grades == 'm':
                    return
                else:
                    #if add_category_grades(db, int(user_ID), user_grades) != -1:
                    add_category_grades(db, int(user_ID), user_grades)
                    print(f"Success! Grades for the {db[int(user_ID)][0].upper()} category were added.")
            else:
               print(f"`{user_ID}` is not an ID of an existing category.")
               print("::: Enter the ID of the category to add grades to")
               print("::: or enter M to return back to the menu.")
               user_ID = input('> ')
               if user_ID == 'M' or user_ID == 'm':
                    return

def add_category_grades(db, cid, grades_str):
    """
    Inserts into the `db` collection (a dictionary)
    a list of grades for the provided category ID.
    The list is obtained from the grades_str.
    Calls is_numeric() to check each grade in 
    grades_str: if all provided grades were not numeric, 
    does not update the dictionary and returns -1.
    Stores the grades as a list of floats (not as strings).
    Calls show_grades_category() if the user adds grades to a category
    that already has grades added to it. 
    If a category with the provided ID already has grades
    in it, then the new grades are appended to the existing
    grades and updated information is displayed.
    Returns the number of grades that were added.
    """
    if is_numeric(grades_str) == True:
        if len(db[cid]) > 2:
            show_grades_category(db, cid)
            float_grade_list = []
            grade_list = grades_str.split()
            for grade in grade_list:
                float_grade_list.append(float(grade))
            initial_dict = db[cid][0:2]
            db[cid] = initial_dict + [db[cid][2] + float_grade_list]
            show_grades_category(db, cid)
            return len(grade_list)
        else:
            float_grade_list = []
            grade_list = grades_str.split()
            for grade in grade_list:
                float_grade_list.append(float(grade))
            initial_dict = db[cid]
            db[cid] = initial_dict + [float_grade_list]
            return len(grade_list)
    else:
        return -1
    
def show_grades(db):
    """
    Calls list_categories() at the beginning of the function.
    If the dictionary is empty, return from the function.
    Otherwise, prompts the user to enter the category ID or 
    enter "A" to show grades of all categories that store them
    If the provided ID is not valid, prompt the user to enter 
    a valid ID or go back to the menu using ‘M’ or ‘m’ as input.
    Calls show_grades_category() with appropriate arguments 
    to show the grades.
    """
    exists = False
    print("Below is the info for the current categories.")
    list_categories(db, True)
    if len(db) == 0:
        return
    else:
        print("::: Enter the category ID for which you want to see the grades")
        print("::: or enter A to list all of them.")
        user_ID = input('> ')
        while exists == False:
            if user_ID == 'A':
                for key in db:
                    show_grades_category(db, key)
                    exists = True
            else:
                for key in db:
                    if int(user_ID) == key and len(db[key]) == 3:
                        exists = True
                        show_grades_category(db, key)
                    elif int(user_ID) == key and len(db[key]) == 2:
                        print(f"No grades were provided for category ID `{user_ID}`.")
                        return
                    else:
                        print(f"WARNING: `{user_ID}` is not an ID of an existing category.")
                        print("::: Enter the category ID for which you want to see the grades")
                        print("::: or enter M to return back to the menu.")
                        user_ID = input('> ')
                        if user_ID == 'M' or user_ID == 'm':
                            return        

def show_grades_category(db, cid):
    """
    Displays the grades the user added into the db collection (dictionary), 
    for the provided category ID `cid`.
    If there are no grades, display "No grades were provided for category ID `cid`."
    and return 0.
    Otherwise, print the capitalized category name followed by a word "grades",
    and then a list of grades. Print the grades list without any beautification. 
    E.g.: QUIZ grades [100, 100, 95, 5, 80, 0]
    Return the number of grades in the grades list.
    """
    if len(db[cid]) == 3:
        print(f"{db[cid][0].upper()} grades {db[cid][2]}")
        return len(db[cid][2])
    else:
        print(f"No grades were provided for category ID `{cid}`.")
        return 0

def save_data(db):
    """
    Calls list_categories() at the beginning of the function.
    If there are no categories, notify the user and return 0.
    By default, save the `db` to a CSV file.
    Asks the user whether to read from the default filename
    or ask for the filename to open.
    Calls save_dict_to_csv() to create the file.
    """
    print("Below is the info for the current categories.")
    list_categories(db,True)
    if len(db) == 0:
        print("Skipping the creation of an empty file.")
        return 0
    else:
        print("::: Save to the default file (grade_data.csv)? Type Y or N")
        user_res = input("> ")
        if user_res == 'Y':
            print("Saving the database in grade_data.csv")
            save_dict_to_csv(db, "grade_data.csv")
            print("Database contents:")
            print(db)
        if user_res == 'N':
            print("::: Name the file you want save to")
            filename = input('> ')
            print(f"Saving the database in {filename}.csv")
            save_dict_to_csv(db, filename)
            print("Database contents:")
            print(db)

def save_dict_to_csv(db, filename):
    """
    Saves a dictionary into a csv file.
    """
    import csv
    with open(filename, 'w', newline='') as csvfile:
        dict_writer = csv.writer(csvfile)
        list_ints = []
        for key, value in db.items():
            if len(value) == 3:
                for num in value[2]:
                    list_ints.append(str(num))
                name = value[0]
                prct = str(value[1])
                str_ints = ','.join(list_ints)
                row = [str(key), name, prct]
                dict_writer.writerow(row + value[2])
            else:
                name = value[0]
                prct = str(value[1])
                row = [str(key), name, prct]
                dict_writer.writerow(row)

def load_dict_from_csv(filename):
    """
    Given a string containing the filename,
    Opens the file and stores its contents
    into the dictionary, which is returned
    from this function.
    The function assumes that the first element
    on each row will be an integer ID, stored
    as a key in the dictionary, and the values
    that are on the rest of the line are stored
    in a list as follows:
    [row[1], float(row[2]), [float(i) for i in row[3:]]]
    The function returns an empty dictionary
    if the CSV file is empty.
    """
    import csv
    with open(filename) as csvfile:
        dict_reader = csv.reader(csvfile)
        grades_dict = {}
        grades_list = []
        for row in dict_reader:
            key = int(row[0])
            name = row[1]
            prct = float(row[2])
            for num in row[3:]:
                float_num = float(num)
                grades_list.append(float_num)
            grades_dict[key] = [name, prct, grades_list]
            grades_list = []
        return grades_dict

def load_data(db):
    """
    Imports csv and os. Loads data from a dictionary into a csv file.
    Asks user if they want to use the default filename. If not, prompts user
    to enter a name. Checks if the filename ends with csv. If not, keeps prompting the
    user to enter a filename until it ends with csv. Checks if the file exists. If not,
    issues a warning and returns back to the menu.
    """
    import csv
    import os
    filename = "grade_data.csv"
    print(f"::: Load the default file ({filename})? Type Y or N")
    user_res = input('> ')
    if user_res == "Y":
        print(f"Reading the database from {filename}")
        new_db = load_dict_from_csv(filename)
        print("Resulting database:\n", new_db)
        db.update(new_db)
    if user_res == 'N':
        csv = False
        while csv == False:
            print("::: Enter the name of the csv file to load.")
            user_filename = input('> ')
            if user_filename[-3:] != 'csv':
                print(f"WARNING: {user_filename} does not end with `.csv`")
            elif os.path.isfile(user_filename):
                csv = True
                print(f"Reading the database from {user_filename}")
                new_db = load_dict_from_csv(user_filename)
                print("Resulting database:\n", new_db)
                db.update(new_db)
            else:
                print("WARNING: Cannot find a CSV file named '<filename>'")
                return

if __name__ == "__main__":
    the_menu = {'1': 'List categories',
'2': 'Add a category',
'3': 'Update a category',
'4': 'Delete a category',
'5': 'Add grades',
'6': 'Show grades',
'7': 'Grade statistics',
'8': 'Save the data',
'9': 'Upload data from file',
'Q': 'Quit this program'
}
    main_db = {} # stores the grading categories and info
    max_cat = 10 # the max total num of categories a user can provide
    cat_id_offset = 100 # the starting value for the category ID in this program

    opt = None

    while True:
        print_main_menu(the_menu) 
        print("::: Enter an option")
        opt = input("> ")

        if opt == 'Q' or opt == 'q': 
            print("Goodbye")
            break # exit the main `while` loop
        else:
            if check_option(opt, the_menu) == "invalid": 
                continue
            print("You selected option {} to > {}.".format(opt, the_menu[opt]))

        if opt == '1': # note that the menu should store the keys as strings
            list_categories(main_db)
        elif opt == '2':
            add_categories(main_db, max_cat, cat_id_offset)
        elif opt == '3':
            update_category(main_db)
        elif opt =='4':
            delete_category(main_db)
        elif opt == '5':
            add_grades(main_db)
        elif opt == '6':
            show_grades(main_db)
        elif opt == '8':
            save_data(main_db)
        elif opt == '9':
            load_data(main_db)
            

        

        opt = input("::: Press Enter to continue...")

    print("See you next time!")


