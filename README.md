# Intelligent-Alarm-Sensitivity-for-ZBJ.com
This project is built for ZBJ Network Co., Ltd. to adjust DevOps system alarm thresholds with intelligent sensitivity.

The alarm distribution regression model is built by Savitzky-Golay Convolution Algorithm.

To run this project, please ask ZBJ Network Co., Ltd. for permission, then:

Step 1: Update server url authorized by ZBJ Network Co., Ltd. in threshold.py and time.py.

Step 2: Execute threshold.py to obtain the real-time data needed to calculate the performance thresholds.

Step 3: Execute threshold_result.py to obtain the dynamic performance thresholds.

Step 4: Execute time.py to obtain the data needed to calculate the time thresholds to trigger the alarm.

Step 5: Execute time_result.py to obtain the dynamic time thresholds.
