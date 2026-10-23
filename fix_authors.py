import os
import subprocess
import sys

OLD_EMAIL = "allaanilkumar56@gmail.com"
NEW_NAME = "Alla Poojitha"
NEW_EMAIL = "allapoojitha123@gmail.com"

def git(*args, env=None, input_text=None):
    result = subprocess.run(
        ["git", *args],
        env=env,
        input=input_text,
        text=True,
        capture_output=True
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.rstrip("\n")

def field(commit, fmt):
    return git("show", "-s", f"--format={fmt}", commit)

try:
    branch = git("branch", "--show-current")
    if branch != "main":
        raise RuntimeError("Please switch to main before running this script.")

    if git("status", "--porcelain"):
        raise RuntimeError("Working tree is not clean. Stop and check your changes.")

    old_tip = git("rev-parse", "main")
    commits = git("rev-list", "--reverse", "main").splitlines()

    # Keep a separate backup of the current main branch.
    backup = "backup-before-author-fix-python"
    suffix = 1
    while subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{backup}"]
    ).returncode == 0:
        suffix += 1
        backup = f"backup-before-author-fix-python-{suffix}"

    git("branch", backup, "main")
    print(f"Backup created: {backup}")

    new_parent = None

    for old_commit in commits:
        parents = field(old_commit, "%P").split()
        if len(parents) > 1:
            raise RuntimeError(
                f"Merge commit detected ({old_commit}). Backup exists; stopping safely."
            )

        tree = field(old_commit, "%T")
        author_name = field(old_commit, "%an")
        author_email = field(old_commit, "%ae")
        author_date = field(old_commit, "%aI")
        committer_name = field(old_commit, "%cn")
        committer_email = field(old_commit, "%ce")
        committer_date = field(old_commit, "%cI")
        message = git("show", "-s", "--format=%B", old_commit)

        if author_email.lower() == OLD_EMAIL.lower():
            author_name, author_email = NEW_NAME, NEW_EMAIL
        if committer_email.lower() == OLD_EMAIL.lower():
            committer_name, committer_email = NEW_NAME, NEW_EMAIL

        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": author_name,
            "GIT_AUTHOR_EMAIL": author_email,
            "GIT_AUTHOR_DATE": author_date,
            "GIT_COMMITTER_NAME": committer_name,
            "GIT_COMMITTER_EMAIL": committer_email,
            "GIT_COMMITTER_DATE": committer_date,
        })

        args = ["commit-tree", tree]
        if new_parent:
            args.extend(["-p", new_parent])

        new_parent = git(*args, env=env, input_text=message + "\n")
        print(f"Rebuilt {old_commit[:8]} -> {new_parent[:8]}")

    # Move main only after all commits were rebuilt successfully.
    git("update-ref", "refs/heads/main", new_parent, old_tip)
    print("\nSUCCESS: Local main history has been rewritten.")
    print(f"Backup branch: {backup}")
    print("Verify the author names before pushing to GitHub.")

except Exception as exc:
    print(f"\nSTOPPED: {exc}")
    print("Do not push. Your original main reference was not intentionally updated on failure.")
    sys.exit(1)
