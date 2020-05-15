#!/usr/bin/python3


import sys
import subprocess
import time


IPFS = 'ipfs --api /ip4/127.0.0.1/tcp/5001'


def ipfs_recur_listing(pth):
    try:
        out = subprocess.check_output('%s ls --size=false %s' % (IPFS, pth), shell=True, universal_newlines=True)
    except:
        return None
    for line in out.split('\n'):
        if not line:
            continue
        cid, name = line.split()
        if name.endswith('/'):
            for cid_, name_ in ipfs_recur_listing('%s/%s' % (pth, name)):
                yield cid_, '%s%s' % (name, name_)
        else:
            yield cid, name


def ipfs_cat_dev_null(pth):
    subprocess.check_call('%s cat %s >/dev/null' % (IPFS, pth), shell=True)


def main():
    pths = sys.argv[1:]
    first_run = 1
    cids = set()
    while 1:
        for pth in pths:
            print(pth)
            t_begin = time.time()
            lst = ipfs_recur_listing(pth)
            t_end = time.time()
            print('listing took %ss' % (t_end - t_begin, ))
            if lst is None:
                print('err')
                continue
            for cid, name in lst:
                if cid in cids:
                    continue
                print(cid, name)
                if not first_run:
                    print('>')
                    ipfs_cat_dev_null(cid)
                    print('!')
                cids.add(cid)
        if first_run:
            print('first run done')
        first_run = 0
        print('zzz')
        time.sleep(600)  # TODO: hard-coded shit
    return 0


if __name__ == '__main__':
    sys.exit(main())
