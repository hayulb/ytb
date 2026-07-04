import streamlit as st
import re

st.set_page_config(page_title="유튜브 썸네일 다운로더", page_icon="🖼️")

st.title("🖼️ 유튜브 썸네일 다운로더")
st.write("유튜브 영상 링크를 입력하면 다양한 화질의 썸네일을 가져옵니다.")

# 유튜브 링크에서 영상 ID 추출하는 함수
def get_video_id(url):
    regex = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(4)
    return None

video_url = st.text_input("유튜브 영상 URL을 입력하세요:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    video_id = get_video_id(video_url)
    
    if video_id:
        st.success(f"영상 ID 추출 성공: {video_id}")
        
        # 고화질 썸네일 URL 생성
        max_res_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        hq_res_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        
        st.subheader("📸 최고화질 썸네일 (Max Resolution)")
        st.image(max_res_url, use_container_width=True)
        st.caption(f"이미지 주소: {max_res_url}")
        
        st.subheader("📸 표준 고화질 썸네일 (HQ Default)")
        st.image(hq_res_url, width=480)
        
    else:
        st.error("올바른 유튜브 URL 형식이 아닙니다. 다시 확인해주세요.")
