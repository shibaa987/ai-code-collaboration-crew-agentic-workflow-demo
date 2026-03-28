import streamlit as st
import sys, os, re
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.crew import build_crew
from src.tools.github_tool import GitHubPRTool


def extract_code(text: str) -> str:
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def stream_text(text, placeholder, delay=0.01):
    """Simulate typing effect"""
    output = ""
    for char in text:
        output += char
        placeholder.markdown(output)
        time.sleep(delay)

def split_sections(text):
    sections = {
        "code": "",
        "review": "",
        "tests": ""
    }

    if "### BACKEND CODE ###" in text:
        parts = text.split("### BACKEND CODE ###")
        sections["code"] = parts[-1]

    # if "### REVIEW ###" in text:
    #     parts = text.split("### REVIEW ###")
    #     sections["review"] = parts[-1]
    #
    # if "### TESTS ###" in text:
    #     parts = text.split("### TESTS ###")
    #     sections["tests"] = parts[-1]

    return sections

# Page config
st.set_page_config(page_title="AI Code Crew", layout="wide")

# Header
st.title("🤖 AI Code Collaboration Crew")
st.markdown("Generate → Review → Test → Create PR")

# Sidebar
st.sidebar.header("⚙️ Settings")
model = st.sidebar.selectbox("Model", ["Groq", "OpenAI"])
create_pr = st.sidebar.checkbox("Auto Create PR")

# Input
feature_request = st.text_area(
    "💡 Enter Feature Request",
    placeholder="Create a simple python program that cretaes simple stories for kids"
)

# Run button
if st.button("Run AI Crew"):

    if not feature_request.strip():
        st.warning("Please enter a feature request")
        st.stop()

    st.subheader("⚙️ Agent Execution")

    # Placeholders for each agent
    backend_box = st.empty()
    review_box = st.empty()
    test_box = st.empty()

    with st.spinner("Running agents... ⏳"):
        crew = build_crew(feature_request)
        result = crew.kickoff()

    output_text = result.raw
    sections = split_sections(output_text)

    # 👨‍💻 Backend Agent
    st.markdown("### 👨‍💻 Backend Engineer")
    stream_text(sections["code"] or output_text, backend_box)

    # 🕵️ Reviewer
    # st.markdown("### 🕵️ Code Reviewer")
    # stream_text(sections["review"] or "No review output", review_box)
    #
    # # 🧪 Tester
    # st.markdown("### 🧪 Test Engineer")
    # stream_text(sections["tests"] or "No tests generated", test_box)

    with st.spinner("Running agents... ⏳"):
        crew = build_crew(feature_request)
        result = crew.kickoff()

        output_text = result.raw

        sections = split_sections(output_text)

        code = extract_code(sections["code"] or output_text)
        # review = sections["review"]
        # tests = sections["tests"]

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Code", "🧠 Full Output", "🧪 Validation", "🚀 PR"]
    )

    # 📄 Code Tab
    with tab1:
        st.subheader("Generated Code")
        st.code(code)

    # 🧠 Full Output
    with tab2:
        st.subheader("Agent Output")
        st.text(output_text)

    # 🧪 Validation
    with tab3:
        if "def " in code:
            st.success("✅ Valid Python function detected")
        else:
            st.error("❌ Invalid code")

    # 🚀 PR Tab
    with tab4:
        if "def " in code:
            if create_pr:
                pr_tool = GitHubPRTool()
                pr_url = pr_tool._run(file_content=code)

                st.success("PR Created 🎉")
                st.markdown(f"[View PR]({pr_url})")
            else:
                st.info("Enable PR creation from sidebar")
        else:
            st.warning("Fix code before PR")

    # with tab5:
    #     st.text(review)
