import Functions as f
import Class_structure as cs
import matplotlib.pyplot as plt
import prompt_dictionary as prod

open_objects = []
figures_dict = {}


def import_data_script():
    path_list = f.user_input_path()
    new_objects = f.unpack_raw_file(path_list)
    for obj in new_objects:
        open_objects.append(obj)
    print("imported data successful"
          "\nreturning to main menu..")


def create_figure_script():
    temp_dict = {}
    if len(open_objects) == 0:
        print(f"{prod.prompt_dict['make_fig_instruction']['no_data']}")
        return

    obj_selected = f.get_single_obj_from_list(open_objects)

    print("Available traces with the selected data:")
    #this for loops displays the trace options and saves them in temp dict for later.
    for n, key in enumerate(obj_selected.data_dict.keys()):
        print(f"{n}. {key}")
        temp_dict[str(n)] = key
    user_trace_selection = input(prod.prompt_dict['make_fig_instruction']['long_description'])

    while True:
        if user_trace_selection.lower().find("not") == -1:
            comma_separated = user_trace_selection.split(",")
            result_selection = [f.num_only(_str) for _str in comma_separated]
            if len(result_selection) == 1:
                if result_selection[0] =="":
                    result_selection = [str(n) for n in range(len(obj_selected.data_dict.keys()))]
        else:
            split_string = user_trace_selection.lower().split("not")
            comma_separated = [item.split(",") for item in split_string]
            cleaned_list = []
            for n in range(len(comma_separated)):
                cleaned_list.append([f.num_only(_str) for _str in comma_separated[n]])

            result_selection = f.unique_list([str(n) for n in range(len(obj_selected.data_dict.keys()))], cleaned_list[-1])
            result_selection = (list(set(result_selection)))
            result_selection.sort()
        try:
            selected_keys = [temp_dict[n] for n in result_selection]
            break
        except:
            user_trace_selection = input(prod.prompt_dict['make_fig_instruction']['key_error'])
            continue
    print(f"you selected: {selected_keys}")

    i = 0
    figure_name = input("type a name for the figure, type file, to use the file name as the title:")
    if "file" in figure_name:
        figure_name = obj_selected.name

    if figure_name == "":
        figure_name = "figure"

    updated_name = figure_name
    while updated_name in figures_dict.keys():
        i += 1
        updated_name = figure_name + f"{i}"
    figure_name = updated_name

    figures_dict[figure_name] = cs.new_figure(figure_name)
    current_fig = figures_dict[figure_name]

    for key in selected_keys:
        x_values = [value[0] for value in obj_selected.data_dict[key].data]
        y_values = [value[1] for value in obj_selected.data_dict[key].data]
        if type(y_values[0]) == str:
            pass
        else:
            current_fig.plot_data(x_values, y_values, key, obj_selected.data_dict[key].units, obj_selected.name)
    current_fig.draw_legend()
    current_fig.adjust_y_axes()


def show_plots():
    plt.show()
    for fig_obj in figures_dict.values():
        print(f"deleting figure: {fig_obj}")
        del fig_obj
    figures_dict.clear()


def plot_all():
    if len(open_objects) == 0:
        print(f"{prod.prompt_dict['make_fig_instruction']['no_data']}")
        return

    for data_object in open_objects:
        figures_dict[data_object.name] = cs.new_figure(data_object.name)
        current_figure = figures_dict[data_object.name]
        print(data_object.name)
        print(data_object.key_list)
        for data_key in data_object.data_dict.keys():
            current_raw_data = data_object.data_dict[data_key]
            x_values = [value[0] for value in current_raw_data.data]
            y_values = [value[1] for value in current_raw_data.data]
            if type(y_values[0]) == str:
                pass
            else:
                current_figure.plot_data(x_values, y_values, data_key, current_raw_data.units, data_object.name)
        current_figure.draw_legend()


def hello():
    print("hello")




menu_dict = {
    'main': {'Import data': import_data_script,
             'Create figure': create_figure_script,
             'quit': quit,
             'show plots': show_plots,
             'just plot everything (default settings)': plot_all,
             'print_hello': hello}
}

if __name__ == "__main__":
    while True:
        current_menu = 'main'
        menu_function = f.return_key_input(menu_dict[current_menu])
        menu_function()
