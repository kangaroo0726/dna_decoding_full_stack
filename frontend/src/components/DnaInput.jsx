import "../App.css"

export function DnaInput({ strand, setStrand, strandType, setStrandType, fiveToThree, setFiveToThree }) {
  async function getFileContents(file) {
    const fileText = await file.text();
    return fileText;
  }

  return (
  <div className="dna-input">
      <textarea className="text-input" placeholder="Enter sequence" onChange={ (event) => setStrand(event.target.value) } value={ strand }></textarea>
      <h2 className="divider">OR</h2>
      <div className="files">
        <input className="file-input" accept=".txt" type="file" onChange={ async (event) => { const fileText = await getFileContents(event.target.files[0]);
          setStrand(fileText)
        } } id="fileUpload"/>
        <label className="file-input-label" htmlFor="fileUpload">Upload DNA File</label>
        <label className="file-input-box" htmlFor="fileUpload">Upload DNA File</label>
      </div>
      <select className="type-select" value={ strandType } onChange={ (event) => setStrandType(event.target.value) }>
        <option value="template">Template</option>
        <option value="coding">Coding</option>
        <option value="mrna">mRNA</option>
      </select>
      <div className="orientation">
        <input className="orientation-select" type="checkbox" checked={ fiveToThree } onChange={ (event) => setFiveToThree(event.target.checked) } id="orientation"/>
        <label className="orientation-select-label" htmlFor="orientation">Five to three</label>
      </div>
   </div>   
  );
}