#בס"ד
#Author : Tsibulsky David 309444065

import datetime
import pandas as pd
import numpy as np
import os

def read_from_csv():
    # assign directory with csv files :
    directory = 'attendance_csv_files'

    #init empty df for result
    result = pd.DataFrame(columns=['Name','minutes'])

    total_minuts_of_all_lecturs = 0

    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a csv file
        if os.path.isfile(f) and str(f).endswith(".csv"):
            #read csv file
            df = pd.read_csv(f, encoding= 'utf-16',engine='python', sep = '\t') #encoding= 'unicode_escape'

            #calculate  the lecture  duretion
            meeting_start_time = datetime.datetime.strptime(df["Meeting Start Time"][0][1:], '"%Y-%m-%d %H:%M:%S"')
            meeting_end_time = datetime.datetime.strptime(df["Meeting End Time"][0][1:], '"%Y-%m-%d %H:%M:%S"')
            timedelta_obj= meeting_end_time-meeting_start_time
            diff_in_minutes = timedelta_obj.total_seconds() / 60
            total_minuts_of_all_lecturs +=diff_in_minutes


            #create column with attendee duration in minutes , cast to integer
            df['minutes'] = df['Attendance Duration'].str.split(' ').str[0]
            df['minutes'] = df['minutes'].astype(int)

            #summarize all the entries of the same attendee
            df2 = df.groupby('Name').sum()

            #merge with a previous result
            result = pd.merge(result, df2, on="Name", how="outer")
            result = result.fillna(0)
            result["minutes"] = result["minutes_x"] + result["minutes_y"]
            result.drop(['minutes_x', 'minutes_y'], axis=1, inplace=True)


    #arrange columns
    result["Total lecture time (min)"] = round(total_minuts_of_all_lecturs,2)
    result["% Attendance time"] = (result["minutes"]/total_minuts_of_all_lecturs).round(2)
    result.rename(columns={"minutes":"Total atendance time (min)"},inplace=True)
    result["More then 70% Attendence"] = np.where(result["% Attendance time"] >= 0.7 , "    YES", "    NO")

    #save the result to csv file
   # result.to_csv('output.csv', index=False ,encoding = 'utf-8-sig')

    return result

if __name__ == '__main__':
    read_from_csv()

