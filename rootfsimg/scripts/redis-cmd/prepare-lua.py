import re
import sys
find_num = re.compile(r'[\d\.]+')
with open(sys.argv[1],'r') as f:
    with open(sys.argv[2],'w') as new_command_f:
        for line in f:
            ops = line.strip().split()
            ops = [x if find_num.match(x) else f"'{x}'" for x in ops]
            new_line = 'redis.call(' + ','.join(ops) + ');\n'
            new_command_f.write(new_line)
        new_command_f.write("return 0;")