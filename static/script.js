async function classifyQuestion() {

    const question =
        document.getElementById("question").value.trim();

    const result =
        document.getElementById("result");


    // Check empty question

    if (!question) {

        result.innerHTML =
            "<p>Please enter a question.</p>";

        return;
    }


    // Loading message

    result.innerHTML =
        "<p>Analyzing your question...</p>";


    try {

        const response = await fetch(
            "/classify",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data = await response.json();


        // Error

        if (data.error) {

            result.innerHTML =
                `<p>${data.error}</p>`;

            return;
        }


        // ------------------------------------------
        // INTENTS
        // ------------------------------------------

        let intentHTML = "";

        data.intents.forEach(function(intent) {

            intentHTML += `
                <span class="intent-tag">
                    ${intent}
                </span>
            `;

        });


        // ------------------------------------------
        // ACTIONS
        // ------------------------------------------

        let actionHTML = "<ul>";

        data.actions.forEach(function(action) {

            actionHTML += `
                <li>${action}</li>
            `;

        });

        actionHTML += "</ul>";


        // ------------------------------------------
        // DISPLAY RESULT
        // ------------------------------------------

        result.innerHTML = `

            <h2>Analysis Result</h2>


            <div class="result-section">

                <strong>Detected Intents</strong>

                <div class="intent-container">
                    ${intentHTML}
                </div>

            </div>


            <div class="result-item">

                <strong>Subject</strong>

                <span>
                    ${data.subject}
                </span>

            </div>


            <div class="result-item">

                <strong>Topic</strong>

                <span>
                    ${data.topic}
                </span>

            </div>


            <div class="result-section">

                <strong>Recommended Actions</strong>

                ${actionHTML}

            </div>

        `;

    }


    catch (error) {

        result.innerHTML =
            "<p>Unable to connect to the server.</p>";

        console.error(error);

    }

}