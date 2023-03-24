import re
import sys
find_num = re.compile(r'[\d\.]+')
with open(sys.argv[1],'r') as f:
    with open(sys.argv[2],'w') as new_command_f:
        for line in f:
            ops = line.strip().split()
            if len(ops) == 2:
                new_line = f'SET {ops[1]} 1 \n'
                new_command_f.write(new_line)