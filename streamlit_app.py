import streamlit as st
from openai import OpenAI

def rfile(name_file):
 with open(name_file, "r", encoding="utf-8") as file:
    content_sys = file.read()
    return content_sys

# # Hiển thị logo ở trên cùng, căn giữa
# col1, col2, col3 = st.columns([3, 2, 3])
# with col2:
#     st.image("logo.png", use_container_width=True)  # Thay use_column_width bằng use_container_width


try:
    # Hiển thị logo ở trên cùng, căn giữa
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)  # Thay use_column_width bằng use_container_width
except:
    pass


# Tùy chỉnh nội dung tiêu đề
title_content = rfile("00.xinchao.txt")

# Hiển thị tiêu đề với nội dung tùy chỉnh
st.markdown(
    f"""
    <h1 style="text-align: center; font-size: 24px;">{title_content}</h1>
    """,
    unsafe_allow_html=True
)

# Lấy OpenAI API key từ `st.secrets`.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

#1

# Tạo OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Khởi tạo lời nhắn "system" để định hình hành vi mô hình.
INITIAL_SYSTEM_MESSAGE = {
    "role": "system",
    "content":rfile("01.system_trainning.txt") ,
}

# Khởi tạo lời nhắn ví dụ từ vai trò "assistant".
INITIAL_ASSISTANT_MESSAGE = {
    "role": "assistant",
    "content":rfile("02.assistant.txt"),
}

# # Khởi tạo lời nhắn ví dụ từ vai trò "user".
# INITIAL_USER_MESSAGE = {
#     "role": "user",
#     "content": (
#         "Xin chào trợ lý Anh Lập Trình ! Tôi muốn tìm hiểu thêm về cách sử dụng dịch vụ của bạn. "
#         "Bạn có thể giúp tôi được không?"
#     ),
# }

# Tạo một biến trạng thái session để lưu trữ các tin nhắn nếu chưa tồn tại.
if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# Loại bỏ INITIAL_SYSTEM_MESSAGE khỏi giao diện hiển thị.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Tạo ô nhập liệu cho người dùng.
if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):

    # Lưu trữ và hiển thị tin nhắn của người dùng.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tạo phản hồi từ API OpenAI.
    stream = client.chat.completions.create(
        model = rfile("module_chatgpt.txt").strip(),
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Hiển thị và lưu phản hồi của trợ lý.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


#####