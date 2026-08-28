import "./App.css";
import { useState } from "react";
import { DnaInput } from "./components/DnaInput.jsx"
import { DecodeButton } from "./components/DecodeButton.jsx"
import { Results } from "./components/Results.jsx";

function App() {
  const [strand, setStrand] = useState("");
  const [strandType, setStrandType] = useState("template");
  const [fiveToThree, setFiveToThree] = useState(false);
  const [converted, setConverted] = useState("");
  const [proteins, setProteins] = useState("");
  const [loading, setLoading] = useState(false);

  function setResultMessage(message) {
    setConverted(message);
    setProteins(message);
  }

  async function decodeDna() {
    setConverted("");
    setProteins("");
    setLoading(true);
    const requestObject = {
      strand,
      strand_type: strandType,
      five_to_three: fiveToThree,
    };
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/decode`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestObject),
      });
      if (!response.ok) {
        const errorData = await response.json();
        setResultMessage(errorData.detail);
        return;
      }

      const data = await response.json();
      setConverted(data.converted);
      setProteins(data.proteins.join(", "));

    } catch {
      setResultMessage("Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <h1>DNA Decoder</h1>
      <DnaInput strand={ strand } setStrand={ setStrand } strandType={ strandType } setStrandType={ setStrandType } fiveToThree={ fiveToThree } setFiveToThree={ setFiveToThree }/>
      <DecodeButton loading={ loading } decodeDna={ decodeDna }/>
      <Results converted={ converted } proteins={ proteins }/>
    </div>
  );
}

export default App;
