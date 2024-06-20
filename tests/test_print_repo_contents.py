import pytest
import requests
import time
from unittest.mock import patch
from src.print_repo_contents import get_all_files, display_files_as_tree

# Mock data for testing
mock_tree = [
    {"path": "file1.txt", "type": "blob"},
    {"path": "folder1/file2.txt", "type": "blob"},
    {"path": "folder1/folder2/file3.txt", "type": "blob"},
]

# Test for get_all_files function
@patch('requests.get')
def test_get_all_files(mock_get):
    # Define the mock response object
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"tree": mock_tree}
    
    repo_owner = "octocat"
    repo_name = "Hello-World"
    branch = "main"
    token = None

    file_paths = get_all_files(repo_owner, repo_name, branch, token)

    assert file_paths == ["file1.txt", "folder1/file2.txt", "folder1/folder2/file3.txt"]

# Test for handling rate limit in get_all_files function
@patch('requests.get')
def test_get_all_files_rate_limit(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 403
    mock_response.headers = {
        'X-RateLimit-Remaining': '0',
        'X-RateLimit-Reset': str(int(time.time()) + 1)
    }
    mock_response.json.return_value = {}

    repo_owner = "octocat"
    repo_name = "Hello-World"
    branch = "main"
    token = None

    with patch('time.sleep', return_value=None):
        with pytest.raises(Exception):
            get_all_files(repo_owner, repo_name, branch, token)

# Test for display_files_as_tree function
def test_display_files_as_tree(capsys):
    file_paths = ["file1.txt", "folder1/file2.txt", "folder1/folder2/file3.txt"]
    display_files_as_tree(file_paths)
    
    captured = capsys.readouterr()
    output = captured.out

    expected_output = (
        "├── file1.txt\n"
        "└── folder1\n"
        "    ├── file2.txt\n"
        "    └── folder2\n"
        "        └── file3.txt\n"
        "\nTotal number of files: 3\n"
    )

    assert output == expected_output

if __name__ == "__main__":
    pytest.main()
