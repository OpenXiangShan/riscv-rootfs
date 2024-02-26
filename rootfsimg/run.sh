#!/bin/sh
echo '===== Start running SPEC2006 ====='
echo '======== BEGIN mcf ========'
set -x
md5sum /spec/astar_base
date -R
/spec_common/before_workload
cd /spec && ./astar_base BigLakes2048.cfg
date -R
set +x
/spec_common/trap
echo '======== END   mcf ========'
echo '===== Finish running SPEC2006 ====='
