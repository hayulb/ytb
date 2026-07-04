import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import re

st.set_page_config(page_title="유튜브 댓글 수집기", page_icon="💬", layout="wide")

st.title("💬 유튜브 댓글 수집 및 분석기")

# API 키 불러오기
if "YOUTUBE_API_KEY" not in st.secrets:
    st.error("Secrets에 YOUTUBE_API_KEY를 먼저 등록해주세요.")
    st.stop()

api_key = st.secrets["YOUTUBE_API_KEY"]
youtube = build("youtube", "v3", developerKey=api_key)

def get_video_id(url):
    regex = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    return match.group(4) if match else None

# 댓글 수집 함수
def get_youtube_comments(video_id, max_results=100):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response.get("items", []):
            comment_snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "작성자": comment_snippet["authorDisplayName"],
                "댓글 내용": comment_snippet["textDisplay"],
                "좋아요 수": comment_snippet["likeCount"],
                "발행일": comment_snippet["publishedAt"]
            })
        return pd.DataFrame(comments)
    except Exception as e:
        st.error(f"에러가 발생했습니다: {e}")
        return pd.DataFrame()

# UI 구성
video_url = st.text_input("댓글을 추출할 유튜브 URL을 입력하세요:")
max_count = st.slider("가져올 댓글 개수 설정", min_value=20, max_value=100, value=50, step=10)

if st.button("댓글 가져오기 🚀"):
    if video_url:
        video_id = get_video_id(video_url)
        if video_id:
            with st.spinner("유튜브에서 댓글을 열심히 가져오는 중..."):
                df = get_youtube_comments(video_id, max_results=max_count)
                
                if not df.empty:
                    st.success(f"총 {len(df)}개의 댓글을 성공적으로 가져왔습니다!")
                    
                    # 통계치 보여주기
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("총 좋아요 수 합계", int(df["좋아요 수"].sum()))
                    with col2:
                        st.metric("가장 많은 좋아요를 받은 댓글의 좋아요 수", int(df["좋아요 수"].max()))
                    
                    # 데이터프레임 출력
                    st.dataframe(df, use_container_width=True)
                    
                    # CSV 다운로드 버튼
                    csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    st.download_button(
                        label="📥 댓글 데이터 CSV 다운로드",
                        data=csv,
                        file_name=f"youtube_comments_{video_id}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("댓글이 없거나 댓글 기능이 비활성화된 영상입니다.")
        else:
            st.error("유튜브 영상 ID를 추출할 수 없습니다. URL을 확인해주세요.")
    else:
        st.info("URL을 입력하고 버튼을 눌러주세요.")
