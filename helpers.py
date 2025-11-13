# helper functions and variables
import pandas as pd

def generate_empty_plate() -> pd.DataFrame:
    # generates a table based on a 384-well plate


    ROW_IDX = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
    ]

    COLUMNS = range(1,25)

    plate_dict = dict([(column, [''] * 16) for column in COLUMNS])

    empty_plate = pd.DataFrame.from_dict(plate_dict)

    empty_plate.set_index(pd.Series(ROW_IDX), inplace=True)

    return empty_plate