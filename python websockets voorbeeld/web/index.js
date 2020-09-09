const minus = document.querySelector(".minus");
const plus = document.querySelector(".plus");
const value = document.querySelector(".value");
const users = document.querySelector(".users");
const websocket = new WebSocket("ws://145.44.96.127:8766/");

websocket.onmessage = ({ data }) => {
  data = JSON.parse(data);
  console.log(data)
  const types = {
    state: () => (value.textContent = data.value),
    users: () => {
      users.textContent = `${data.count.toString()} user ${
        data.count === 1 ? "" : "s"
      }`;
    },
  };

  types[data.type] && types[data.type]();
};
