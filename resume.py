import openai
import os
import streamlit as st

# 设置OpenAI API密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

# 获取用户输入的个人资料和工作描述
def get_user_input():
    name = st.text_input("请输入您的名字：")
    email = st.text_input("请输入您的电子邮件地址：")
    phone = st.text_input("请输入您的电话号码：")
    job_title = st.text_input("请输入您要申请的职位：")
    job_description = st.text_area("请输入职位描述：")
    return name, email, phone, job_title, job_description

# 使用OpenAI API生成求职信
def generate_cover_letter(name, email, phone, job_title, job_description, summary_length, tone):
    prompt = (f"写一封给{job_title}的求职信。"
              f"我的名字是{name}，我的联系方式是电子邮件{email}和电话号码{phone}。"
              f"职位描述：{job_description}\n"
              f"请使用{tone}语气撰写求职信，并在摘要中包含{summary_length}个字。")
    
    # 使用OpenAI的GPT-3生成文本
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # 从OpenAI响应中提取生成的文本
    cover_letter = response.choices[0].text

    # 提取摘要
    summary = openai.Completion.create(
        engine="davinci",
        prompt=cover_letter,
        max_tokens=summary_length,
        temperature=0.5,
    ).choices[0].text
    
    return summary

# 主要的Streamlit应用程序
def main():
    st.title("求职信生成器")
    name, email, phone, job_title, job_description = get_user_input()
    if st.button("生成求职信"):
        summary_length = st.slider("请设置摘要长度", 50, 500, 200)
        tone = st.selectbox("请选择求职信的语气", ("正式", "友好", "幽默"))
        summary = generate_cover_letter(name, email, phone, job_title, job_description, summary_length, tone)
        st.write("生成的摘要：")
        st.write(summary)
        save = st.button("保存到文件")
        if save:
            with open(f"{name}-CoverLetter.txt", "w") as f:
                f.write(summary)
            st.write("文件已保存！")

if __name__ == "__main__":
    main()

