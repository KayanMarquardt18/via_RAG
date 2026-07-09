import bhGif from "../assets/blackhole.gif";

export default function BlackHole() {
  return (
    <div style={{
      position: "fixed",
      inset: 0,
      zIndex: -1,
      background: "#000",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      overflow: "hidden",
    }}>
      <img
        src={bhGif}
        alt=""
        style={{
          width: "70%",
          maxWidth: "800px",
          opacity: 0.85,
        }}
      />
    </div>
  );
}