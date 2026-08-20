export function DecodeButton(props) {
  return (
    <div>
      <button disabled={ props.loading } onClick={ props.decodeDna }>Decode</button>
    </div>
  );
}