import os
import random
import subprocess
from datetime import datetime, timedelta

def get_positive_int(prompt, default=20):
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_repo_path(prompt, default="."):
    while True:
        user_input = input(f"{prompt} (default current directory): ")
        if not user_input.strip():
            return default
        if os.path.isdir(user_input):
            return user_input
        else:
            print("Directory does not exist. Please enter a valid path.")

def get_filename(prompt, default="data.txt"):
    user_input = input(f"{prompt} (default {default}): ")
    if not user_input.strip():
        return default
    return user_input

def random_date_in_last_year():
    today = datetime.now()
    start_date = today - timedelta(days=365)
    random_days = random.randint(0, 364)
    random_seconds = random.randint(0, 23*3600 + 3599)
    commit_date = start_date + timedelta(days=random_days, seconds=random_seconds)
    return commit_date

def get_recent_date(is_yesterday):
    today = datetime.now()
    if is_yesterday:
        target_date = today - timedelta(days=1)
        max_seconds = 23*3600 + 3599
    else:
        target_date = today
        max_seconds = today.hour * 3600 + today.minute * 60 + today.second
        if max_seconds <= 0:
            max_seconds = 1
            
    random_seconds = random.randint(0, max_seconds)
    start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_day + timedelta(seconds=random_seconds)

def get_date_mode():
    print("\nChoose commit date range:")
    print("1. Random dates in the last year")
    print("2. Yesterday and Today")
    while True:
        choice = input("Enter choice (1 or 2) [default 2]: ")
        if not choice.strip() or choice == '2':
            return 2
        elif choice == '1':
            return 1
        else:
            print("Invalid choice.")

def make_commit(date, repo_path, filename, message="graph-greener!"):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")
    subprocess.run(["git", "add", filename], cwd=repo_path)
    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def main():
    print("="*60)
    print("🌱 Welcome to graph-greener - GitHub Contribution Graph Commit Generator 🌱")
    print("="*60)
    print("This tool will help you fill your GitHub contribution graph with custom commits.\n")

    mode = get_date_mode()
    num_commits = get_positive_int("How many commits do you want to make", 20)
    repo_path = get_repo_path("Enter the path to your local git repository", ".")
    filename = get_filename("Enter the filename to modify for commits", "data.txt")

    print(f"\nMaking {num_commits} commits in repo: {repo_path}\nModifying file: {filename}\n")

    for i in range(num_commits):
        if mode == 1:
            commit_date = random_date_in_last_year()
        else:
            commit_date = get_recent_date(is_yesterday=(i % 2 == 0))
            
        print(f"[{i+1}/{num_commits}] Committing at {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
        make_commit(commit_date, repo_path, filename)

    print("\nPushing commits to your remote repository...")
    subprocess.run(["git", "push"], cwd=repo_path)
    print("✅ All done! Check your GitHub contribution graph in a few minutes.\n")
    print("Tip: Use a dedicated repository for best results. Happy coding!")

if __name__ == "__main__":
    main()