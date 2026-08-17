import { useState } from "react";

function App() {
  const [strand, setStrand] = useState("");
  const [strandType, setStrandType] = useState("template");
  const [currentOrientation, setOrientation] = useState(false);

  return (
    <div>
      <h1>DNA Decoder</h1>
      <textarea placeholder="Enter sequence" onChange={ (event) => setStrand(event.target.value) } value={ strand }></textarea>
      <select value={ strandType } onChange={ (event) => setStrandType(event.target.value) }>
        <option value="template">Template</option>
        <option value="coding">Coding</option>
        <option value="mrna">mRNA</option>
      </select>
      <input type="checkbox" checked={ currentOrientation } onChange={ (event) => setOrientation(event.target.checked) } id="orientation"/>
      <label htmlFor="orientation">Five to three</label>
    </div>
  );
}

export default App;
