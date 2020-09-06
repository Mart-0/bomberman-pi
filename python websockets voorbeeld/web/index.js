const minus = document.querySelector(".minus");
const plus = document.querySelector(".plus");
const value = document.querySelector(".value");
const users = document.querySelector(".users");
const websocket = new WebSocket("ws://192.168.2.20:8765/");

minus.onclick = () => websocket.send(JSON.stringify({ action: "minus" }));
plus.onclick = () => websocket.send(JSON.stringify({ action: "plus" }));

websocket.onmessage = ({ data }) => {
  data = JSON.parse(data);

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
