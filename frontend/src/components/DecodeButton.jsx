import "../App.css"

export function DecodeButton({ loading, decodeDna }) {
  return (
    <div className="decode-button">
      <button className="decode" disabled={ loading } onClick={ decodeDna }>{ loading ? "Decoding..." : "Decode"}</button>
    </div>
  );
}