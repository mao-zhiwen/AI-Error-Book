import streamlit as st
from llm_core import ai_chat
from db_model import add_error, get_all_errors, delete_error

# 页面配置（更精美的设置）
st.set_page_config(
    page_title="AI智能错题本",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式（让界面更好看）
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #ecfdf5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #fef2f2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-header">📚 AI智能错题本</div>', unsafe_allow_html=True)
st.markdown("基于字节跳动豆包大模型，帮你高效整理错题、分析错误原因")
st.divider()

# 侧边栏功能菜单
with st.sidebar:
    st.header("功能菜单")
    menu = st.radio(
        "选择功能",
        ["录入错题", "查看错题本", "知识点总结", "生成练习题"]
    )
    st.divider()
    st.caption("暑假实训项目 | 豆包大模型版")

# 1. 录入错题功能
if menu == "录入错题":
    st.markdown('<div class="sub-header">📝 录入新错题</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox(
            "选择学科",
            ["数学", "语文", "英语", "物理", "化学", "生物", "历史", "地理", "政治", "其他"]
        )
        question = st.text_area("题目内容", height=150, placeholder="请输入完整的题目内容")
        wrong_answer = st.text_area("你的错误答案", height=100, placeholder="输入你当时做错的答案")
    
    with col2:
        correct_answer = st.text_area("正确答案", height=100, placeholder="输入标准正确答案")
        note = st.text_area("个人备注（选填）", height=100, placeholder="可以记录自己的思考和感悟")
    
    if st.button("开始AI分析并保存", type="primary", use_container_width=True):
        if not question or not correct_answer:
            st.markdown('<div class="error-box">⚠️ 题目和正确答案不能为空！</div>', unsafe_allow_html=True)
        else:
            with st.spinner("🤖 AI正在分析你的错题，请稍候..."):
                # 构建提示词
                prompt = f"""
                请分析以下{subject}学科的错题：
                
                题目：{question}
                学生错误答案：{wrong_answer}
                正确答案：{correct_answer}
                
                请严格按照以下三个方面进行分析：
                1. 错误原因分析：精准指出学生为什么会做错
                2. 核心知识点：列出这道题涉及的所有关键知识点
                3. 解题技巧：给出解决这类题目的通用方法和技巧
                
                要求语言简洁明了，适合学生学习使用。
                """
                
                # 调用AI
                ai_result = ai_chat(prompt)
                
                # 保存到数据库
                add_error(
                    subject=subject,
                    question=question,
                    wrong_answer=wrong_answer,
                    correct_answer=correct_answer,
                    ai_analysis=ai_result,
                    note=note
                )
                
                st.markdown('<div class="success-box">✅ 错题保存成功！</div>', unsafe_allow_html=True)
                st.divider()
                st.markdown('<div class="sub-header">🤖 AI分析结果</div>', unsafe_allow_html=True)
                st.write(ai_result)

# 2. 查看错题本功能
elif menu == "查看错题本":
    st.markdown('<div class="sub-header">📖 我的错题本</div>', unsafe_allow_html=True)
    
    all_errors = get_all_errors()
    
    if not all_errors:
        st.info("📭 错题本为空，快去录入你的第一道错题吧！")
    else:
        # 按学科筛选
        subjects = ["全部"] + list(set([e.subject for e in all_errors]))
        selected_subject = st.selectbox("按学科筛选", subjects)
        
        filtered_errors = all_errors
        if selected_subject != "全部":
            filtered_errors = [e for e in all_errors if e.subject == selected_subject]
        
        st.write(f"共找到 {len(filtered_errors)} 道错题")
        st.divider()
        
        # 显示错题列表
        for error in filtered_errors:
            with st.expander(f"【{error.subject}】错题ID：{error.id} | {error.question[:50]}..."):
                st.subheader("题目")
                st.write(error.question)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("错误答案")
                    st.write(error.wrong_answer)
                with col2:
                    st.subheader("正确答案")
                    st.write(error.correct_answer)
                
                st.subheader("🤖 AI分析")
                st.write(error.ai_analysis)
                
                if error.note:
                    st.subheader("📝 个人备注")
                    st.write(error.note)
                
                # 删除按钮
                if st.button(f"删除该错题", key=f"delete_{error.id}", type="secondary"):
                    delete_error(error.id)
                    st.rerun()

# 3. 知识点总结功能
elif menu == "知识点总结":
    st.markdown('<div class="sub-header">📊 知识点总结</div>', unsafe_allow_html=True)
    
    all_errors = get_all_errors()
    
    if not all_errors:
        st.markdown('<div class="error-box">⚠️ 请先录入错题再生成知识点总结</div>', unsafe_allow_html=True)
    else:
        # 按学科生成总结
        subjects = list(set([e.subject for e in all_errors]))
        selected_subject = st.selectbox("选择学科", subjects)
        
        if st.button("生成知识点总结", type="primary", use_container_width=True):
            with st.spinner("🤖 AI正在整合所有错题生成总结，请稍候..."):
                # 筛选该学科的错题
                subject_errors = [e for e in all_errors if e.subject == selected_subject]
                
                # 构建提示词
                errors_text = ""
                for i, error in enumerate(subject_errors):
                    errors_text += f"""
                    错题{i+1}：
                    题目：{error.question}
                    完整分析：{error.ai_analysis}
                    """
                
                prompt = f"""
                请根据以下{selected_subject}学科的错题，生成一份全面的知识点总结：
                
                {errors_text}
                
                总结要求：
                1. 梳理出所有涉及的核心知识点
                2. 指出最容易出错的知识点和常见错误类型
                3. 给出针对性的学习建议和复习重点
                
                请用清晰的结构和简洁的语言回答。
                """
                
                summary = ai_chat(prompt)
                
                st.markdown(f'<div class="sub-header">📚 {selected_subject}知识点总结</div>', unsafe_allow_html=True)
                st.write(summary)

# 4. 生成练习题功能
elif menu == "生成练习题":
    st.markdown('<div class="sub-header">✏️ 生成针对性练习题</div>', unsafe_allow_html=True)
    
    all_errors = get_all_errors()
    
    if not all_errors:
        st.markdown('<div class="error-box">⚠️ 请先录入错题再生成练习题</div>', unsafe_allow_html=True)
    else:
        # 按学科生成
        subjects = list(set([e.subject for e in all_errors]))
        selected_subject = st.selectbox("选择学科", subjects)
        num_questions = st.slider("题目数量", 1, 10, 5)
        
        if st.button("生成练习题", type="primary", use_container_width=True):
            with st.spinner("🤖 AI正在生成针对性练习题，请稍候..."):
                # 筛选该学科的错题
                subject_errors = [e for e in all_errors if e.subject == selected_subject]
                
                # 构建提示词
                errors_text = ""
                for i, error in enumerate(subject_errors):
                    errors_text += f"""
                    错题{i+1}：
                    题目：{error.question}
                    完整分析：{error.ai_analysis}
                    """
                
                prompt = f"""
                请根据以下{selected_subject}学科的错题，生成{num_questions}道针对性的练习题：
                
                {errors_text}
                
                要求：
                1. 题目要针对错题中暴露的薄弱知识点
                2. 题目难度适中，适合巩固练习
                3. 每道题都要给出详细的答案和解析
                
                请按照以下格式输出：
                1. 题目1
                答案：
                解析：
                
                2. 题目2
                答案：
                解析：
                ...
                """
                
                exercises = ai_chat(prompt)
                
                st.markdown(f'<div class="sub-header">✏️ {selected_subject}针对性练习题</div>', unsafe_allow_html=True)
                st.write(exercises)