import { useState } from "react";

function App() {
  const [strand, setStrand] = useState("");
  const [strandType, setStrandType] = useState("template");
  const [fiveToThree, setFiveToThree] = useState(false);
  const [converted, setConverted] = useState("");
  const [proteins, setProteins] = useState("");
  const [loading, setLoading] = useState(false);

  async function decodeDna() {
    setConverted("decoding");
    setLoading(true);
    const requestObject = { "strand": strand, 
                            "strand_type": strandType, 
                            "five_to_three": fiveToThree }
    try {
      const response = await fetch("http://127.0.0.1:8000/decode", { method: "POST", 
                                                                      headers: { "Content-Type": "application/json" }, 
                                                                      body: JSON.stringify(requestObject) })
      if (!response.ok) {
        console.log(response);
        const errorData = await response.json();
        setConverted(errorData.detail);
        throw new Error(`HTTP Error Status: ${response.status}`)
      }

      const data = await response.json();
      setConverted(data.converted);
      setProteins(data.proteins.join(", "))

      console.log(data);
    } catch (error) {
      console.log(`Fetch failed: ${error}`)
      setProteins("");
    }
    setLoading(false);
  }

  return (
    <div>
      <h1>DNA Decoder</h1>
      <textarea placeholder="Enter sequence" onChange={ (event) => setStrand(event.target.value) } value={ strand }></textarea>
      <select value={ strandType } onChange={ (event) => setStrandType(event.target.value) }>
        <option value="template">Template</option>
        <option value="coding">Coding</option>
        <option value="mrna">mRNA</option>
      </select>
      <input type="checkbox" checked={ fiveToThree } onChange={ (event) => setFiveToThree(event.target.checked) } id="orientation"/>
      <label htmlFor="orientation">Five to three</label>
      <button disabled={ loading } onClick={ decodeDna }>Decode</button>
      <p>{converted}</p>
      <p>{proteins}</p>
    </div>
  );
}

export default App;
