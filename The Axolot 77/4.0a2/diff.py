#!/usr/bin/env python3

import argparse
import os
import filecmp
import difflib

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def get_all_files(folder):
    file_set = set()
    for root, _, files in os.walk(folder):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), folder)
            file_set.add(rel_path)
    return file_set

def read_file_lines(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception:
        return []

def print_diff(base_path, comp_path, rel_file):
    base_file = os.path.join(base_path, rel_file)
    comp_file = os.path.join(comp_path, rel_file)
    
    base_lines = read_file_lines(base_file)
    comp_lines = read_file_lines(comp_file)

    diff = difflib.ndiff(base_lines, comp_lines)
    
    for line in diff:
        if line.startswith('- '):
            print(f"    {RED}{line.rstrip()}{RESET}")
        elif line.startswith('+ '):
            print(f"    {GREEN}{line.rstrip()}{RESET}")
        elif line.startswith('? '):
            print(f"    {YELLOW}{line.rstrip()}{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Diff two folders like git.")
    parser.add_argument('-base', required=True, help='Base folder path')
    parser.add_argument('-comp', required=True, help='Comparison folder path')
    args = parser.parse_args()

    base_files = get_all_files(args.base)
    comp_files = get_all_files(args.comp)

    added_files = comp_files - base_files
    removed_files = base_files - comp_files
    common_files = base_files & comp_files

    for file in sorted(added_files):
        print(f"{GREEN}+ {file}{RESET}")
    for file in sorted(removed_files):
        print(f"{RED}- {file}{RESET}")
    for file in sorted(common_files):
        base_file = os.path.join(args.base, file)
        comp_file = os.path.join(args.comp, file)

        if not filecmp.cmp(base_file, comp_file, shallow=False):
            print(f"{YELLOW}• {file}{RESET}")
            print_diff(args.base, args.comp, file)

if __name__ == "__main__":
    main()
