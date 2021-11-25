import os
import sys
import unittest
from importlib import import_module


EXCLUDED_FILES = ["__main__.py", "config.ini"]


def bold(string):
    return f"\033[1m{string}\033[0m"


def run_all_unittests():
    filepath_relative = __file__
    dirpath = os.path.dirname(os.path.realpath(__file__))
    totalrun = errors = failures = 0
    for filename in os.listdir(dirpath):
        filepath = f"tests/{filename}"
        if filename.lower() in [excl.lower() for excl in EXCLUDED_FILES] or not os.path.isfile(filepath) or ".py" not in filename:
            continue
        filename = filename.strip(".py")
        print(bold("=" * 80))
        print(bold(filename))
        print()
        import_module(filename)
        result = unittest.main(module=filename, exit=False, verbosity=2).result
        totalrun += result.testsRun
        errors += len(result.errors)
        failures += len(result.failures)
        print(bold("=" * 80))
        print("\n" * 4)
    print(bold(f"Run: {totalrun}\nFailures: {failures}\nErrors: {errors}\n"))


if __name__ == "__main__":
    run_all_unittests()

