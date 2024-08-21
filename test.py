import os
import requests
import json
api_key = "da1f20fa26ff33bf88deec61ff67c743.hpZFBH5QWUev0kXZ"

def check_code_changes(before_code, after_code):
    # 设置请求的URL
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 设置请求体
    data = {
        "model": "codegeex-4",
        "messages": [
            {
                "role": "system",
                "content": "Please check the code changes below. If there are any areas that need improvement, please generate a comment. If there are no issues, please return 'pass'."
            },
            {
                "role": "user",
                "content": f"before:\n{before_code}\nAfter:\n{after_code}"
            }
        ],
        "top_p": 0.7,
        "temperature": 0.9,
        "max_tokens": 1024,
        "stop": ["", "", "", ""]
    }
    
    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    return response_dict["choices"][0]['message']['content']

token = os.getenv("GIT_TOKEN")
repo = 'AndongWang/test-wca'
pr_number = 4

print(token)
print(repo)
print(pr_number)
# GitHub API 基本信息
api_url = f"https://api.github.com/repos/{repo}"
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# 获取PR中的更改文件列表
files_url = f"{api_url}/pulls/{pr_number}/files"
response = requests.get(files_url, headers=headers)

if response.status_code != 200:
    print(f"Error fetching PR files: {response.status_code} {response.text}")
    response.raise_for_status()


files = response.json()
print(files)

# 获取最新的 commit_id
pr_url = f"{api_url}/pulls/{pr_number}"
pr_response = requests.get(pr_url, headers=headers)

if pr_response.status_code != 200:
    print(f"Error fetching PR details: {pr_response.status_code} {pr_response.text}")
    pr_response.raise_for_status()

try:
    pr_details = pr_response.json()
    commit_id = pr_details['head']['sha']
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    print(f"Response content: {pr_response.text}")
    raise


for file in files:
    filename = file['filename']
    before_code = ""
    after_code = ""
    old_lines = []
    new_lines = []
    
    for change in file['patch'].split('\n'):
        if change.startswith('@@'):
            parts = change.split(' ')
            old_part = parts[1]
            new_part = parts[2]
            
            old_start_line = int(old_part.split(',')[0][1:])
            new_start_line = int(new_part.split(',')[0][1:])
        elif change.startswith('-'):
            old_lines.append(change[1:])
            before_code += change[1:] + "\n"
        elif change.startswith('+'):
            new_lines.append(change[1:])
            after_code += change[1:] + "\n"
        else:
            old_lines.append(change)
            new_lines.append(change)
            before_code += change + "\n"
            after_code += change + "\n"

    # 调用生成评论的API
    try:
        response = check_code_changes(before_code, after_code)
    except Exception as e:
        print(f"Error checking code changes for file {filename}: {e}")
        continue
    
    comment_body = response

    # 添加评论
    comment_url = f"{api_url}/pulls/{pr_number}/comments"
    comment_data = {
        "body": comment_body,
        "path": filename,
        "commit_id": commit_id,
        "line": new_start_line,  # 使用 line 而不是 position
        "side": "RIGHT"
    }
    
    comment_response = requests.post(comment_url, json=comment_data, headers=headers)
    
    if comment_response.status_code != 201:
        print(f"Error posting comment for file {filename}: {comment_response.status_code} {comment_response.text}")
