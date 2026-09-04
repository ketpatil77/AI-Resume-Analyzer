import argparse
import re
import subprocess
import sys


def package_name(requirement):
    requirement = requirement.split('#', 1)[0].strip()
    if not requirement:
        return None
    return re.split(r'[<>=!~;\[\s]', requirement, maxsplit=1)[0].strip() or None


def run(args, quiet=False):
    kwargs = {'text': True}
    if quiet:
        kwargs.update({'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL})
    return subprocess.run(args, **kwargs).returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('requirements')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()

    missing = []
    with open(args.requirements, encoding='utf-8') as file:
        for line in file:
            requirement = line.split('#', 1)[0].strip()
            name = package_name(requirement)
            if not name:
                continue

            if run([sys.executable, '-m', 'pip', 'show', name], quiet=True) == 0:
                if not args.check:
                    print(f'✓ {name} already installed')
                continue

            missing.append(requirement)
            if args.check:
                continue

            print(f'↓ Installing {requirement}...')
            if run([sys.executable, '-m', 'pip', 'install', requirement]) != 0:
                print(f'Dependency install failed: {requirement}', file=sys.stderr)
                return 1

    return 1 if args.check and missing else 0


if __name__ == '__main__':
    raise SystemExit(main())
