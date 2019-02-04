"""
Contains utility functions used during testing
"""

DEFAULT_INPUT_VERSION = '1.2.3-beta'
DEFAULT_RELEASED_VERSION_MAJOR = '2.0.0'
DEFAULT_OUTPUT_VERSION_MAJOR = '2.0.1-beta'
DEFAULT_OUTPUT_VERSION_MINOR = '1.3.1-beta'
DEFAULT_OUTPUT_VERSION_PATCH = '1.2.4-beta'


def append_to_file(a_file, a_str):
    """
    :param a_str: a string to append to the version file
    """
    with open(a_file, 'a') as file_handle:
        file_handle.write(a_str)
