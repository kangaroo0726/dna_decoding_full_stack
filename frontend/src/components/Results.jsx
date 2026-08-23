import "../App.css"

export function Results({ converted, proteins }) {
  return (
    <div className="results">
    <div className="result-group">
      <label htmlFor="converted">Converted</label>
      <textarea id="converted" className="result-output" placeholder="converted" readOnly value={ converted }></textarea>
    </div>
    <div className="result-group">
      <label htmlFor="proteins">Proteins</label>
      <textarea id="proteins" className="result-output" placeholder="proteins" readOnly value={ proteins }></textarea>
    </div>
    </div>
  );
}