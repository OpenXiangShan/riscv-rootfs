#!/bin/sh
echo '===== Start running ====='
echo '======== BEGIN ========'
export LD_LIBRARY_PATH=/lib:$LD_LIBRARY_PATH
set -x
/usr/bin/taskset -c 0 /usr/bin/task0.sh &
PID0=$!
/usr/bin/taskset -c 1 /usr/bin/task1.sh &
PID1=$!
wait $PID0
wait $PID1
echo '======== END ========'
echo '===== Finish running ====='
