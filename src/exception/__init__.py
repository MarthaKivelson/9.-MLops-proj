import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error information including file name, line number, and the error message.

    :param error: The exception that occurred.
    :param error_detail: The sys module to access traceback details.
    :return: A formatted error message string.
    """
    #extract traceback details
    _, _, exc_tb = error_detail.exc_info()

    #get file name 
    file_name = exc_tb.tb_frame.f_code.co_filename

    #create a formatted error msg 
    line_number = exc_tb.tb_lineno
    error_msg = f"Error occured in python script: [{file_name}] at the line number [{line_number}]: {str(error)}"

    logging.error(error_msg)

    return error_msg

class MyException(Exception):
    """
    Custom exception class for handling errors in the US visa application.
    """
    def __init__(self, error_msg: str, error_detail: sys):
        """
        Initializes the USvisaException with a detailed error message.

        :param error_message: A string describing the error.
        :param error_detail: The sys module to access traceback details.
        """
        # Call the base class constructor with the error message
        super().__init__(error_msg)

        self.error_msg = error_message_detail(error_detail, error_detail)

    def __str__(self) -> str:
        """
        Returns the string representation of the error message.
        """
        return self.error_msg