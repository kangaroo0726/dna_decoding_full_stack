import "../App.css"

export function DecodeButton(props) {
  return (
    <div className="decode-button">
      <button className="decode" disabled={ props.loading } onClick={ props.decodeDna }>{ props.loading ? "Decoding..." : "Decode"}</button>
    </div>
  );
}