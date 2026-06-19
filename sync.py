"""LOCAL: pull the latest schedule.xlsx from GitHub so local statuses match the cloud worker."""
import subprocess
import sys

XLSX = "schedule.xlsx"


def run_git(args):
    """Run a git command, print the command + its output, return CompletedProcess."""
    print(f"$ {' '.join(args)}")
    proc = subprocess.run(args, capture_output=True, text=True)
    out = (proc.stdout or "").rstrip()
    err = (proc.stderr or "").rstrip()
    if out:
        print(out)
    if err:
        print(err)
    return proc


def main():
    # 1. Warn if schedule.xlsx is open/locked
    print("[1/4] Checking if schedule.xlsx is open/locked...")
    try:
        # Opening for append needs a write lock; Excel holds one while the file is open.
        with open(XLSX, "a"):
            pass
        print("      OK, file is not locked.")
    except PermissionError:
        print("Close schedule.xlsx in Excel first, then re-run sync.py")
        sys.exit(1)
    except FileNotFoundError:
        print("      Note: schedule.xlsx not found locally yet; the pull will fetch it.")

    # 2. Fetch
    print("\n[2/4] Fetching latest from origin/main...")
    fetch = run_git(["git", "fetch", "origin", "main"])
    if fetch.returncode != 0:
        print("ERROR: git fetch failed (see output above). Check your internet/remote.")
        sys.exit(1)

    # 3. Check for uncommitted local changes to schedule.xlsx
    print("\n[3/4] Checking for uncommitted local edits to schedule.xlsx...")
    status = run_git(["git", "status", "--porcelain", XLSX])
    if status.returncode != 0:
        print("ERROR: git status failed (see output above).")
        sys.exit(1)
    if status.stdout.strip():
        print("\nYou have local edits not yet pushed. If you continue, pulling may "
              "conflict. Recommend: run push.py first, OR discard local edits.")
        sys.exit(1)
    print("      Clean — no uncommitted changes to schedule.xlsx.")

    # 4. Pull
    print("\n[4/4] Pulling latest from origin/main...")
    pull = run_git(["git", "pull", "origin", "main"])
    combined = (pull.stdout + pull.stderr).lower()

    # 6. Merge conflict?
    if "conflict" in combined or "merge conflict" in combined:
        print("\nMerge conflict on schedule.xlsx. The cloud and your local copy both "
              "changed it. Easiest fix: tell Claude and we'll resolve it.")
        sys.exit(1)

    if pull.returncode != 0:
        print("\nERROR: git pull failed (see output above).")
        sys.exit(1)

    # 5. Success
    print("\nSYNC COMPLETE — your schedule.xlsx is now up to date. You can edit it now.")


if __name__ == "__main__":
    main()
