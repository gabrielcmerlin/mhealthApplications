# Time Series in mHealth Applications: Task Definition and Data Collection

## Introduction

Author: Gabriel da Costa Merlin - ICMC/USP

Advisor: Diego Furtado Silva - ICMC/USP

Project financed by Research Support Foundation of the State of São Paulo (FAPESP).

Summary: Monitoring physiological signs, vital signs, and other parameters that can be collected over time from individuals are essential in several tasks in healthcare, such as heart rate estimation and the identification of abnormal heartbeats. However, these time series are obtained by very expensive and usually not portable equipment. On the other hand, with the improvement and miniaturization of sensors capable of transmitting various data types, mobile and wearable devices have increasingly shown themselves as options to support medical decisions. Smartphones and smartwatches have increasingly accurate and diverse sensors, making the World Health Organization consider that mobile health (mHealth) may revolutionize how populations interact with public health systems. However, several scientific and technological challenges need to be overcome for mHealth applications to be viable in practice. Among these challenges are the need for low-cost methods, the heterogeneity and multimodality of the data, and the difficulty in obtaining annotated data. In this scenario, this project proposes investigating the use of Machine Learning for time series in mHealth applications. At the end of this research, we intend to have advanced the state-of-the-art for these applications and still make available the models generated for this, along with all other resources necessary for the advancement of research in the same domain.

## Folders

- App: It has the application code used during data collection and its APK files.
- Scripts: I collect some data and needed to transform it in a single CSV file. In order to not waste a lot of time, scripts were written, some use Selenium to interact with a third party website, others prefer PyDrive to access Google Drive to store its data.
- Dataset_dealer: As said above, a CSV contains all the data collected. For the purpose of ease its handling, I wrote Reader and Writer codes that facilitate the conversion of a CSV to numpy array (time series) and dataframe (targets). Moreover, there is 'mylib.py', which contains some functions to alterate all the time series in a file.
- Train: Some extrisic regression models were trained and compared with these codes.
- Preproc: After the first trainings, the noise of the time series collected presented a great difficulty, then I started studying some ways to remove it, mainly Fast Fourrier Transform.
