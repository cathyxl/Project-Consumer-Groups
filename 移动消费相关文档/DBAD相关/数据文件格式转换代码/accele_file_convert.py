"""
    This Python file is used to convert the old log files of acceleration to the latest log files with new acceleration
data format.

    Noticed that the old log files have data format as following:
        person_id, time_step_window, acceleration
    Each old file contains all records of all people in exact one experiment.
    The old file name is like "data2_1.csv" in which the first digit "2" denotes the id of experiment while the second
means that it is the acceleration data that are stored in the file.

    And the new log files have data format like this:
        time_step_window, acceleration_in_x, acceleration_in_y, acceleration_in_z
    Each new type file contains all records of one person in one experiment.
    The name of this kind of file is like "2.1_accele.csv" in which digit "2" denotes the experiment id and the other
digit "1" denotes the person id.

    The old log files need to be placed in the directory "input" which is in the same directory with this Python file.
And the output files will be output into the directory "output" which is also in the same directory with this Python
file.
"""


from os import mkdir, path, remove


# The minimum experiment id.
min_exp_id = 1
# The maximum experiment id.
max_exp_id = 6
# The set of IDs of missing experiments whose IDs are between "min_exp_id" and "min_exp_id".
missing_exp_id_set = set([])


def new_file_writer(exp_id, person_id, tmp_records_of_individual):
    """
    Write to new log files.
    :param exp_id:
    :param person_id:
    :param tmp_records_of_individual:
    :return:
    """
    if not path.exists("output") or path.isfile("output"):
        mkdir("output")
    file_name = str(exp_id) + "."+ person_id + "_accele.csv"
    if path.isfile(file_name):
        remove(file_name)
    with open("output\\" + file_name, "a", True) as new_file:
        for time_step_window, acceleration in tmp_records_of_individual:
            new_row_data = time_step_window + ", " + acceleration + ", 0, 0\n"
            new_file.write(new_row_data)


def old_file_processor(exp_id):
    """
    Read old log file that has records of the exp_id-th experiment and then convert it to the new log files.
    :param exp_id:
    :return:
    """
    file_name = "input\\data" + str(exp_id) + "_1.csv"
    current_person_id = None
    tmp_records_of_individual = []
    with open(file_name, "r", True) as old_file:
        while True:
            str_with_line_break = old_file.readline()
            if str_with_line_break == "":
                new_file_writer(exp_id, current_person_id, tmp_records_of_individual)
                break
            line_str = str_with_line_break.rstrip("\n")
            data_list = line_str.split(",")
            if len(data_list) != 3:
                print("Warning: Invalid row data which should be like this form, \"person_id, time_step_window, acceleration\".")
                continue
            person_id = data_list[0]
            time_step_window = data_list[1]
            acceleration = data_list[2]
            if current_person_id is None:
                current_person_id = person_id
            if person_id != current_person_id:
                new_file_writer(exp_id, current_person_id, tmp_records_of_individual)
                current_person_id = person_id
                tmp_records_of_individual = []
            tmp_records_of_individual.append([time_step_window, acceleration])


def conversion_start(min_exp_id, max_exp_id, missing_exp_id_set = None):
    """
    Run the conversion procedure according to the range of given experiment IDs.
    :param min_exp_id:
    :param max_exp_id:
    :param missing_exp_id_set:
    :return:
    """
    if missing_exp_id_set is None or len(missing_exp_id_set) == 0:
        for exp_id in range(min_exp_id, max_exp_id + 1):
            old_file_processor(exp_id)
    else:
        for exp_id in range(min_exp_id, max_exp_id + 1):
            if exp_id not in missing_exp_id_set:
                old_file_processor(exp_id)


# Here is the entrance of this program.
conversion_start(min_exp_id, max_exp_id, missing_exp_id_set)
