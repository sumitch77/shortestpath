const form = document.getElementById("route-form");
const sourceSelect = document.getElementById("source");
const destinationSelect = document.getElementById("destination");
const swapBtn = document.getElementById("swap-btn");
const errorBox = document.getElementById("error");
const resultPanel = document.getElementById("result-panel");
const routeVisual = document.getElementById("route-visual");
const distanceEl = document.getElementById("distance");

function hideError() {
  errorBox.classList.add("hidden");
  errorBox.textContent = "";
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
  resultPanel.classList.add("hidden");
}

function renderRoute(route) {
  routeVisual.innerHTML = "";

  route.forEach((city, index) => {
    const step = document.createElement("div");
    step.className = "route-step";

    const node = document.createElement("div");
    node.className = "city-node";
    if (index === 0) node.classList.add("start");
    if (index === route.length - 1) node.classList.add("end");
    node.textContent = city;
    step.appendChild(node);

    if (index < route.length - 1) {
      const arrow = document.createElement("div");
      arrow.className = "route-arrow";
      arrow.textContent = "↓";
      step.appendChild(arrow);
    }

    routeVisual.appendChild(step);
  });
}

swapBtn.addEventListener("click", () => {
  const temp = sourceSelect.value;
  sourceSelect.value = destinationSelect.value;
  destinationSelect.value = temp;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();

  const source = sourceSelect.value;
  const destination = destinationSelect.value;

  if (!source || !destination) {
    showError("Please select both source and destination cities.");
    return;
  }

  const submitBtn = form.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = "Finding route…";

  try {
    const response = await fetch("/api/route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, destination }),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    renderRoute(data.route);
    distanceEl.textContent = `${data.distance.toFixed(2)} km`;
    resultPanel.classList.remove("hidden");
  } catch {
    showError("Could not reach the server. Is the app running?");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Find Shortest Route";
  }
});
