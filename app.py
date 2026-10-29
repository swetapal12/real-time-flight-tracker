import math
import re
import streamlit as st

st.set_page_config(
    page_title="Advanced Password Security Analyzer", 
    page_icon="🛡️", 
    layout="centered"
)

st.title("🛡️ Advanced Password Security Analyzer")
st.write("Evaluate password strength, mathematical entropy, and brute-force crack time.")
st.markdown("---")

show_password = st.checkbox("Show password characters")
input_type = "default" if show_password else "password"

password = st.text_input("Enter a password to test:", type=input_type)

def estimate_crack_time(entropy):
    guesses_per_second = 10_000_000_000
    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_second / 2

    if seconds < 1:
        return "Instantaneous (less than a second)"
    elif seconds < 60:
        return f"About {round(seconds, 2)} seconds"
    elif seconds < 3600:
        return f"About {round(seconds / 60, 1)} minutes"
    elif seconds < 86400:
        return f"About {round(seconds / 3600, 1)} hours"
    elif seconds < 31536000:
        return f"About {round(seconds / 86400, 1)} days"
    elif seconds < 31536000 * 1000:
        return f"About {round(seconds / 31536000, 1)} years"
    else:
        return "Centuries (Virtually Uncrackable)"

def analyze_password(pwd):
    if not pwd:
        return 0, 0, []

    length = len(pwd)
    pool_size = 0
    feedback = []

    has_lower = bool(re.search(r"[a-z]", pwd))
    has_upper = bool(re.search(r"[A-Z]", pwd))
    has_digit = bool(re.search(r"[0-9]", pwd))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", pwd))

    if has_lower:
        pool_size += 26
    else:
        feedback.append("Add lowercase letters (a-z).")

    if has_upper:
        pool_size += 26
    else:
        feedback.append("Add uppercase letters (A-Z).")

    if has_digit:
        pool_size += 10
    else:
        feedback.append("Add numbers (0-9).")

    if has_symbol:
        pool_size += 32
    else:
        feedback.append("Add special characters (e.g., @, #, $).")

    if length < 12:
        feedback.append("Increase length to at least 12 characters.")

    entropy = round(length * math.log2(pool_size), 2) if pool_size > 0 else 0
    return entropy, length, feedback

if password:
    entropy, length, feedback = analyze_password(password)
    crack_time = estimate_crack_time(entropy)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Password Length", value=f"{length} chars")
    with col2:
        st.metric(label="Calculated Entropy", value=f"{entropy} bits")

    st.info(f"⏱️ *Estimated Brute-Force Crack Time:* {crack_time}")

    if entropy < 28:
        st.error("🚨 Strength: *Very Weak*")
    elif entropy < 36:
        st.warning("⚠️ Strength: *Weak*")
    elif entropy < 60:
        st.info("💡 Strength: *Moderate*")
    else:
        st.success("🛡️ Strength: *Strong*")

    if feedback:
        st.subheader("Recommendations:")
        for tip in feedback:
            st.write(f"- {tip}")
else:
    st.info("Type or paste a password above to analyze.")