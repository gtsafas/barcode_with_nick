import logo from "./logo.svg";
import { useEffect, useState } from "react";
import "./App.css";

function Inventory({ items }) {
  return items.map((item) => <div key={item.name}>{item.name}</div>);
}

function App() {
  const [items, setItems] = useState([]);
  const [lastUploadedId, setLastUploadedId] = useState("");

  useEffect(() => {
    fetch("http://localhost:8888/items")
      .then((r) => r.json())
      .then((d) => setItems(d));
  }, []);

  function onFileChanged(event) {
    const file = event.target.files[0];

    const formData = new FormData();
    formData.append("barcode_image", file, file.name);

    fetch("http://localhost:8888/upload", {
      method: "POST",
      body: formData,
    })
      .then((r) => r.json())
      .then((d) => {
        setLastUploadedId(d.product);
      });
  }

  return (
    <div className="App">
      <div>Last uploaded: {lastUploadedId}</div>
      <Inventory items={items} />
      <input type="file" onChange={onFileChanged} />
    </div>
  );
}

export default App;
