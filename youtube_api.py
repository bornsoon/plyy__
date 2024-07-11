
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YouTube API 키
API_KEY = 'AIzaSyClYLulYqkFyTNaVdqinymp8q2gqmDU1QE'

# YouTube API 클라이언트 생성
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos(query):
    try:
        # YouTube에서 검색
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=1  # 가져올 결과 수 (최대 50)
        ).execute()

        # 검색 결과에서 비디오 ID 가져오기
        video_id = search_response['items'][0]['id']['videoId']
        
        # 비디오의 URL 생성
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        return video_url
    
    except HttpError as e:
        print('YouTube API request error:', e)

# 'newjeans howseet' 곡의 비디오 URL 가져오기
video_url = search_videos('newjeans howseet')

if video_url:
    print('Found video:', video_url)
else:
    print('Video not found.')

# 위에서 사용한 search_videos 함수를 그대로 가져온다고 가정합니다.

# 'newjeans howseet' 곡의 비디오 ID 가져오기
video_url = search_videos('newjeans howseet')

if video_url:
    video_id = video_url.split('=')[-1]  # 비디오 URL에서 ID 추출
    embed_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1" frameborder="0" allowfullscreen></iframe>'
    # <iframe width="500" height="375" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1" title="100+ (feat. Lil Baby)" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
    
else:
    embed_code = '<p>Video not found.</p>'

# HTML 파일에 쓸 내용
html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Embedded YouTube Video</title>
</head>
<body>
    <h2>YouTube Video</h2>
    {embed_code}
</body>
</html>
'''

# 파일에 쓰기
filename = 'embedded_video.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'HTML 파일 "{filename}"이 생성되었습니다.')
