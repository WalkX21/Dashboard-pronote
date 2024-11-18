# import json
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# from collections import defaultdict


# # Load JSON data
# def load_data(file_path):
#     with open(file_path, "r", encoding="utf-8") as file:
#         return json.load(file)


# # Parse user mark
# def parse_user_mark(user_mark):
#     """Convert user mark to a normalized score out of 20."""
#     if "/" in user_mark:
#         mark, max_mark = map(lambda x: float(x.replace(",", ".")), user_mark.split("/"))
#         return (mark / max_mark) * 20
#     else:
#         return float(user_mark.replace(",", "."))


# # Calculate averages per subject
# def calculate_moyenne_par_matiere(data):
#     subject_totals = defaultdict(lambda: {"weighted_sum": 0, "total_coeff": 0})

#     for entry in data:
#         subject = entry["subject"]
#         user_mark = parse_user_mark(entry["user_mark"])
#         coefficient = float(entry["coefficient"])

#         # Accumulate weighted sum and coefficients
#         subject_totals[subject]["weighted_sum"] += user_mark * coefficient
#         subject_totals[subject]["total_coeff"] += coefficient

#     # Calculate weighted average for each subject
#     return {
#         subject: round(totals["weighted_sum"] / totals["total_coeff"], 2)
#         for subject, totals in subject_totals.items()
#         if totals["total_coeff"] > 0
#     }


# # Calculate general averages per date
# def calculate_moyenne_per_date(data):
#     data_by_date = defaultdict(list)
#     for entry in data:
#         data_by_date[entry["date"]].append(entry)

#     date_results = []
#     running_marks = []
#     for date, entries in sorted(data_by_date.items()):
#         running_marks.extend(entries)

#         # Compute averages
#         moyenne_par_matiere = calculate_moyenne_par_matiere(running_marks)
#         moyenne_generale = sum(moyenne_par_matiere.values()) / len(moyenne_par_matiere)

#         date_results.append({
#             "date": date,
#             "moyenne_par_matiere": moyenne_par_matiere,
#             "moyenne_generale": round(moyenne_generale, 2)
#         })

#     return date_results


# # Streamlit App
# def run_streamlit_app(data, date_results):
#     st.title("Marks Analysis Dashboard")

#     # Overview
#     st.header("Data Overview")
#     st.write("Combined Data from JSON")
#     st.dataframe(pd.DataFrame(data))

#     # Moyenne par Matière
#     st.header("Subject-wise Averages")
#     moyenne_par_matiere = calculate_moyenne_par_matiere(data)
#     st.write("Averages by Subject")
#     st.json(moyenne_par_matiere)

#     # Chart for Moyenne Générale Progression
#     st.header("Moyenne Générale Progression")
#     moyenne_generale_over_time = pd.DataFrame({
#         "Date": [res["date"] for res in date_results],
#         "Moyenne Générale": [res["moyenne_generale"] for res in date_results]
#     })
#     st.line_chart(moyenne_generale_over_time.set_index("Date"))

#     # Subject-wise Average Chart
#     st.header("Subject-wise Averages Over Time")
#     subject_data = pd.DataFrame([
#         {"Date": res["date"], "Subject": subject, "Average": moyenne}
#         for res in date_results
#         for subject, moyenne in res["moyenne_par_matiere"].items()
#     ])
#     st.line_chart(subject_data.pivot(index="Date", columns="Subject", values="Average"))

#     # Detailed Analysis
#     st.header("Detailed Analysis Per Date")
#     for res in date_results:
#         st.subheader(f"Date: {res['date']}")
#         st.write("Moyenne Par Matière:")
#         st.json(res["moyenne_par_matiere"])
#         st.write(f"Moyenne Générale: {res['moyenne_generale']}")

#     st.header("Additional Insights")
#     st.write("You can extend this dashboard to include more insights or export the data.")


# if __name__ == "__main__":
#     # Load the dataset
#     data = load_data("combined_marks.json")

#     # Perform analysis
#     date_results = calculate_moyenne_per_date(data)

#     # Launch Streamlit app
#     run_streamlit_app(data, date_results)

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
        moyenne_par_matiere = calculate_moyenne_par_matiere(running_marks)
        moyenne_generale = sum(moyenne_par_matiere.values()) / len(moyenne_par_matiere)

        # Compute class averages
        running_class_averages.extend(
            [{"class_average": parse_class_average(entry["class_average"]), "coefficient": float(entry["coefficient"])} for
             entry in entries])

        weighted_sum = sum(avg["class_average"] * avg["coefficient"] for avg in running_class_averages)
        total_coeff = sum(avg["coefficient"] for avg in running_class_averages)
        class_moyenne_generale = weighted_sum / total_coeff if total_coeff else 0

        date_results.append({
            "date": date,
            "moyenne_par_matiere": moyenne_par_matiere,
            "moyenne_generale": round(moyenne_generale, 2),
            "class_moyenne_generale": round(class_moyenne_generale, 2)
        })

    return date_results


# Streamlit App
def run_streamlit_app(data, date_results):
    st.title("Downfall caught in 4k")

    # Overview
    st.header("Data Overview")
    st.write("Combined Data from JSON")
    st.dataframe(pd.DataFrame(data))

    # Subject-wise Averages
    st.header("Subject-wise Averages")
    moyenne_par_matiere = calculate_moyenne_par_matiere(data)
    st.write("Averages by Subject")
    st.json(moyenne_par_matiere)

    # Moyenne Générale Progression with Class Average
    st.header("Moyenne Générale vs Class Average Progression")
    moyenne_generale_over_time = pd.DataFrame({
        "Date": [res["date"] for res in date_results],
        "User Moyenne Générale": [res["moyenne_generale"] for res in date_results],
        "Class Moyenne Générale": [res["class_moyenne_generale"] for res in date_results]
    })
    st.line_chart(moyenne_generale_over_time.set_index("Date"))

    # User Mark vs Class Average
    st.header("User Mark vs. Class Average by Subject")
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
        title="User Mark vs. Class Average",
        hover_data=["Date", "Subject"]
    )
    st.plotly_chart(fig)

    # Subject Impact on Moyenne Générale
    st.header("Subject Impact on Moyenne Générale")
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

    # Detailed Analysis Per Date
    st.header("Detailed Analysis Per Date")
    for res in date_results:
        st.subheader(f"Date: {res['date']}")
        st.write("Moyenne Par Matière:")
        st.json(res["moyenne_par_matiere"])
        st.write(f"User Moyenne Générale: {res['moyenne_generale']}")
        st.write(f"Class Moyenne Générale: {res['class_moyenne_generale']}")



if __name__ == "__main__":
    # Load the dataset
    data = load_data("combined_marks.json")

    # Perform analysis
    date_results = calculate_moyenne_per_date(data)

    # Launch Streamlit app
    run_streamlit_app(data, date_results)
