const minus = document.querySelector(".minus");
const plus = document.querySelector(".plus");
const value = document.querySelector(".value");
const users = document.querySelector(".users");
const websocket = new WebSocket("ws://145.44.96.127:8766/");

websocket.onmessage = ({ data }) => {
  data = JSON.parse(data);

  const types = {
    users: () => userCount(data),
    players: () => displayPlayers(data),
  };

  types[data.type] && types[data.type]();
};

function userCount(data) {
  console.log('user data!')
  console.log(data)
}

function displayPlayers(data) {
  console.log('user data!')
  console.log(data)
}

function pageInfo() {
  // testing
  var node = document.createElement("LI");
  var textnode = document.createTextNode("Water");
  node.appendChild(textnode);
  document.getElementById("myList").appendChild(node);
}