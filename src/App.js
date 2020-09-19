// App.js
import React from "react";

import Diagram from "./components/Diagram";
// render function...
export default function App() {
  const search = window.location.search;
  const params = new URLSearchParams(search);
  const nodeToHighlight = params.get("node");
  const editable = params.get("editable") || true;

  return (
    <div>
      <Diagram nodeToHighlight={nodeToHighlight} />
    </div>
  );
}
