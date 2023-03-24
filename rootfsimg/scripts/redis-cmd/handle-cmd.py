with open('user-timeline-run-redis.cmd','r') as f:
    with open('user-timeline-RANGE.cmd','w') as new_command_f:
        f.readline()
        for line in f:
            si = line.index(']')
            new_line = line[si+1:]
            ops = new_line.strip().split()
            ops = [x.strip('"').replace("key:","") for x in ops]
            new_line = ' '.join(ops) + '\n'
            new_command_f.write(new_line)

