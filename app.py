from flask import Flask, render_template, request, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Use a non-interactive backend to avoid threading issues
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Load the student data CSV
df = pd.read_csv('./data/student_data.csv')
df = df.drop("Unnamed: 0", axis=1)

# Helper function to convert plot to base64 string
def plot_to_base64(plt):
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()  # Close the plot to free memory
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for displaying graphs
@app.route('/plot/<string:graph_type>')
def plot(graph_type):
    img_base64 = ""
    
    # Gender Distribution Graph
    if graph_type == 'gender_distribution':
        plt.figure(figsize=(6, 4))  # Increase width to ensure title is fully visible
        ax = sns.countplot(data=df, x="Gender")
        ax.bar_label(ax.containers[0])
        plt.title("Gender Distribution")
        img_base64 = plot_to_base64(plt)

    # Parent's Education vs Student's Score (Bar Plot)
    elif graph_type == 'parent_educ_vs_score':
        plt.figure(figsize=(10, 6))

        # Group the data by Parent's Education and calculate mean scores
        gb = df.groupby("ParentEduc").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'}).reset_index()

        # Plot the scores as grouped bar charts
        bar_width = 0.2  # Width of the bars
        index = range(len(gb))  # Positions of the groups on the x-axis

        plt.bar(index, gb['MathScore'], width=bar_width, label='Math Score', color='green')
        plt.bar([i + bar_width for i in index], gb['ReadingScore'], width=bar_width, label='Reading Score', color='cyan')
        plt.bar([i + 2 * bar_width for i in index], gb['WritingScore'], width=bar_width, label='Writing Score', color='yellow')

        # Labels and title
        plt.xlabel("Parent's Education Level")
        plt.ylabel("Scores")
        plt.title("Student Scores Based on Parent's Education Level")

        # Set x-axis tick labels
        plt.xticks([i + bar_width for i in index], gb['ParentEduc'], rotation=45)

        # Add a legend
        plt.legend()

        # Convert plot to base64 string
        img_base64 = plot_to_base64(plt)


    # Parent's Marital Status vs Student's Score Heatmap
    elif graph_type == 'parent_marital_vs_score':
        gb1 = df.groupby("ParentMaritalStatus").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'}).dropna()
        plt.figure(figsize=(7, 5))  # Increase width
        sns.heatmap(gb1, annot=True)
        plt.title("Parent's Marital Status vs Student's Score")
        img_base64 = plot_to_base64(plt)

    # Ethnic Group Distribution Pie Chart
    elif graph_type == 'ethnic_distribution':
        groupA = df.loc[(df['EthnicGroup']=="group A")].count()
        groupB = df.loc[(df['EthnicGroup']=="group B")].count()
        groupC = df.loc[(df['EthnicGroup']=="group C")].count()
        groupD = df.loc[(df['EthnicGroup']=="group D")].count()
        groupE = df.loc[(df['EthnicGroup']=="group E")].count()
        
        l = ["group A","group B","group C","group D","group E"]
        mlist = [groupA["EthnicGroup"],groupB["EthnicGroup"],groupC["EthnicGroup"],groupD["EthnicGroup"],groupE["EthnicGroup"]]
        plt.figure(figsize=(6, 6))  # Increase width
        plt.pie(mlist, labels=l, autopct="%1.2f%%")
        plt.title("Distribution of Ethnic Group")
        img_base64 = plot_to_base64(plt)

    # Boxplot for MathScore
    elif graph_type == 'math_boxplot':
        plt.figure(figsize=(7, 5))  # Increase width
        sns.boxplot(data=df, x="MathScore")
        plt.title("Boxplot of Math Scores")
        img_base64 = plot_to_base64(plt)

    # Boxplot for ReadingScore
    elif graph_type == 'reading_boxplot':
        plt.figure(figsize=(7, 5))  # Increase width
        sns.boxplot(data=df, x="ReadingScore")
        plt.title("Boxplot of Reading Scores")
        img_base64 = plot_to_base64(plt)

    # Boxplot for WritingScore
    elif graph_type == 'writing_boxplot':
        plt.figure(figsize=(7, 5))  # Increase width
        sns.boxplot(data=df, x="WritingScore")
        plt.title("Boxplot of Writing Scores")
        img_base64 = plot_to_base64(plt)

    # Weekly Study Hours vs Score Heatmap
    elif graph_type == 'weekly_study_vs_score':
        gb3 = df.groupby("WklyStudyHours").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'})
        plt.figure(figsize=(7, 5))  # Increase width
        sns.heatmap(gb3, annot=True)
        plt.title("Relationship between Weekly Study Hours and Student's Score")
        img_base64 = plot_to_base64(plt)

    # Practice Sport vs Score Heatmap
    elif graph_type == 'practice_sport_vs_score':
        gb4 = df.groupby("PracticeSport").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'})
        plt.figure(figsize=(7, 5))  # Increase width
        sns.heatmap(gb4, annot=True)
        plt.title("Relationship between Practice Sport and Student's Score")
        img_base64 = plot_to_base64(plt)

    # Lunch Type vs Score Heatmap
    elif graph_type == 'lunch_type_vs_score':
        gb5 = df.groupby("LunchType").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'})
        plt.figure(figsize=(7, 5))  # Increase width
        sns.heatmap(gb5, annot=True)
        plt.title("Relationship between Lunch Type and Student's Score")
        img_base64 = plot_to_base64(plt)

    return jsonify({'img': img_base64})

# Route to fetch data of a specific student
@app.route('/student/<int:student_id>')
def get_student(student_id):
    if student_id >= 1 and student_id < len(df):
        student_data = df.iloc[student_id].to_dict()
        return jsonify(student_data)
    else:
        return jsonify({'error': 'Student not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
