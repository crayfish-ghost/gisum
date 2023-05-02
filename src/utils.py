import re, os, json
from urllib.parse import urlparse, urlunparse
from .tokenizer import get_token_num
from .read_config import config
from typing import Dict, List

def convert_url_to_api(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL")

        if "github.com" not in parsed_url.netloc:
            raise ValueError("Not a GitHub URL")

        path = re.sub(r"^/*", "", parsed_url.path)  # Remove leading slashes
        path_parts = path.split("/")
        if len(path_parts) < 4 or path_parts[2] != "issues":
            raise ValueError("Not a GitHub Issue URL")

        api_url = urlunparse(("https", "api.github.com", f"repos/{path_parts[0]}/{path_parts[1]}/issues/{path_parts[3]}", "", "", ""))
        return api_url
    except ValueError as e:
        print(f"Error converting URL: {str(e)}")
        raise

def extract_issue_comments (issue_data: Dict) -> str:
    #issue_json_text = json.dumps(issue_data)
    summary = issue_data["summary"]
    pages = issue_data["pages"]
    comments = []
    comments.append(' Title:"{title}", issue_id:{iid}, state:"{state}"'.format(title=summary["title"],
                                                                          iid=summary["id"],
                                                                          state=summary["state"]))
    comments.append("\n\n Issue describe:" + summary["body"] + "\n\n")

    for page in pages:
        for comment in page:
            text = ""
            comment["body"] = re.sub(r'\n\s*\n', '\n', comment["body"])

            #1つのコメントがpromptとして長くなりすぎる場合は要約対象から外す
            if get_token_num(comment["body"]) > config.getint('other','comment_token_limit'):
                print("Sorry this comment is too long, eliminated:\n{url}".format(url=comment["html_url"]))
                continue
            
            line_head=" User:{user}, created_at:{created_at}\n".format(user=comment["user"]["login"]
                                                             ,created_at=comment["created_at"])
            line_body=" Comment:{body}\n\n".format(body=comment["body"])
            comments.append(line_head + line_body)

    return comments

