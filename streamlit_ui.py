import streamlit as st
from app1 import analyze_career, analyze_resume_job

st.set_page_config(
    page_title="CareerTwin | AI Career Copilot",
    page_icon="💼",
    layout="wide"
)

st.title("💼 CareerTwin")
st.subheader("Your personal AI Career & Interview Copilot")

st.write(
    "Analyse your career profile, identify skill gaps,"
    "ana prepare for your target job role."
)

career_tab, resume_tab = st.tabs(
    ["Career Analysis", "Resume vs Job Description"]
)

with career_tab:
    st.header("Your Career Profile")

    with st.form("career_form"):
        student_name = st.text_input("Student Name")
        education = st.text_input("Education", placeholder="MCA")
        skills = st.text_area("Technical Skills", placeholder="Python, SQL")
        projects = st.text_area("Projects", placeholder="E-Commerce, REST API")
        experience = st.text_area("Experience/Intership", 
                                  placeholder="Fresher or relevant experience")
        target_role = st.text_input("Target Job Role", placeholder="Backend Developer")

        career_submit_btn = st.form_submit_button(
            "Analyse My Career",
            type="primary"
        )

    if career_submit_btn:
        if not student_name.strip() or not target_role.strip():
            st.warning("Enter your name and target job role...")
        else:
            # Context Engineering
            student_context = f"""
            STUDENT PROFILE

            Name: {student_name}
            Education: {education}
            Technical Skills: {skills}
            Projects: {projects}
            Experience/Internship: {experience}
            Target Job Role: {target_role}
            """

            try:
                # Show progress while Gemini processes the request
                with st.spinner("Analyzing your career profile"):
                    result = analyze_career(student_context)

                st.success("Career Analysis Completed")

                st.subheader("Profile summary")
                st.write(result["profile_summary"])

                left, right = st.columns(2)
                with left:
                    st.subheader("Strengths")
                    for item in result["strengths"]:
                        st.markdown(f"- {item}")

                    st.subheader("Skill Gaps")
                    for item in result["skill_gaps"]:
                        st.markdown(f"- {item}")

                    st.subheader("Priority Skills")
                    for item in result["priority_skills"]:
                        st.markdown(f"- {item}")

                with right:
                    st.subheader("Interview Topics")
                    for item in result["interview_topics"]:
                        st.markdown(f"- {item}")

            except BaseException as ex:
                st.error(f"Career analysis failed: {ex}")


with resume_tab:
    st.header("Resume vs Job Description Matcher")
    st.write("Compare your resume against a target job description to find skill gaps and tailor your bullet points.")

    with st.form("resume_form"):
        resume_input = st.text_area(
            "Paste Your Resume Text", 
            placeholder="Paste the plain text content of your resume here...",
            height=200
        )
        job_desc_input = st.text_area(
            "Paste Job Description", 
            placeholder="Paste the target job description here...",
            height=200
        )

        resume_submit_btn = st.form_submit_button(
            "Analyze Match",
            type="primary"
        )

    if resume_submit_btn:
        if not resume_input.strip() or not job_desc_input.strip():
            st.warning("Please provide both your resume text and the job description.")
        else:
            try:
                with st.spinner("Analyzing resume against job description..."):
                    match_result = analyze_resume_job(resume_input, job_desc_input)

                st.success("Analysis Completed Successfully!")

                st.subheader("Match Summary")
                st.write(match_result.get("match_summary", "No summary provided."))

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Matching Skills")
                    matching = match_result.get("matching_skills", [])
                    if matching:
                        for item in matching:
                            st.markdown(f"- ✅ {item}")
                    else:
                        st.info("No explicit matching skills found.")

                    st.subheader("Resume Improvements")
                    improvements = match_result.get("resume_improvements", [])
                    if improvements:
                        for item in improvements:
                            st.markdown(f"- 💡 {item}")
                    else:
                        st.info("No specific improvements listed.")

                with col2:
                    st.subheader("Missing Skills / Requirements")
                    missing = match_result.get("missing_skills", [])
                    if missing:
                        for item in missing:
                            st.markdown(f"- ❌ {item}")
                    else:
                        st.info("No major missing skills identified!")

            except Exception as ex:
                st.error(f"Resume analysis failed: {ex}")