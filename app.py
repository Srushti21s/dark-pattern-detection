
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter

from website_collector import collect_website
from pattern_detector import detect_patterns
from risk_analyzer import calculate_risk
from ml_detector import predict_pattern


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Dark Pattern Risk Analyzer",
    page_icon="🔍",
    layout="wide"
)

# MAIN TITLE
st.title("🔍 Dark Pattern Detection & Risk Analysis")
st.caption("An intelligent prototype for detecting potentially manipulative website interfaces.")

st.divider()

# WEBSITE ANALYSIS
st.header("Website Analysis")

website_url = st.text_input(
    "Enter Website URL (optional)",
    placeholder="https://example.com"
)

uploaded_file = st.file_uploader(
    "Or upload a website HTML file",
    type=["html", "htm"]
)

sample_text = (
    "Limited time offer! Don't miss out. "
    "Additional charges apply. "
    "Sign up to continue shopping. "
    "Recommended option: Premium Membership. "
    "Contact support to cancel your subscription. "
    "Subscribe now!"
)

text_input = st.text_area(
    "Or enter website text:",
    value=sample_text,
    height=150
)

# ANALYSE BUTTON
if st.button("Analyse Website", type="primary"):

    text_to_analyse = ""

    # HTML UPLOAD
    if uploaded_file is not None:

        html_content = uploaded_file.read().decode(
            "utf-8", errors="replace"
        )

        soup = BeautifulSoup(html_content, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text_to_analyse = soup.get_text(
            separator=" ", strip=True
        )

    # WEBSITE URL
    elif website_url.strip():

        parsed = urlparse(website_url.strip())

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            st.error("Please enter a valid HTTP or HTTPS URL.")
            st.stop()

        try:
            with st.spinner("Collecting website content..."):
                website_data = collect_website(website_url.strip())
                text_to_analyse = website_data["text"]

        except Exception as e:
            st.error(f"Website collection failed: {e}")
            st.stop()

    # MANUAL TEXT
    else:
        text_to_analyse = text_input

    if not text_to_analyse.strip():
        st.warning("Please provide website content to analyse.")
        st.stop()

    # PATTERN DETECTION
    results = detect_patterns(text_to_analyse)

    unique_results = list({
        (item["pattern"], item["evidence"]): item
        for item in results
    }.values())

    evidence_counts = Counter(
        item["pattern"] for item in unique_results
    )

    # RISK CALCULATION
    risks = {
        pattern: calculate_risk(pattern, count)
        for pattern, count in evidence_counts.items()
    }

    high = sum(r["level"] == "High" for r in risks.values())
    medium = sum(r["level"] == "Medium" for r in risks.values())
    low = sum(r["level"] == "Low" for r in risks.values())

    # OVERALL RISK
    if high > 0:
        overall_risk = "HIGH"
    elif medium > 0:
        overall_risk = "MEDIUM"
    elif low > 0:
        overall_risk = "LOW"
    else:
        overall_risk = "NO RISK DETECTED"

    # MACHINE LEARNING
    try:
        ml_result = predict_pattern(text_to_analyse)
    except Exception as e:
        st.error(f"Machine learning prediction failed: {e}")
        st.stop()

    st.success("Analysis completed!")

    st.divider()

    # DASHBOARD METRICS
    st.header("📊 Analysis Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Patterns Found", len(unique_results))
    c2.metric("High Risk", high)
    c3.metric("Medium Risk", medium)
    c4.metric("Low Risk", low)

    st.divider()

    # OVERALL RISK ASSESSMENT
    st.subheader("⚠️ Overall Risk Assessment")

    st.info(f"Overall Website Risk: {overall_risk}")

    if overall_risk == "HIGH":
        st.warning("Potentially high-risk patterns were detected.")
    elif overall_risk == "MEDIUM":
        st.info("Some potentially manipulative patterns were detected.")
    elif overall_risk == "LOW":
        st.success("Only low-risk patterns were detected.")
    else:
        st.success("No known keyword patterns were detected.")

    st.divider()

    # RISK DISTRIBUTION
    left, right = st.columns(2)

    with left:
        st.subheader("Risk Distribution")

        risk_chart = pd.DataFrame({
            "Risk Level": ["High", "Medium", "Low"],
            "Count": [high, medium, low]
        })

        st.bar_chart(risk_chart.set_index("Risk Level"))

    with right:
        st.subheader("🤖 Machine Learning Result")

        st.metric(
            "Predicted Category",
            ml_result["prediction"]
        )

        st.metric(
            "Model Score",
            str(ml_result["confidence"]) + "%"
        )

    st.divider()

    # PATTERN CATEGORY DISTRIBUTION
    st.subheader("📊 Pattern Category Distribution")

    if evidence_counts:

        pattern_chart = pd.DataFrame({
            "Pattern": list(evidence_counts.keys()),
            "Count": list(evidence_counts.values())
        })

        st.bar_chart(pattern_chart.set_index("Pattern"))

    else:
        st.info("No patterns available to display.")

    st.divider()

    # DETAILED RESULTS
    st.header("🔍 Detailed Detection Results")

    pattern_explanations = {
        "Nagging": "Repeated prompts or notifications that pressure users into taking an action.",
        "Obstruction": "Making actions such as cancelling a subscription unnecessarily difficult.",
        "Sneaking": "Hiding important information such as additional charges or fees.",
        "Interface Interference": "Using visual design or default selections to influence user choices.",
        "Forced Action": "Requiring users to perform an action, such as signing up, to continue."
    }

    if unique_results:

        rows = []

        for item in unique_results:

            pattern = item["pattern"]
            risk = risks[pattern]

            rows.append({
                "Pattern": pattern,
                "Evidence": item["evidence"],
                "Evidence Count": evidence_counts[pattern],
                "Risk Score": risk["score"],
                "Risk Level": risk["level"]
            })

        results_df = pd.DataFrame(rows)

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

        # PATTERN EXPLANATIONS
        st.subheader("📖 Pattern Explanations")

        for pattern in evidence_counts:

            with st.expander(f"🔍 {pattern}"):

                st.write(pattern_explanations.get(
                    pattern, "Explanation unavailable."
                ))

                st.write("Evidence found:")

                for item in unique_results:
                    if item["pattern"] == pattern:
                        st.write(f"- {item['evidence']}")

        # DOWNLOAD REPORT
        csv = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Analysis Report",
            data=csv,
            file_name="dark_pattern_analysis.csv",
            mime="text/csv"
        )

    else:
        st.success("No keyword patterns detected.")

    st.divider()

    st.caption(
        "Prototype limitation: Uses keyword-based detection, "
        "illustrative risk scores and a small synthetic ML dataset. "
        "Results require further validation."
    )
