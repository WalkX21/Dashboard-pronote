import json
import pandas as pd
import streamlit as st
import plotly.express as px
from collections import defaultdict


# Load JSON data
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Parse user mark
def parse_user_mark(user_mark):
    """Convert user mark to a normalized score out of 20."""
    if "/" in user_mark:
        mark, max_mark = map(lambda x: float(x.replace(",", ".")), user_mark.split("/"))
        return (mark / max_mark) * 20
    else:
        return float(user_mark.replace(",", "."))


# Parse class average
def parse_class_average(class_average):
    """Convert class average to a float value."""
    return float(class_average.replace(",", "."))


# Calculate averages per subject
def calculate_moyenne_par_matiere(data):
    subject_totals = defaultdict(lambda: {"weighted_sum": 0, "total_coeff": 0})

    for entry in data:
        subject = entry["subject"]
        user_mark = parse_user_mark(entry["user_mark"])
        coefficient = float(entry["coefficient"])

        # Accumulate weighted sum and coefficients
        subject_totals[subject]["weighted_sum"] += user_mark * coefficient
        subject_totals[subject]["total_coeff"] += coefficient

    # Calculate weighted average for each subject
    return {
        subject: round(totals["weighted_sum"] / totals["total_coeff"], 2)
        for subject, totals in subject_totals.items()
        if totals["total_coeff"] > 0
    }


# Calculate general averages per date (user and class)
def calculate_moyenne_per_date(data):
    data_by_date = defaultdict(list)
    for entry in data:
        data_by_date[entry["date"]].append(entry)

    date_results = []
    running_marks = []
    running_class_averages = []

    for date, entries in sorted(data_by_date.items()):
        running_marks.extend(entries)

        # Compute user averages
        user_total_weighted = sum(
            parse_user_mark(entry["user_mark"]) * float(entry["coefficient"]) for entry in running_marks
        )
        user_total_coeff = sum(float(entry["coefficient"]) for entry in running_marks)
        user_moyenne_generale = user_total_weighted / user_total_coeff if user_total_coeff else 0

        # Compute class averages
        running_class_averages.extend(
            [{"class_average": parse_class_average(entry["class_average"]), "coefficient": float(entry["coefficient"])} for
             entry in entries])

        class_total_weighted = sum(
            avg["class_average"] * avg["coefficient"] for avg in running_class_averages
        )
        class_total_coeff = sum(avg["coefficient"] for avg in running_class_averages)
        class_moyenne_generale = class_total_weighted / class_total_coeff if class_total_coeff else 0

        date_results.append({
            "date": date,
            "user_moyenne_generale": round(user_moyenne_generale, 2),
            "class_moyenne_generale": round(class_moyenne_generale, 2)
        })

    return date_results


# Streamlit App
def run_streamlit_app(data, date_results):
    st.title("Marks Analysis Dashboard")

    # Overview
    st.header("Data Overview")
    st.write("Combined Data from JSON")
    st.dataframe(pd.DataFrame(data))

    # Subject Filter
    unique_subjects = sorted(set(entry["subject"] for entry in data))
    selected_subject = st.radio("Select a Subject for Detailed Analysis", unique_subjects)

    # 1. Moyenne Générale Progression with Class Comparison
    st.header("Moyenne Générale vs Class Moyenne Progression")
    progression_df = pd.DataFrame({
        "Date": [res["date"] for res in date_results],
        "User Moyenne Générale": [res["user_moyenne_generale"] for res in date_results],
        "Class Moyenne Générale": [res["class_moyenne_generale"] for res in date_results],
    })
    progression_df.set_index("Date", inplace=True)
    st.line_chart(progression_df)

    # 2. Subject-Wise Performance
    st.header("Subject-Wise Performance")
    moyenne_par_matiere = calculate_moyenne_par_matiere(data)
    st.write("Averages by Subject")
    st.json(moyenne_par_matiere)

    # Bar chart for Subject-Wise Averages
    subject_avg_df = pd.DataFrame({
        "Subject": list(moyenne_par_matiere.keys()),
        "Average": list(moyenne_par_matiere.values())
    })
    fig = px.bar(
        subject_avg_df,
        x="Subject",
        y="Average",
        title="Subject-Wise Averages (User)",
        labels={"Average": "Average Marks"},
    )
    st.plotly_chart(fig)

    # 3. User Marks vs Class Averages
    st.header("User Marks vs. Class Averages")
    comparison_data = pd.DataFrame([
        {
            "Date": entry["date"],
            "Subject": entry["subject"],
            "User Mark": parse_user_mark(entry["user_mark"]),
            "Class Average": parse_class_average(entry["class_average"])
        }
        for entry in data
    ])
    fig = px.scatter(
        comparison_data,
        x="User Mark",
        y="Class Average",
        color="Subject",
        title="User Marks vs Class Averages",
        hover_data=["Date", "Subject"]
    )
    st.plotly_chart(fig)

    # 4. Impact of Coefficients
    st.header("Impact of Coefficients on Moyenne Générale")
    impact_data = pd.DataFrame([
        {
            "Subject": subject,
            "Impact": moyenne
        }
        for subject, moyenne in moyenne_par_matiere.items()
    ])
    fig = px.bar(
        impact_data,
        x="Subject",
        y="Impact",
        title="Subject Impact on Moyenne Générale",
        labels={"Impact": "Average Contribution"}
    )
    st.plotly_chart(fig)

    # 5. Performance Trends by Subject
    st.header(f"Performance Trends for {selected_subject}")
    subject_data = [
        entry for entry in data if entry["subject"] == selected_subject
    ]
    subject_df = pd.DataFrame({
        "Date": [entry["date"] for entry in subject_data],
        "Mark": [parse_user_mark(entry["user_mark"]) for entry in subject_data]
    })
    st.line_chart(subject_df.set_index("Date"))

    # 6. Detailed Analysis Per Date
    st.header("Detailed Analysis Per Date")
    for res in date_results:
        st.subheader(f"Date: {res['date']}")
        st.write("Moyenne Par Matière:")
        st.json(res["moyenne_par_matiere"])
        st.write(f"User Moyenne Générale: {res['user_moyenne_generale']}")
        st.write(f"Class Moyenne Générale: {res['class_moyenne_generale']}")

    st.header("Additional Insights")
    st.write("You can extend this dashboard to include more insights or export the data.")


if __name__ == "__main__":
    # Load the dataset
    data = load_data("combined_marks.json")

    # Perform analysis
    date_results = calculate_moyenne_per_date(data)

    # Launch Streamlit app
    run_streamlit_app(data, date_results)
