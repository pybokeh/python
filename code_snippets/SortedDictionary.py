myhash = {1:'John', 4:'Dick', 3:'Bill', 2:'Alex'}

for score in sorted(myhash.keys(), reverse=True):
    print myhash[score] + ' ' + str(score)
