import pandas as pd
import numpy as np
import csv

class Reader():
    '''
    Class that reads the dataset files used on the mHealth project.
    '''

    def __init__(self):
        pass

    def readFile(self, filename: str, tSeriesLen: int = 900) -> tuple[np.ndarray, pd.DataFrame]:
        '''
        Reads a file (filename) contaning series with 'tSeriesLen' length and
        returns a tuple with time series ndarray and exam results DataFrame.

        The original data has 'tSeriesLen' of 900, if you processed the series
        in a way the lengths changed, change this variable.
        '''

        # Opening dataset file.
        with open(filename, "r", encoding="utf-8") as file:
            # Reading the first line that contains the DataFrame header.
            header = next(file).replace("\n","").split(",")

            csvReader = csv.reader(file)

            # Auxiliar variables.
            rgbTimeSeries = []
            iterableAuxData = []

            # Variables that will contain all the data of its type.
            timeSeries = []
            data = []

            # For each line of the dataset...
            for i, row in enumerate(csvReader):
                # Reading serie observations.
                rgbTimeSeries.append(row[:tSeriesLen])

                # Each person has 3 lines of data, in which the first has RED
                # serie data, the second has GREEN serie and the last one the
                # BLUE serie. Furthermore, only the first line of someone's data
                # has theirs exam results.

                # Because of it, if it is the first line of someone...
                if i % 3 == 0:        
                    # Reading the first 2 values (sex and skincolor) as string
                    # and the others (exam results) as floats.
                    iterableAuxData = row[tSeriesLen:tSeriesLen + 2] + [float(x) for x in row[tSeriesLen + 2:]]

                    # Adding the person results in 'data', that will be used to
                    # create the DataFrame.  
                    data.append(iterableAuxData)

                    # Erasing the exam results auxiliar variable.
                    iterableAuxData = []

                # If it is the third (last) line...
                if i % 3 == 2:
                    # Adding the 3 series on ndarray.
                    timeSeries.append(rgbTimeSeries)

                    # Cleaning the auxiliar variable.
                    rgbTimeSeries = []

            return (np.array(timeSeries)).astype(float), pd.DataFrame(data, columns=header)