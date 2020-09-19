import { makeStyles } from "@material-ui/core";
// App.js
import React, { useState } from "react";
import { Confirm, Container, Grid } from "semantic-ui-react";

import Diagram from "../components/Diagram";
import { Menu } from "../components/Menu";
import RecognitionModal from "../components/RecognitionModal";

const useStyles = makeStyles({
  container: {
    padding: '3em'
  },
});

// render function...
export default function App() {
  const [confirmReset, setConfirmReset] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const classes = useStyles()


  const search = window.location.search;
  const params = new URLSearchParams(search);
  const nodeToHighlight = params.get("node");
  const editable = params.get("editable") || true;

  return (
    <>
      <Grid container>

        <Grid.Column width={4}>
          <Menu reset={() => setConfirmReset(true)} start={() => setModalOpen(true)} />
        </Grid.Column>
        <Grid.Column>
          <Diagram nodeToHighlight={nodeToHighlight} />
        </Grid.Column>

      </Grid>
      <RecognitionModal
        open={modalOpen}
        onOpen={() => setModalOpen(true)}
        onClose={() => setModalOpen(false)}
      />
      <Confirm
        open={confirmReset}
        onCancel={() => setConfirmReset(false)}
        onConfirm={() => setConfirmReset(false)}
      />
    </>
  );
}
