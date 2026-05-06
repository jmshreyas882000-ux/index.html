const API = "http://127.0.0.1:5000";

function login() {
  fetch(API + "/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      username: "admin",
      password: "admin"
    })
  })
  .then(res => res.json())
  .then(data => {
    localStorage.setItem("token", data.token);
    alert("Logged in");
  });
}

function addLead() {
  fetch(API + "/add-lead", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": localStorage.getItem("token")
    },
    body: JSON.stringify({
      name: document.getElementById("name").value,
      email: document.getElementById("email").value
    })
  })
  .then(() => alert("Lead added"));
}

function getLeads() {
  fetch(API + "/leads", {
    headers: {
      "Authorization": localStorage.getItem("token")
    }
  })
  .then(res => res.json())
  .then(data => {
    let list = document.getElementById("leads");
    list.innerHTML = "";
    data.forEach(l => {
      list.innerHTML += `<li>${l.name} - ${l.email}</li>`;
    });
  });
}

function chat() {
  fetch(API + "/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      message: document.getElementById("msg").value
    })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("reply").innerText = data.reply;
  });
}
