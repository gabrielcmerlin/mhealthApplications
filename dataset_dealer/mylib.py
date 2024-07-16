from Reader import Reader
from Writer import Writer

from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import signal

import numpy as np
import scipy.stats as stats

import pywt
import math

def normalizeSeries(filename: str, newFilename: str, tSeriesLen: int = 900):
    '''
    Receives a first file (filename) and normalize all its RGB series, creating
    a second file (newFilename). None of the exam results are changed.
    '''

    reader = Reader()
    timeSeries, examResults = reader.readFile(filename, tSeriesLen=tSeriesLen)

    # Creating a new ndarray to store the processed series.
    timeSeriesAux = np.empty((len(timeSeries), 3, tSeriesLen))

    # 'ts' contains the 3 series (RGB) of a person.
    for i, ts in enumerate(timeSeries):
        tsRed = ts[0]
        tsGreen = ts[1]
        tsBlue = ts[2]

        # Normalizing the series.
        tsRed = stats.zscore(tsRed)
        tsGreen = stats.zscore(tsGreen)
        tsBlue = stats.zscore(tsBlue)

        # If a serie is 0 all the time, when we normalize
        # it, we get a NaN serie. Then, transforming an
        # NaN serie in a zeros serie.
        if math.isnan(tsRed[0]):
            tsRed = np.zeros(tSeriesLen)
        if math.isnan(tsGreen[0]):
            tsGreen = np.zeros(tSeriesLen)
        if math.isnan(tsBlue[0]):
            tsBlue = np.zeros(tSeriesLen)

        timeSeriesAux[i] = [tsRed, tsGreen, tsBlue]
        
    # Writing a new file with normalized series
    writer = Writer()
    writer.setFile(newFilename, 'new')
    writer.writeFile(timeSeriesAux, examResults)

def detrendSeries(filename: str, newFilename: str, period: int = 60):
    '''
    Receives a first file (filename) and detrend all its RGB series, creating
    a second file (newFilename). None of the exam results are changed.
    '''

    reader = Reader()
    timeSeries, examResults = reader.readFile(filename)

    # Creating a new ndarray to store the processed series.
    timeSeriesAux = np.empty((len(timeSeries), 3, len(timeSeries[0][0]) - period))

    # 'ts' contains the 3 series (RGB) of a person.
    for i, ts in enumerate(timeSeries):
        tsRed = ts[0]
        tsGreen = ts[1]
        tsBlue = ts[2]

        # Decomposing the series.
        decomposedRed = seasonal_decompose(tsRed, model='aditive', period=period)
        decomposedGreen = seasonal_decompose(tsGreen, model='aditive', period=period)
        decomposedBlue = seasonal_decompose(tsBlue, model='aditive', period=period)

        # Getting its values.
        tsRed = decomposedRed.seasonal + decomposedRed.resid
        tsGreen = decomposedGreen.seasonal + decomposedGreen.resid
        tsBlue = decomposedBlue.seasonal + decomposedBlue.resid

        # Erasing the data lost by the detrend operation.
        tsRed = tsRed[~np.isnan(tsRed)]
        tsGreen = tsGreen[~np.isnan(tsGreen)]
        tsBlue = tsBlue[~np.isnan(tsBlue)]

        timeSeriesAux[i] = [tsRed, tsGreen, tsBlue]

    # Writing a new file with detrended series
    writer = Writer()
    writer.setFile(newFilename, 'new')
    writer.writeFile(timeSeriesAux, examResults)

def fftSeries(filename: str, newFilename: str, freqList: list[float], tSeriesLen: int = 900):
    '''
    Receives a first file (filename) and clean the frequencies on 'freqList' of
    all its RGB series (FFT denoising), creating a second file (newFilename). 
    None of the exam results are changed.
    '''

    reader = Reader()
    timeSeries, examResults = reader.readFile(filename, tSeriesLen=tSeriesLen)

    # Creating a new ndarray to store the processed series.
    timeSeriesAux = np.empty((len(timeSeries), 3, tSeriesLen))

    fs = 900 / 30    # Sampling frequency (900 observations during 30s)
    Q = 0.85         # Quality factor

    # 'ts' contains the 3 series (RGB) of a person.
    for i, ts in enumerate(timeSeries):
        tsRed = ts[0]
        tsGreen = ts[1]
        tsBlue = ts[2]

        # Erasing all the frequencies passed by parameter.
        for freq in freqList:
            w0 = freq / (fs / 2)

            b, a = signal.iirnotch(w0, Q)

            tsRed = signal.lfilter(b, a, tsRed)
            tsGreen = signal.lfilter(b, a, tsGreen)
            tsBlue = signal.lfilter(b, a, tsBlue)

        timeSeriesAux[i] = [tsRed, tsGreen, tsBlue]

    # Writing a new file with denoised series.
    writer = Writer()
    writer.setFile(newFilename, 'new')
    writer.writeFile(timeSeriesAux, examResults)

def __denoiseWavelet(data: np.array, wavelet: str = 'db10', threshold_type: str = 'soft') -> np.array:
    '''
    Receives one serie and returns it denoised using Wavelet Transform.
    '''
    
    coeffs = pywt.wavedec(data, wavelet, mode='per')
    coeffs_thresholded = [pywt.threshold(c, value=0.3, mode=threshold_type) for c in coeffs]

    return pywt.waverec(coeffs_thresholded, wavelet, mode='per')

def waveletSeries(filename, newFilename, tSeriesLen=900):
    '''
    Receives a first file (filename) and denoises all its RGB series using Wavelet
    Transform, creating a second file (newFilename). None of the exam results are changed.
    '''
    
    reader = Reader()
    timeSeries, examResults = reader.readFile(filename, tSeriesLen=tSeriesLen)

    # Creating a new ndarray to store the processed series.
    timeSeriesAux = np.empty((len(timeSeries), 3, tSeriesLen))

    # 'ts' contains the 3 series (RGB) of a person.
    for i, ts in enumerate(timeSeries):
        # Denoising the series.
        tsRed = __denoiseWavelet(ts[0])
        tsGreen = __denoiseWavelet(ts[1])
        tsBlue = __denoiseWavelet(ts[2])

        timeSeriesAux[i] = [tsRed, tsGreen, tsBlue]

    # Writing a new file with denoised series.
    writer = Writer()
    writer.setFile(newFilename, 'new')
    writer.writeFile(timeSeriesAux, examResults)