import { useEffect, useState } from "react";
import { api } from "../services/api";
import { Link } from "react-router-dom";

export default function Home() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    api.get("/api/products").then((res) => setProducts(res.data));
  }, []);

  return (
    <div className="container">
      <h1>Products</h1>
      <div className="grid">
        {products.map((p) => (
          <div key={p.id} className="card">
            <h3>{p.name}</h3>
            <p>${(p.price_cents / 100).toFixed(2)}</p>
            <Link to={`/product/${p.id}`}>View</Link>
          </div>
        ))}
      </div>
    </div>
  );
}