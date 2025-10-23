import { useContext, useEffect, useState } from "react";
import { api } from "../services/api";
import { AuthContext } from "../context/AuthContext";

export default function AdminPanel() {
  const { user } = useContext(AuthContext);
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", price_cents: 0, description: "" });

  const fetchProducts = async () => {
    const res = await api.get("/api/products");
    setProducts(res.data);
  };

  const createProduct = async () => {
    await api.post("/api/products", form);
    fetchProducts();
  };

  useEffect(() => { fetchProducts(); }, []);

  if (user.role !== "admin") return <p>Admins only</p>;

  return (
    <div className="container">
      <h2>Admin Panel</h2>
      <input placeholder="Name" onChange={(e) => setForm({ ...form, name: e.target.value })} />
      <input placeholder="Price (in cents)" onChange={(e) => setForm({ ...form, price_cents: Number(e.target.value) })} />
      <input placeholder="Description" onChange={(e) => setForm({ ...form, description: e.target.value })} />
      <button onClick={createProduct}>Add Product</button>

      <ul>
        {products.map((p) => (
          <li key={p.id}>{p.name} — ${(p.price_cents / 100).toFixed(2)}</li>
        ))}
      </ul>
    </div>
  );
}