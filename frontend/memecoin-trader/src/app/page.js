'use client';

import axios from 'axios';
import { useEffect, useState } from 'react';

export default function Home() {
  const [memecoins, setMemecoins] = useState([]);

  useEffect(() => {
    // Fetch data from the Python backend
    axios.get('http://localhost:3100/api/memecoins')
      .then(response => {
        console.log("Data fetched:", response.data);
        setMemecoins(response.data);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div>
      <h1>Memecoin Trading Dashboard</h1>
      <ul>
        {memecoins.map(coin => (
          <li key={coin.name}>
            <h3>{coin.name}</h3>
            <p>Price: ${coin.price}</p>
            <p>Volume Change: {coin.volume_change}%</p>
            <button onClick={() => handleTrade('buy', coin.name)}>Buy</button>
            <button onClick={() => handleTrade('sell', coin.name)}>Sell</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

const handleTrade = async (action, coinName) => {
  try {
    await axios.post('http://localhost:3100/api/trade', {
      action,
      coin: coinName,
    });
    alert(`${action.toUpperCase()} order for ${coinName} placed successfully.`);
  } catch (error) {
    console.error("Error executing trade:", error);
    alert("Failed to execute trade.");
  }
};

