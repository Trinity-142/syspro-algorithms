import subprocess
import sys

path = sys.argv[1]
hash1 = sys.argv[2]
hash2 = sys.argv[3]
command = sys.argv[4]


def check_commit(hash, command):
    global path
    try:
        subprocess.run(["git", "-C", path, "checkout", hash], check=True)
        print(f"Now in commit {hash}")
        code = subprocess.run(command.split(), cwd=path)
        subprocess.run(["git", "-C", path, "clean", "-fd"], check=True)
        return code.returncode
    except subprocess.CalledProcessError:
        print("Commit checking failed")
        return 1


def get_commits_list(hash1, hash2):
    global path
    try:
        rev_list = subprocess.run(["git", "-C", path, "rev-list", "--reverse", f"{hash1}..{hash2}"],
                                  stdout=subprocess.PIPE,
                                  text=True,
                                  check=True)
        commits = rev_list.stdout.strip().split('\n')
        print(f"List of commits from old to new: {commits}")
        return commits
    except subprocess.CalledProcessError:
        print("Failed to get a list of commits")
        return 1


def binary_search_impl(commits: list[str], l: int, r: int, command: str) -> str:
    if r == l:
        return commits[r]
    pivot = (l + r) // 2
    error_code = check_commit(commits[pivot], command)
    if error_code:
        return binary_search_impl(commits, l, pivot, command)
    else:
        return binary_search_impl(commits, pivot + 1, r, command)


def binary_search(commits: list[str], command: str) -> str:
    return binary_search_impl(commits, 0, len(commits) - 1, command)


print(f"A bug first appears in a commit: {binary_search(get_commits_list(hash1, hash2), command)}")
subprocess.run(["git", "-C", path, "checkout", "main"], check=True)
