from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, lever_pressing, \
    lever_press_latency, cue_iti_responding
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Day', 'tts', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency',
               'Lever Presses', 'Lever Press Latency', 'Lever Press Rate']


def crf_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')
    
    if 'LLeverOn' in eventcode:
        press_latency = lever_press_latency(timecode, eventcode, 'LLeverOn', 'LPressOn')
        (lever_press_rate, iti_rate) = cue_iti_responding(timecode, eventcode, 'StartSession', 'EndSession', 'LPressOn')
    elif 'RLeverOn' in eventcode:
        press_latency = lever_press_latency(timecode, eventcode, 'RLeverOn', 'RPressOn')
        (lever_press_rate, iti_rate) = cue_iti_responding(timecode, eventcode, 'StartSession', 'EndSession', 'RPressOn')
        
    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), loaded_file['tts'], float(dippers),
                         float(dippers_retrieved), float(retrieval_latency), float(total_presses), float(press_latency),
                         float(lever_press_rate)]], columns=column_list)
    
    return df2


(days, df) = loop_over_days(column_list, crf_function)
print(df.to_string())

group_means = df.groupby(['Day', 'tts'])['Dippers', 'Lever Presses', 'Lever Press Rate'].mean().unstack()
group_sems = df.groupby(['Day', 'tts'])['Dippers', 'Lever Presses', 'Lever Press Rate'].sem().unstack()

print(group_means)
print(group_sems)

#   plt.subplot(131)
group_means['Lever Presses'].plot(legend=True, yerr=group_sems['Lever Presses'],
                                  xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Lever Presses')

#   plt.subplot(132)
#   group_means['Lever Press Rate'].plot(legend=True, yerr=group_sems['Lever Press Rate'], xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
#   plt.ylabel('Lever Press Rate (rpm)')

#   plt.subplot(133)
#   group_means['Dippers'].plot(legend=True, yerr=group_sems['Dippers'], ylim=[0, 60],
#                               xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
#   plt.ylabel('Dippers')
#
plt.show()
