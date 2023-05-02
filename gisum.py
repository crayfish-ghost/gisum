import sys
import argparse
from src import utils
from src import github_api
from src import summarizer

def main(url: str):

    # URLをparseし、APIのURLに変換
    api_url = utils.convert_url_to_api(url)

    # github APIを実行し、issueの議論の概要をjsonで受け取る
    issue_data = github_api.fetch_issue_data(api_url)

    # github APIを実行し、issueの議論のcommentを取得する
    issue_comments = utils.extract_issue_comments(issue_data)

    # まとめたcommentデータをAPI経由でChatGPTに渡し、内容を要約させる
    summarized_text = summarizer.summarize(issue_comments)

    print(summarized_text)
    exit(0)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Issue Summarizer")
    parser.add_argument("url", help="URL of the GitHub issue to summarize")
    args = parser.parse_args()
    main(args.url)
