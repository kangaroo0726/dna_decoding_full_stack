import { useState } from "react";

function App() {
  const [strand, setStrand] = useState("");

  return (
    <div>
      <h1>DNA Decoder</h1>
      <textarea placeholder="Enter sequence"></textarea>
    </div>
  );
}

export default App;
