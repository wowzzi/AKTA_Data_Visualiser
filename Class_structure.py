import pprint as pp
import pandas as pd
import matplotlib.pyplot as plt
import Functions as f

colours = {"uv": "b", "cond": "C1", "conc": "g"}
simple_arrow = {
    'width': 0.1,
    'headwidth': 1,
    'headlength': 1,
    'shrink': 1
}

class raw_data:
    def __init__(self, dlist = [0,0], primary_y = 0, units = ["min", "mAU"]):
        self.data = dlist
        self.yaxis = primary_y
        self.units = units


class raw_file:
    def __init__(self, file_path, file_type = "csv"):
        self.path = file_path
        self.name = self.path.split("\\")[-1].replace(".xlsx", "")
        if file_type == "csv":
            self.df = pd.read_csv(self.path, skiprows=1, header=[0, 1], encoding = "utf-16", sep = "\t")
            f.rename_df_cols(self.df)
        else:
            self.df = pd.read_excel(self.path, skiprows=1, header=[0, 1])
            self.df.columns = [': '.join(filter(None, col)).strip() for col in self.df.columns.values]

        self.data_dict = {}
        local_list = []
        unit_list = []
        for col in self.df.columns.values:
            column_name = str(col).lower()
            if column_name.find("uv") != -1:
                y_axis = 0
            else:
                y_axis = 1
            local_list.append(f.make_list(self.df, col))
            unit_list.append((col.split(":")[-1]).strip())

            if len(local_list) == 2:
                if unit_list[-1].lower().strip() == "injection":
                    local_list[-1].append("injection")
                self.data_dict[col.split(":")[0]] = raw_data(dlist=list(zip(local_list[0], local_list[1])),
                                                             primary_y=y_axis, units=[unit_list[0], unit_list[1]])
                local_list.clear()
                unit_list.clear()
        del self.df
        self.key_list = list(self.data_dict.keys())

    def __str__(self):
        return self.name


class new_figure:
    def __init__(self, fig_name):
        self.fig, self.ax = plt.subplots()
        self.axes_dict = {}
        self.name = fig_name
        self.fig.suptitle(self.name)


    def __str__(self):
        return self.name

    def plot_data(self, x, y, data_key, units, file_name):
        if self.ax is None:
            self.ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
            self.ax.yaxis.set_label_position('left')
            self.ax.yaxis.tick_left()
        x_units = units[0].strip()
        y_units = units[1].strip()

        if len(self.axes_dict.keys()) == 0:
            self.axes_dict[y_units] = []
            self.axes_dict[y_units].append(self.ax)
            self.axes_dict[y_units].append({})
        else:
            if y_units not in self.axes_dict:
                self.axes_dict[y_units] = []
                self.axes_dict[y_units].append(self.ax.twinx())
                self.axes_dict[y_units].append({})
                self.axes_dict[y_units][0].set_axis_off()
        self.axes_dict[y_units][0].set_xlabel(x_units)
        self.axes_dict[y_units][0].set_ylabel(y_units)
        colour = '0.5'
        for key in colours.keys():
            if key in data_key.lower():
                colour = colours.get(key)

        data_plot_name = f"{file_name} - {data_key}"
        data_plotted = self.axes_dict[y_units][0].plot(x, y, color=colour, label=data_key)
        self.axes_dict[y_units][1][data_plot_name] = data_plotted

    def draw_legend(self):
        self.fig.legend(loc='outside right upper', draggable=True)

    def adjust_y_axes(self):
        #turn all axes off
        for key in self.axes_dict.keys():
            self.axes_dict[key][0].set_axis_off()
        # set stuff to the primary (left) y axis
        print("set the primary y axis")
        ax_key = f.get_single_obj_from_list(self.axes_dict.keys())
        self.axes_dict[ax_key][0].yaxis.set_label_position('left')
        self.axes_dict[ax_key][0].yaxis.tick_left()
        self.axes_dict[ax_key][0].set_axis_on()

        # set stuff to the secondary (right) y axis
        print("set the secondary y axis")
        ax_key = f.get_single_obj_from_list(self.axes_dict.keys())
        self.axes_dict[ax_key][0].yaxis.set_label_position('right')
        self.axes_dict[ax_key][0].yaxis.tick_right()
        self.axes_dict[ax_key][0].set_axis_on()




    def return_axs(self):
        print(f"{self.ax}")
        print(f"{self.fig}")
        pp.pp(f"{self.axes_dict}")