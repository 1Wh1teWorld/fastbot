from youtubesearchpython import VideosSearch

def generate_most_relevant_url(search_query : str):

    video_search = VideosSearch(search_query, limit=1)
    video_id = video_search.result()["result"][0]["id"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return video_url
    