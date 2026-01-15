#this file is for the storage of large strings associated
#with specific errors or prompts for different parts of the
#script.
prompt_dict ={
    'make_fig_instruction': {'long_description': "type all numbers corresponding to data you want to plot,"
                                                 "\nUse a comma ',' to separate each number,"
                                                 "\nUse keyword: not, followed by the numbers to filter out data,"
                                                 "\nLeaving blank will plot all data:",
                            'short_description': "type each number you want or keyword 'not' followed by numbers\nseparate"
                                                 "each number with commas.",
                            'key_error': "Likely key error!"
                                         "\nmake sure all the numbers you type exist in the list of curves"
                                         "\nInput your amended selection, see the list of available data "
                                         "above:",
                            'fig_name': "type a name for the figure:",
                            'no_data': "import some data before making figures"}
}
