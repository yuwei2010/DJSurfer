#coding:utf-8

"""
Description: extract relevant data such as NTC measured data from a series of external report files (.txt)
Python implementation: using regular expression to extract data, using pandas DataFrame format to store the extracted data
Author: Xiaofeng Yan
Date: 2024-05-01
Version: 0.2
"""

import re
import pandas as pd
import os
from djsurfer.datainterface import DataInterface

class TextReportObject(DataInterface):
    """
    A class representing a text object to extract data in a text file.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
    """

    def __init__(self,path, name=None,comment=None, delimiter=','):

        #Initialize the text interface object, passing the path, name, comment, chunk delimiter to the base class.
        super().__init__(path=path, name=name, comment=comment)

        #Default delimiter is a comma
        self.delimiter = delimiter

    def get_df(self):
        """
        Read the text file and return its selected contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents of the extracted data from text file as a DataFrame.
        """
        #open report file
        with open(path, "r") as file:
            content =file.read()


        failure_match = re.search(r"Failures: \s+(\d+)", content)
        file_match = re.search(r"File Name:\s+(\S+)", content)
        date_match =re.search(r"Report Date:\s+(\w+\s+\d+,\s+\d+)", content)
        time_match = re.search(r"Time:\s+(\d{1,2}:\d{2}:\d{2})", content)
        #time_match = re.search(r'Time:\s+(\d{1,2}:d{2}:\d{2})', content).group(1)
        ntc1_match = re.search(r"NTC1\s+\d+\.\d+K\s+\d+\.\d+\w+\s+(\d+\.\d+)K", content)
        ntc2_match = re.search(r"NTC2\s+\d+\.\d+K\s+\d+\.\d+\w+\s+(\d+\.\d+)K", content)
        c1_match = re.search(r"C1\s+\d+\.\d+p\s+\d+\.\d+\w+\s+(\d+\.\d+)pF", content)
        c2_match = re.search(r"C2\s+\d+\.\d+p\s+\d+\.\d+\w+\s+(\d+\.\d+)pF", content)
        isoRes1_match = re.search(r"5-51_Op\s+\d+\.\d+M\s+\D\s\d+\s\w\s+([><]?\s?\d+[\.\d+\s]?\s)M", content)
        isoRes2_match = re.search(r"6-52_Op\s+\d+\.\d+M\s+\D\s\d+\s\w\s+([><]?\s?\d+[\.\d+\s]?\s)M", content)

        #print(isoRes1_match)
        #print(ntc2_match)

        # Create DataFrames with extracted data
        data = {
            "Filename": [file_match.group(1)] if file_match else [None],
            "Date":[date_match.group(1)] if date_match else [None],
            "Time":[time_match.group(1)] if time_match else [None],
            #"NTC1_measured [KOhm]":[float(ntc1_match.group(1).replace("K",""))] if ntc1_match else [None],
            "NTC1_measured [KOhm]":[float(ntc1_match.group(1))] if ntc1_match else [None],
            "NTC2_measured [KOhm]":[float(ntc2_match.group(1))] if ntc2_match else [None],
            "Cap1_measured [pF]":[float(c1_match.group(1))] if c1_match else [None],
            "Cap2_measured [pF]":[float(c2_match.group(1))] if c2_match else [None],
            "IsoRes1_measured [MOhm]":[isoRes1_match.group(1)] if isoRes1_match else [None],
            "IsoRes2_measured [MOhm]":[isoRes2_match.group(1)] if isoRes2_match else [None],
            "Failure":[int(failure_match.group(1))] if failure_match else [None]
            }
        df = pd.DataFrame(data)

        return df


    def to_excel(self, path):
        """
        Save the text object to an Excel file.

        Args:
            path (str): The path to save the Excel file.
        """
        self.df.to_excel(path, index=False)


if __name__ == '__main__':
    # set the right report file path in datalake
    # Testcase: using local directory containing all report text files
    #report_directory_path =r"C:\Users\yax3si\Documents\Python Scripts\Project_DataEng\mydata\ICTDatalog"

    from pathlib import Path
    #df_obj = TextReportObject(Path(__file__).parent /r" ..\..\tests\demo_data\txt_datapool\217312-0128-15_CELL_Testfile_split_1.txt")
    path = r"C:\Users\yax3si\Documents\Python Scripts\PythonProject_DJSurfer\tests\demo_data\txt_datapool\217312-0128-15_CELL_Testfile_split_2.txt"
    df_obj = TextReportObject(path)
    print(df_obj.get_df())
