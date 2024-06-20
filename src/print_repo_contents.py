import requests
import time


def get_all_files(repo_owner, repo_name, branch="main", token=None):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/" \
          f"{branch}?recursive=1"
    headers = {"Authorization": f"token {token}"} if token else {}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tree = response.json().get("tree", [])
        file_paths = [item["path"] for item in tree if item["type"] == "blob"]
        return file_paths
    elif (
        response.status_code == 403
        and "X-RateLimit-Remaining" in response.headers
        and int(response.headers["X-RateLimit-Remaining"]) == 0
    ):
        # Handle rate limit
        reset_time = int(response.headers["X-RateLimit-Reset"])
        wait_time = max(reset_time - time.time(), 0)
        print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
        time.sleep(wait_time)
        return get_all_files(repo_owner, repo_name, branch, token)
    else:
        raise Exception(
            f"Failed to retrieve files: \n"
            f"{response.status_code} - {response.text}"
        )


def display_files_as_tree(file_paths):
    file_paths.sort()
    tree = {}
    for path in file_paths:
        parts = path.split("/")
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    def print_tree(current_level, indent=""):
        keys = sorted(current_level.keys())
        file_count = 0
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                print(f"{indent}└── {key}")
                next_indent = indent + "    "
            else:
                print(f"{indent}├── {key}")
                next_indent = indent + "│   "
            if current_level[key]:  # It's a directory
                file_count += print_tree(current_level[key], next_indent)
            else:  # It's a file
                file_count += 1
        return file_count

    total_files = print_tree(tree)
    print(f"\nTotal number of files: {total_files}")


def main():
    repo_owner = input("Enter the GitHub repository owner: ")
    repo_name = input("Enter the GitHub repository name: ")
    branch = (
        input("Enter the branch to retrieve files from (default: main): ")
        or "main"
    )
    token = input("Enter your personal access token (optional): ")

    try:
        file_paths = get_all_files(repo_owner, repo_name, branch, token)
        display_files_as_tree(file_paths)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
