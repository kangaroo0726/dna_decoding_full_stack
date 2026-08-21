import "../App.css"

export function Results(props) {
  return (
    <div className="results">
      <p>{ props.converted }</p>
      <p>{ props.proteins }</p>
    </div>
  );
}