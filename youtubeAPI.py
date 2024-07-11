from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# API 키 설정
API_KEY = 'AIzaSyClYLulYqkFyTNaVdqinymp8q2gqmDU1QE'

# YouTube Data API 클라이언트 빌드
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 검색할 쿼리 설정
search_query = '뉴진스 - howsweet 뮤직비디오'

try:
    # YouTube에서 비디오 검색
    search_response = youtube.search().list(
        q=search_query,
        part='id',
        type='video'
    ).execute()

    # 첫 번째 비디오 ID 가져오기
    video_id = search_response['items'][0]['id']['videoId']

    # 비디오 링크 생성
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    print('검색 결과:', video_url)

except HttpError as e:
    print('YouTube API 호출 오류 발생:', e)