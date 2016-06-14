import re
import json
import sys
import os
import apt
from prettytable import PrettyTable
# example: [I 06-08 07:17:42.059 core:117] dde-control-center updated version 3.0.13
r = re.compile("\[.+\] (.+) updated version (.+)")
nv_list = []
nt_list = []
cache = apt.Cache()
x = PrettyTable(["Name", "Tag", "Version in Repo"])
def filter_output(file_path):
    with open(file_path) as fp:
        while True:
            line = fp.readline()
            if not len(line):
                break
            if not line.startswith("["):
                continue

            l = r.findall(line)
            filter_tuple = l[0]
            name = filter_tuple[0]
            version = filter_tuple[1]
            nv_dict = {
                    "name" : name,
                    "tag" : version
                    }
            nv_list.append(nv_dict)
def compare_repo():
    for dict in nv_list:
        pkg = cache[dict['name']]
        version = pkg.versions[0].version
        if '-' in version:
            version = version.rsplit('-', 1)[0]
        if version != dict['tag']:
            #print(version)
            dict['version_in_repo']=version
            #print('package %s has a new tag %s, version in repo is %s' % (dict['name'], dict['tag'], dict['version_in_repo']))
            x.add_row([dict['name'], dict['tag'], dict['version_in_repo']])
            nt_list.append(dict)
if __name__ == "__main__":
    file_path = sys.argv[1]
    filter_output(file_path)
    compare_repo()
    print(x)
    with open('result.json', 'w') as fp:
        json.dump(nt_list, fp)

