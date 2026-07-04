import streamlit as st

st.set_page_config(
    page_title="유튜브 마스터 툴킷",
    page_icon="📺",
    layout="centered"
)

st.title("📺 유튜브 마스터 툴킷에 오신 것을 환영합니다!")
st.markdown("""
이 앱은 YouTube Data API를 활용하여 유튜브 영상의 다양한 정보를 추출하고 분석합니다.
사이드바에서 원하는 기능을 선택해주세요!

### 🌟 주요 기능
1. **🖼️ 썸네일 다운로더**: 영상의 URL만 넣으면 고화질 썸네일을 확인하고 다운로드할 수 있습니다.
2. **💬 댓글 수집 및 분석**: 영상의 댓글을 최대 100개까지 가져와 엑셀(CSV)로 저장하고 간이 분석을 진행합니다.

---
""")

# Secrets 설정 안내 (사용자 확인용)
if "YOUTUBE_API_KEY" not in st.secrets:
    st.error("⚠️ Streamlit Secrets에 'YOUTUBE_API_KEY'가 설정되지 않았습니다. 관자 페이지에서 설정해주세요.")
else:
    st.success("✅ YouTube API 연결 준비 완료!")
