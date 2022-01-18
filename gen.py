#!/usr/bin/env python3

import os
import sys 
from random import randint, seed
from argparse import ArgumentParser
from zlib import crc32

BLOCK_SIZE = (64 * 1024) - 4

def good(file_path: str):
    with open("/dev/urandom", "rb") as rnd_fd, open(file_path, "wb") as trgt_fd:
        for i in range(1,50):
            data = rnd_fd.read(BLOCK_SIZE)
            checksum = crc32(data) & 0xffffffff
            trgt_fd.write(data)
            trgt_fd.write(checksum.to_bytes(4, byteorder=sys.byteorder, signed=False))
        os.fsync(trgt_fd.fileno())


def bad(file_path: str):
    bad_blocks = set([randint(10, 40) for i in range(1,10)])
    with open("/dev/urandom", "rb") as rnd_fd, open(file_path, "wb") as trgt_fd:
        for i in range(1,50):
            data = rnd_fd.read(BLOCK_SIZE)
            checksum = crc32(data) & 0xffffffff
            if i in bad_blocks:
                checksum += 10
            trgt_fd.write(data)
            trgt_fd.write(checksum.to_bytes(4, byteorder=sys.byteorder, signed=False))
        os.fsync(trgt_fd.fileno())


def empty(file_path: str):
    with open(file_path, "wb") as trgt_fd:
        os.fsync(trgt_fd.fileno())


def size(file_path: str):
    with open("/dev/urandom", "rb") as rnd_fd, open(file_path, "wb") as trgt_fd:
        for i in range(1,50):
            block_size = BLOCK_SIZE - randint(1024, 24 * 1024)
            data = rnd_fd.read(block_size)
            checksum = crc32(data) & 0xffffffff
            trgt_fd.write(data)
            trgt_fd.write(checksum.to_bytes(4, byteorder=sys.byteorder, signed=False))
        os.fsync(trgt_fd.fileno())


def main():
    parser = ArgumentParser()
    parser.add_argument('--type', type=str, help='Generated file type (good, bad, empty, part).')
    args = parser.parse_args()

    seed()

    types = {
        'good': good,
        'bad': bad,
        'empty': empty,
        'size': size,
    }[args.type](f'./files/{args.type}.dat')

if __name__ == '__main__':
    main()
