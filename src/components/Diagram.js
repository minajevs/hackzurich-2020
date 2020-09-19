import React from "react";

import * as go from "gojs";
import { ReactDiagram } from "gojs-react";
import OrthogonalLinkReshapingTool from "./OrthogonalLinkReshapingTool";
import "./Diagram.css"; // contains .diagram-component CSS

const initDiagram = (nodeDataArray, linkDataArray) => () => {
  const $ = go.GraphObject.make;
  const diagram = $(go.Diagram, {
    "undoManager.isEnabled": true, // must be set to allow for model change listening
    // 'undoManager.maxHistoryLength': 0,  // uncomment disable undo/redo functionality
    linkReshapingTool: new OrthogonalLinkReshapingTool(),
    model: $(go.GraphLinksModel, {
      linkKeyProperty: "test", // IMPORTANT! must be defined for merges and data sync when using GraphLinksModel
      nodeDataArray,
      linkDataArray,
    }),
  });

  // define a simple Node template
  diagram.nodeTemplate = $(
    go.Node,
    "Auto",
    new go.Binding("location", "loc", go.Point.parse).makeTwoWay(
      go.Point.stringify
    ),
    $(
      go.Shape,
      "Circle",
      { name: "SHAPE", fill: "lightgray", strokeWidth: 2 },
      new go.Binding("stroke", "green").ofModel()
    ),
    $(
      go.TextBlock,
      { margin: 4, editable: false },
      new go.Binding("text").makeTwoWay()
    )
  );

  diagram.linkTemplate = $(
    go.Link,
    {
      routing: go.Link.AvoidsNodes,
      reshapable: true,
      resegmentable: true,
    },
    new go.Binding("points").makeTwoWay(),
    $(
      go.Shape,
      { strokeWidth: 3, fill: "blue" },
      new go.Binding("stroke", "black").ofModel()
    )
  );

  diagram.add(
    $(
      go.Part, // this Part is not bound to any model data
      {
        layerName: "Background",
        position: new go.Point(0, 0),
        selectable: false,
        pickable: false,
      },
      $(
        go.Picture,
        { source: `hata.png` }
      )
    )
  );

  diagram.addDiagramListener("ObjectDoubleClicked", function (ev) {
    console.log(ev.subject); //Successfully logs the node you clicked.
    console.log(ev.subject.ie); //Successfully logs the node's name.
  });

  diagram.addDiagramListener("InitialLayoutCompleted", function (e) {
    // select the Link in order to show its two additional Adornments, for shifting the ends
    diagram.links.first().isSelected = true;
  });

  return diagram;
};
// render function...
export default function Diagram(props) {
  const {
    nodeDataArray = [
      { key: 0, text: "Ts", loc: "200 0" },
      { key: 1, text: "Mxv2", loc: "400 0" },
      { key: 2, text: "P", loc: "500 0" },
      { key: 3, text: "Ts", loc: "600 0" },
      { key: 4, text: "C", loc: "600 200" },
      { key: 5, text: "Fs", loc: "400 200" },
      { key: 6, text: "G", loc: "0 200" },
    ],
    linkDataArray = [
      { from: "0", to: "1" },
      { from: "1", to: "2" },
      { from: "1", to: "4" },
      { from: "1", to: "5" },
      { from: "2", to: "3" },
      { from: "3", to: "4" },
      { from: "4", to: "5" },
      { from: "5", to: "6" },
      { from: "0", to: "6" },
    ],
  } = props;

  return (
    <ReactDiagram
      initDiagram={initDiagram(nodeDataArray, linkDataArray)}
      divClassName="diagram-component"
      onModelChange={console.log}

    />
  );
}
