const minus = document.querySelector(".minus");
const plus = document.querySelector(".plus");
const value = document.querySelector(".value");
const users = document.querySelector(".users");
const websocket = new WebSocket(config.host);

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