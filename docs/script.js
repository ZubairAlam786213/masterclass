const API = "https://profile-backend-uavf.onrender.com";

async function loadProjects() {
  const container = document.getElementById("project-list");

  try {
    const response = await fetch(`${API}/api/projects`);

    const projects = await response.json();

    container.innerHTML = "";

    projects.forEach((project) => {
      container.innerHTML += `

            <div class="card">

                <h3>${project.title}</h3>

                <p>${project.description}</p>

                <br>

                <strong>Tech Stack</strong>

                <p>${project.tech_stack.join(", ")}</p>

                <br>

                <a href="${project.live_url}" target="_blank">
                    View Project
                </a>

            </div>

            `;
    });
  } catch {
    container.innerHTML = "Unable to load projects.";
  }
}

loadProjects();

const form = document.getElementById("contactForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const status = document.getElementById("status");

  status.innerHTML = "Sending...";

  const data = {
    name: document.getElementById("name").value,

    email: document.getElementById("email").value,

    message: document.getElementById("message").value,
  };

  try {
    const response = await fetch(`${API}/api/contact`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      status.innerHTML = result.message;

      form.reset();
    } else {
      status.innerHTML = result.detail;
    }
  } catch {
    status.innerHTML = "Unable to connect to server.";
  }
});