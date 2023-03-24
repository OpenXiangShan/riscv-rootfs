redis-cli -x script load < redislua.lua > 1.tmp
redis-cli evalsha `cat 1.tmp` 0
