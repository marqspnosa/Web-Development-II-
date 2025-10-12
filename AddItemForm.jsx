import { useState } from "react";

function AddItemForm({ onAddItem }) {
  const [name, setName] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    onAddItem(name);
    setName("");
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter new item"
        style={{ marginRight: "0.5rem", padding: "0.4rem" }}
      />
      <button type="submit" style={{ padding: "0.4rem 1rem" }}>
        Add
      </button>
    </form>
  );
}

export default AddItemForm;