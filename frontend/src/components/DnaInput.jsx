export function DnaInput(props) {
  async function getFileContents(file) {
    const fileText = await file.text();
    return fileText;
  }

  return (
  <div>
      <textarea placeholder="Enter sequence" onChange={ (event) => props.setStrand(event.target.value) } value={ props.strand }></textarea>
      <input type="file" onChange={ async (event) => { const fileText = await getFileContents(event.target.files[0]);
        props.setStrand(fileText)
       } } id="fileUpload"/>
      <label htmlFor="fileUpload">Upload DNA File</label>
      <select value={ props.strandType } onChange={ (event) => props.setStrandType(event.target.value) }>
        <option value="template">Template</option>
        <option value="coding">Coding</option>
        <option value="mrna">mRNA</option>
      </select>
      <input type="checkbox" checked={ props.fiveToThree } onChange={ (event) => props.setFiveToThree(event.target.checked) } id="orientation"/>
      <label htmlFor="orientation">Five to three</label>
   </div>   
  );
}