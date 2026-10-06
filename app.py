"""Password Strength Analyzer & Security Suggestion Tool.

Run locally with: streamlit run app.py
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from password_strength_analyzer.core.analyzer import analyze_password
from password_strength_analyzer.core.history import clear_history, load_safe_history, save_safe_history

st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔐 Password Strength Analyzer & Security Suggestion Tool")
st.caption("Defensive, local-first password assessment for cybersecurity education")

with st.sidebar:
    st.header("🛡️ Privacy by design")
    st.write(
        "Your password is analyzed in memory by this application. "
        "It is not written to history, printed to logs, or sent to an external service."
    )
    st.warning("Use synthetic/demo passwords for screenshots and demonstrations. Never paste a real password into a public/shared environment.")
    st.divider()
    st.subheader("Optional context")
    st.write("Enter demo terms only. They are used only for the current analysis and are not saved.")
    context_raw = st.text_input("Context terms (comma-separated)", placeholder="student, college, example")
    context_terms = [x.strip() for x in context_raw.split(",") if x.strip()]

    st.divider()
    st.subheader("Safe local history")
    st.caption("Only aggregate metadata is saved; passwords are never stored.")
    if st.button("Clear local history"):
        clear_history()
        st.success("Local aggregate history cleared.")

password = st.text_input(
    "Enter a password for local analysis",
    type="password",
    placeholder="Use a synthetic demo password",
    help="Analysis happens locally. Do not use a real password in a classroom screenshot or shared computer.",
)

if password:
    result = analyze_password(password, context_terms)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.score}/100")
    col2.metric("Classification", result.classification)
    col3.metric("Length", result.length)
    col4.metric("Entropy-style estimate", f"{result.estimated_entropy_bits} bits")
    st.progress(result.score / 100)

    if result.classification in {"VERY WEAK", "WEAK"}:
        st.error(f"Assessment: **{result.classification}**")
    elif result.classification == "MODERATE":
        st.warning(f"Assessment: **{result.classification}**")
    else:
        st.success(f"Assessment: **{result.classification}**")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "⚠️ Weaknesses", "💡 Suggestions", "📚 Learn"])

    with tab1:
        left, right = st.columns(2)
        with left:
            st.subheader("Length analysis")
            if result.length < 8:
                st.error("Below 8 characters")
            elif result.length < 12:
                st.warning("8–11 characters")
            elif result.length < 16:
                st.info("12–15 characters")
            else:
                st.success("16+ characters")
            st.write(f"Length contribution: **{result.length_score}/30**")

        with right:
            st.subheader("Character diversity")
            labels = {"uppercase": "Uppercase", "lowercase": "Lowercase", "digits": "Digits", "symbols": "Symbols"}
            for key, label in labels.items():
                st.write(f"{'✅' if result.character_diversity[key] else '❌'} {label}")
            st.caption(f"Approximate character pool used by the entropy-style estimate: {result.character_pool_size}")

        st.subheader("Detection summary")
        detection = pd.DataFrame([
            ["Common password", result.common_password],
            ["Repeated characters", result.repeated_character],
            ["Sequential pattern", result.sequential_pattern],
            ["Keyboard pattern", result.keyboard_pattern],
            ["Dictionary/common word", result.dictionary_word],
            ["Personal-context overlap", result.personal_information_overlap],
        ], columns=["Check", "Detected"])
        detection["Detected"] = detection["Detected"].map(lambda x: "⚠️ Yes" if x else "✅ No")
        st.dataframe(detection, hide_index=True, use_container_width=True)

        if st.button("Save safe aggregate result to local history"):
            save_safe_history(result.safe_dict())
            st.success("Saved only aggregate metadata. The password was not stored.")

    with tab2:
        if result.findings:
            for finding in result.findings:
                icon = {"critical": "🚨", "high": "🔴", "medium": "🟠", "low": "🟡"}.get(finding.severity, "ℹ️")
                st.markdown(f"### {icon} {finding.category}")
                st.write(finding.message)
        else:
            st.success("No obvious pattern-based weaknesses were detected by these checks.")
        st.info("A clean result does not prove that a password is safe. Real attackers may have leaked-password databases and smarter guessing models that this educational analyzer does not reproduce.")

    with tab3:
        st.subheader("Recommended actions")
        for suggestion in result.suggestions:
            st.markdown(f"- {suggestion}")
        st.subheader("Passphrase guidance")
        st.write("A strong passphrase is long, unique, and difficult to predict. Prefer several unrelated words rather than a familiar sentence, quotation, name, or pattern.")
        st.write("Example for education only: `river-cactus-orbit-lantern-mango` — do not use this example as a real credential.")

    with tab4:
        st.subheader("Why composition alone is not enough")
        st.write("A password such as `Password123!` contains uppercase/lowercase letters, numbers, and a symbol, but it is still highly predictable. This project therefore combines length, estimated character space, common-password checks, dictionary checks, repeated characters, sequences, keyboard patterns, and optional context overlap.")
        st.subheader("Entropy-style estimate")
        st.write("The displayed value is a rough mathematical estimate based on password length and an estimated character pool: length × log₂(pool size). It assumes random selection from that pool, which humans usually do not achieve. Therefore it is not a measurement of actual attacker effort or guaranteed security.")
        st.subheader("What this tool does not do")
        st.write("It does not crack passwords, attempt authentication, query breach services, collect credentials, or send passwords to external APIs.")

st.divider()
st.header("📈 Local aggregate history")
history = load_safe_history()
if history:
    history_df = pd.DataFrame(history)
    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"], errors="coerce")
    st.dataframe(history_df, hide_index=True, use_container_width=True)
    if "score" in history_df.columns:
        st.line_chart(history_df[["score"]].reset_index(drop=True))
else:
    st.caption("No local aggregate history yet. Run an analysis and choose to save its safe metadata.")

st.divider()
st.caption("Educational cybersecurity project • Local-first • Defensive use only • Passwords are not stored or transmitted")
