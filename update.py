import subprocess

def git_pull():
    result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
    print("Git pull output:")
    print(result.stdout)

git_pull()
