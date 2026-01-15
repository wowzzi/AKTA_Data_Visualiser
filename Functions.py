import pandas as pd
import glob
import Class_structure as cs
import prompt_dictionary as prod

def make_list(whichdf, colx):
    result = []
    for p in range(len(whichdf)):
        x = whichdf[colx].iloc[p]
        if pd.notna(x):
            if type(x) == str:
                result.append(x)
            else:
                result.append(float(x))
        else:
            break
    return result


def user_input_path():
    while True:
        print("paste the path to your folder containing the data,"
              "include wild card * to select all from a given extension\n"
              "e.g. C:\\users\\your_name\\*.xlsx")
        path = input("input your path:")
        try:
            result_list = glob.glob(path)
        except:
            print("there was an error with your path")
            print()
        else:
            if len(result_list) == 0:
                print("we could not find any files in that location, check the path,"
                      "the wildcard and the file extension")
            else:
                print(f"we found {len(result_list)} suitable files")
                break
    return result_list


def unpack_raw_file(path_list):
    object_list = []
    file_extension = (path_list[0]).split(".")[-1]
    file_extension.lower().strip()
    i = 1
    for repo in path_list:
        print(f"Processing files {i}/{len(path_list)} please wait")
        object_list.append(cs.raw_file(repo, file_type = file_extension))
        i += 1
    return object_list

def rename_df_cols(whichdf):
    #extract column list from the df into a singular 1-d list (intended for CSV not xlsx)
    native_columns = [item.strip() for _tup in whichdf.columns.values for item in _tup]
    i = 2                               #initialize at 2 to avoid going out of range.
    while i < len(native_columns):
        current_name = native_columns[i]
        if "unnamed" in current_name.lower():
            native_columns[i] = native_columns[i - 2]    #reassign the unnamed columns
        i += 1

    temp_list = []
    final_list = []
    #reconstruction of the column names in a single list.
    for term in native_columns:
        temp_list.append(term)
        if len(temp_list) == 2:
            final_list.append(": ".join(temp_list))
            temp_list.clear()

    whichdf.columns = final_list



def init_new_fig(name="default"):
    return cs.new_figure(name)

def num_only(input_string):
    return "".join(char for char in input_string if char.isnumeric())

def unique_characters(primary_string, comparator_string):
    return "".join(char for char in primary_string if char not in comparator_string)

def unique_list(primary_list, comparator_list):
    return [item for item in primary_list if item not in comparator_list]


def return_key_input(whichdict):
    temp_dict = {}
    for n, key in enumerate(whichdict.keys()):
        print(f"{n}. {key}")
        temp_dict[str(n)] = key
    while True:
        user_input = input("input the desired menu option number:")
        user_input = num_only(user_input)
        try:
            output = temp_dict[user_input]
            break
        except:
            print("key error, retry")
            continue

    return whichdict[output]

def get_single_obj_from_list(whichlist):
    temp_dict = {}
    for n, obj in enumerate(whichlist):
        print(f"{n}. {obj}")
        temp_dict[str(n)] = obj
    while True:
        user_input = input("input the desired menu option number:")
        user_input = num_only(user_input)
        try:
            output = temp_dict[user_input]
            break
        except:
            print("key error, retry")
            continue
    return output


def get_multiple_obj_from_list(whichlist):
    temp_dict = {}
    for n, item in enumerate(whichlist):
        print(f"{n}. {item}")
        temp_dict[n] = item
    user_selection = input("")








def extract_lists(list1 =["x"], list2=["y"]):
    pass

