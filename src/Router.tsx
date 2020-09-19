import React from 'react'
import {
  BrowserRouter,
  Switch,
  Route,
  Link
} from "react-router-dom"

import StartScreen from './start-screen/StartScreen'
import DiagramScreen from './diagram-screen/DiagramScreen'
import { makeStyles } from '@material-ui/core/styles'

export type Props = {}

const useStyles = makeStyles({
  root: {
    padding: '30px'
  },
});

export const Router: React.FC<Props> = ({ }) => {
  const classes = useStyles()
  return (
    <div className={classes.root}>
      <BrowserRouter>
        <Switch>
          <Route path="/" exact>
            <StartScreen />
          </Route>
          <Route path="/diagram">
            <DiagramScreen />
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  )
}

export default Router