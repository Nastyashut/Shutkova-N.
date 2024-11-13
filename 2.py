import os 
import signal

N = 10
L = 100
pipes = []
pids = []

for i in range(N):
    pipes.append(os.pipe())
    pid = os.fork()

    if pid == 0:
        # child 
        break
    else:
        pids.append(pid)
else:
    for p in pipes:
        os.close(p[0])
    while s:=input():
        s = s.split()
        c = ord(s[1][0]) % N
        if s[0] == 'load':
            os.write(pipes[c][1], ((L - len(s[1]))* ' ' + s[1]).encode())
        elif s[0] == 'check':
            s = ' '.join(s)
            os.write(pipes[c][1], ((L - len(s)) * ' ' + s).encode())
        elif s[0] == 'kill':
            for p in pids:
                os.kill(p, signal.SIGTERM)
            exit()
        else:   
            raise Exception('Incorrect command')
    exit()

for p in pipes[:-1]:
    os.close(p[0])
    os.close(p[1])
os.close(pipes[-1][1])

reader = os.fdopen(pipes[-1][0])
words = []

# child process
while word := os.read(pipes[-1][0], L).decode().strip():
    word = word.split()
    if len(word) == 2:
        # check 
        print(word[1] in words)
    else:
        words.append(word[0])
