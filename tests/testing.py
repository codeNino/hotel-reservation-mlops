from utils.error import CustomException
from utils.logger import AppLogger
import sys


logger = AppLogger(__file__)()


def divide_number(a, b : int):
    try:
        result = a/b
        logger.info("Dividing two numbers")
        return result
    except Exception as e:
        logger.error("Error occurred")
        raise CustomException("Custom Error zero", sys)
    

if __name__ == "__main__":
    try:
        logger.info("Starting Main Program")
        divide_number(10, 0)
    except CustomException as ce:
        logger.error(str(ce))
