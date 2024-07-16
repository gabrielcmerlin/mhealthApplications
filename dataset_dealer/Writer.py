import pandas as pd
import numpy as np
import io

class Writer():
    '''
    Class that writes the dataset files used on the mHealth project.
    '''

    file: io.TextIOWrapper
    status: str

    def __init__(self):
        pass

    def setFile(self, filename: str, status: str):
        '''
        A Writer object can only work with one file each time, then you need to
        specify the filename and its status ('new' or 'old'). The status is
        needed, because some methods are only available for and previous existing
        file ('old') and others for a new file ('new').
        '''

        if status == 'new':
            self.file = open(filename, 'w')
        elif status == 'old':
            self.file = open(filename, 'r+')
        else:
            print('Invalid file status. Only available: \'new\', \'old\'.')
            return

        self.status = status

    def __writePersonInfo(self, tSeries: np.ndarray, dfInfo: pd.DataFrame):
        '''
        Writes in the file all the information about one person.
        '''

        # Iterating through the 3 time series (RGB) of the pacient and writing
        # on each line one time serie.
        for i in range(len(tSeries)):
            linha = tSeries[i].tolist()

            # If it is the first serie (RED), also writing the exam results 
            # (DataFrame) in the line.
            if i == 0:
                linha += (dfInfo.values).tolist()[0]

            self.file.write(','.join(str(e) for e in linha) + '\n')

    def writeOnePerson(self, tSeries: np.ndarray, dfInfo: pd.DataFrame):
        '''
            Receives the RGB time series and the exam results of one pacient and
            handles all the operational process to write it on a file.

            Only available for 'old' status files.
        '''

        if self.status != 'old':
            print('Not possible to use this function with a non \'old\' file status.')
            return
        
        # Reading the written data on the file.
        self.file.seek(0)
        content = self.file.readlines()

        # Getting the headers.
        oldDfHeader = content[0].replace('\n', '').split(',')
        newDfHeader = list(dfInfo)

        # Auxiliar variable to the new person exam results.
        newDfInfo = pd.DataFrame(columns=oldDfHeader)

        added = 0 # Variable counting the new columns brought by the new data.

        # Matching the columns of the new data DataFrame and the pattern of the
        # old file.
        for i in range(len(newDfHeader)):
            if newDfHeader[i] not in oldDfHeader:
                oldDfHeader.append(newDfHeader[i])
                added += 1

            newDfInfo[newDfHeader[i]] = dfInfo[newDfHeader[i]]
        content[0] = ','.join(oldDfHeader) + '\n'

        # Going through the old data and adding a NaN value on the new columns
        # brought by the new data
        for i in range(1, len(content), 3):
            content[i] = content[i].replace('\n','')
            for j in range(added):
                content[i] += ',nan'
            content[i] += '\n'

        # Writing the modified old data.
        self.file.seek(0)
        self.file.writelines(content)

        # Writing the new data.
        self.__writePersonInfo(tSeries[0], newDfInfo)

    def writeFile(self, timeSeriesArray: np.ndarray, dataFrame: pd.DataFrame):
        '''
        Receives a ndarray containing the time series of all pacients and a 
        DataFrame, creating then a file (filename) with the dataset.

        Only available for 'new' status files.
        '''

        if self.status != 'new':
            print('Not possible to use this function with a non \'new\' file status.')
            return

        dfHeader = list(dataFrame)

        # Writing DataFrame header on the first line.
        for i in range(len(dfHeader)):
            self.file.write(f"{dfHeader[i]}")

            # Writing a comma after each member of the DataFrame header unless
            # it is the last one.
            if i != len(dfHeader) - 1:
                self.file.write(",")

        self.file.write("\n")

        # Writing info about the time series and DataFrame.
        for i in range(len(timeSeriesArray)):
            self.__writePersonInfo(timeSeriesArray[i], dataFrame[i:i+1])