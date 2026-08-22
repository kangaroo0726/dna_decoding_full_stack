import "../App.css"

export function Results(props) {
  return (
    <div className="results">
    <div className="result-group">
      <label htmlFor="converted">Converted</label>
      <textarea id="converted" className="result-output" placeholder="converted" readOnly value={ props.converted }></textarea>
    </div>
    <div className="result-group">
      <label htmlFor="proteins">Proteins</label>
      <textarea id="proteins" className="result-output" placeholder="proteins" readOnly value={ props.proteins }></textarea>
    </div>
    </div>
  );
}