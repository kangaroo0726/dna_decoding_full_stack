export function DnaInput(props) {
  return (
  <div>
      <textarea placeholder="Enter sequence" onChange={ (event) => props.setStrand(event.target.value) } value={ props.strand }></textarea>
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