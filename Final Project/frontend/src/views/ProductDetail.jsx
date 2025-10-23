import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../services/api";

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    api.get(`/api/products/${id}`).then((res) => setProduct(res.data));
  }, [id]);

  if (!product) return <p>Loading...</p>;

  return (
    <div className="container">
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p><strong>${(product.price_cents / 100).toFixed(2)}</strong></p>
    </div>
  );
}