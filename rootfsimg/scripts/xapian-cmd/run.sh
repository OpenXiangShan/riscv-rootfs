# Set this to point to the top level of the TailBench data directory
DATA_ROOT=/root/xapian/data

# This location is used by applications to store scratch data during execution.
SCRATCH_DIR=/root/

NSERVERS=1
QPS=500
WARMUPREQS=1000
REQUESTS=3000

TBENCH_QPS=${QPS} TBENCH_MAXREQS=${REQUESTS} TBENCH_WARMUPREQS=${WARMUPREQS} \
       TBENCH_RANDSEED=123 \
       TBENCH_MINSLEEPNS=100000 TBENCH_TERMS_FILE=${DATA_ROOT}/terms.in \
       chrt -r 99 ./xapian_integrated -n ${NSERVERS} -d ${DATA_ROOT}/wiki -r 1000000000