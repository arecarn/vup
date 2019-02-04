"""
Contains utility functions used during testing
"""


def append_to_file(a_file, a_str):
    """
    :param a_str: a string to append to the version file
    """
    with open(a_file, 'a') as file_handle:
        file_handle.write(a_str)
