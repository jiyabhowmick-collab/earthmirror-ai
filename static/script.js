// ==============================
// EarthMirror AI - Frontend Logic
// ==============================

let currentCarbonScore = null;
let currentImpactLevel = null;


// ==============================
// Calculate Carbon Footprint
// ==============================

async function calculateFootprint() {

    const travel = document.getElementById("travel").value;
    const electricity = document.getElementById("electricity").value;
    const food = document.getElementById("food").value;
    const shopping = document.getElementById("shopping").value;

    // Validation

    if (
        travel === "" ||
        electricity === "" ||
        food === "" ||
        shopping === ""
    ) {

        alert("Please fill all fields.");

        return;
    }

    try {

        const response = await fetch("/calculate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                travel,
                electricity,
                food,
                shopping
            })

        });

        const data = await response.json();

        if (data.success) {

            currentCarbonScore = data.carbon_score;
            currentImpactLevel = data.impact_level;

            document.getElementById("carbonScore").innerText =
                data.carbon_score;

            document.getElementById("impactLevel").innerText =
                `Impact Level: ${data.impact_level}`;

            showSuccessMessage(
                "Carbon footprint calculated successfully."
            );

        } else {

            alert(data.error);

        }

    } catch (error) {

        console.error(error);

        alert(
            "Something went wrong while calculating your carbon footprint."
        );
    }
}


// ==============================
// AI Sustainability Coach
// ==============================

async function getInsights() {

    if (!currentCarbonScore) {

        alert(
            "Please calculate your carbon footprint first."
        );

        return;
    }

    const output = document.getElementById("aiInsights");

    output.innerText =
        "Generating personalized sustainability insights...";

    try {

        const response = await fetch("/ai-insights", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                carbon_score: currentCarbonScore,

                impact_level: currentImpactLevel

            })

        });

        const data = await response.json();

        if (data.success) {

            output.innerText = data.insights;

        } else {

            output.innerText =
                "Unable to generate insights.";

            alert(data.error);
        }

    } catch (error) {

        console.error(error);

        output.innerText =
            "An error occurred while generating insights.";
    }
}


// ==============================
// Future Earth Simulator
// ==============================

async function simulateFuture() {

    if (!currentCarbonScore) {

        alert(
            "Please calculate your carbon footprint first."
        );

        return;
    }

    const output =
        document.getElementById("futureSimulation");

    output.innerText =
        "Analyzing future environmental impact...";

    try {

        const response = await fetch("/future-simulation", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                carbon_score: currentCarbonScore

            })

        });

        const data = await response.json();

        if (data.success) {

            output.innerText =
                data.simulation;

        } else {

            output.innerText =
                "Unable to generate simulation.";

            alert(data.error);
        }

    } catch (error) {

        console.error(error);

        output.innerText =
            "An error occurred while generating future projections.";
    }
}


// ==============================
// Helper Function
// ==============================

function showSuccessMessage(message) {

    const oldMessage =
        document.getElementById("successMessage");

    if (oldMessage) {

        oldMessage.remove();
    }

    const div = document.createElement("div");

    div.id = "successMessage";

    div.innerText = message;

    div.style.background = "#dcfce7";
    div.style.color = "#166534";
    div.style.padding = "12px";
    div.style.marginTop = "15px";
    div.style.borderRadius = "8px";
    div.style.textAlign = "center";
    div.style.fontWeight = "600";

    const resultCard =
        document.querySelector(".result-card");

    resultCard.appendChild(div);

    setTimeout(() => {

        const msg =
            document.getElementById("successMessage");

        if (msg) {

            msg.remove();
        }

    }, 3000);
}


// ==============================
// Smooth Startup Log
// ==============================

window.addEventListener("load", () => {

    console.log(
        "🌍 EarthMirror AI Loaded Successfully"
    );

});