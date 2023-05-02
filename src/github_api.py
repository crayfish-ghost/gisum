import requests, json, sys, math, os
from typing import Dict, List

#for debug
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def fetch_issue_summary(api_url: str) -> Dict:
    #return read_json_file("~/gisum/dummy_data/summary.json") #for debug

    try:
        response = requests.get(api_url, headers={'Accept': 'application/vnd.github+json'})

        # Check if the response is not successful (HTTP status code is not 2xx)
        if not response.ok:
            raise requests.exceptions.RequestException(f"GitHub API request failed: {response.status_code} - {response.text}")

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issue data: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise

def fetch_issue_pages(summary: dict) -> Dict:
    
    per_page = 100
    page_max = math.ceil(summary["comments"]/per_page) + 1
    responses = []

    #responses.append(read_json_file("~/gisum/dumy_data/comment.json")) #for debug
    #return responses #for debug

    for page in list(range(1, page_max) ):
        try:
            response = requests.get(summary['comments_url']
                                    ,headers={'Accept': 'application/vnd.github+json'
                                              ,"Authorization": "token " + os.environ.get("GITHUB_API_KEY")}
                                    ,params={'per_page': per_page, 'page': page})
            if not response.ok:
                raise requests.exceptions.RequestException(f"GitHub API request failed: {response.status_code} - {response.text}")

            responses.append(response.json())
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issue data: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise
    return responses

def fetch_issue_data(api_url: str) -> Dict:
    issue_summary = fetch_issue_summary(api_url)

    if issue_summary['comments'] < 1:
        print("issueにコメントがありません")
        sys.exit()
    issue_pages = fetch_issue_pages(issue_summary)

    return { 'summary': issue_summary,
             'pages': issue_pages
            }
