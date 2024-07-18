import os
import requests
import json

# 获取环境变量
# token = os.getenv('GITHUB_TOKEN')
# repo = os.getenv('GITHUB_REPOSITORY')
# pr_number = os.getenv('GITHUB_REF').split('/')[-1]

repo = "WCA-2024-tony-team"

# GitHub API 基本信息
api_url = f"https://github.ibm.com/repos/{repo}"
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# 获取PR中的更改文件列表
files_url = f"{api_url}/pulls/{pr_number}/files"
response = requests.get(files_url, headers=headers)
files = response.json()

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
    
    # 返回响应内容
    return response.json()

# 处理每个文件的更改
for file in files:
    filename = file['filename']
    before_code = ""
    after_code = ""
    old_lines = []
    new_lines = []
    
    for change in file['patch'].split('\n'):
        if change.startswith('@@'):
            # 解析更改的范围
            parts = change.split(' ')
            old_part = parts[1]
            new_part = parts[2]
            
            # 获取行号范围
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
    response = check_code_changes(before_code, after_code)
    comment_body = response.get('choices', [{}])[0].get('message', {}).get('content', '这里的更改需要注意。')

    # 添加评论
    comment_url = f"{api_url}/pulls/{pr_number}/comments"
    comment_data = {
        "body": comment_body,
        "path": filename,
        "position": new_start_line
    }
    requests.post(comment_url, json=comment_data, headers=headers)

