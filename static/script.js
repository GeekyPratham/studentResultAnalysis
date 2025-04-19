// Function to display the graph based on button clicks
function showGraph(graphType) {
    fetch(`/plot/${graphType}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('plot').src = 'data:image/png;base64,' + data.img;
        });
}

// Function to fetch and display student data
function getStudentData() {
    const studentId = document.getElementById('student-id').value;
    if (studentId) {
        fetch(`/student/${studentId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('student-info').innerHTML = '<p>Student not found!</p>';
                } else {
                    let info = `<p><strong>Gender:</strong> ${data.Gender}</p>`;
                    info += `<p><strong>Ethnic Group:</strong> ${data.EthnicGroup}</p>`;
                    info += `<p><strong>Parent's Education:</strong> ${data.ParentEduc}</p>`;
                    info += `<p><strong>Lunch Type:</strong> ${data.LunchType}</p>`;
                    info += `<p><strong>Test Prep:</strong> ${data.TestPrep}</p>`;
                    info += `<p><strong>Parent's Marital Status:</strong> ${data.ParentMaritalStatus}</p>`;
                    info += `<p><strong>Practice Sport:</strong> ${data.PracticeSport}</p>`;
                    info += `<p><strong>Is First Child:</strong> ${data.IsFirstChild}</p>`;
                    info += `<p><strong>Number of Siblings:</strong> ${data.NrSiblings}</p>`;
                    info += `<p><strong>Transport Means:</strong> ${data.TransportMeans}</p>`;
                    info += `<p><strong>Weekly Study Hours:</strong> ${data.WklyStudyHours}</p>`;
                    info += `<p><strong>Math Score:</strong> ${data.MathScore}</p>`;
                    info += `<p><strong>Reading Score:</strong> ${data.ReadingScore}</p>`;
                    info += `<p><strong>Writing Score:</strong> ${data.WritingScore}</p>`;
                    document.getElementById('student-info').innerHTML = info;
                }
            });
    }
}
