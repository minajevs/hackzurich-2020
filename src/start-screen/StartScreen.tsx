import { makeStyles } from '@material-ui/core';
import React, { useCallback, useState } from 'react'
import { useHistory } from 'react-router-dom';
import { Button, Container, Header, Icon, Transition } from 'semantic-ui-react'

export type Props = {}

const useStyles = makeStyles({
  buttons: {
    padding: '3em'
  },
});

export const StartScreen: React.FC<Props> = ({ }) => {
  const [visible, setVisible] = useState(true)

  const classes = useStyles()
  const history = useHistory()

  const go = useCallback(() => {
    setVisible(false)
  }, [])

  return (
    <>
      <Container text textAlign="center">
        <Header as='h2'>Siemens img rcgnt</Header>
        <p>
          Jau sen ir noskaidrots fakts, ka aplūkojot maketa dizainu un kompozīciju teksta saturs novērš uzmanību. Lorem Ipsum izmanto tāpēc, kas tas nodrošina vairāk vai mazāk vienmērīgu burtu izvietojumu un padara to līdzīgu lasāmam tekstam angļu valodā, kas neizdodas, ja vienu un to pašu tekstu 'Šeit ir teksts, šeit ir teksts' atkārto. Daudzas maketēšanas un web lapu rediģēšanas programmas mūsdienās izmanto Lorem Ipsum kā standarta parauga tekstu un, izmantojot interneta meklēšanas programmās atslēgas vārdus "lorem ipsum", var redzēt cik daudz web lapu aizvien vēl gaida savu piedzimšanu. Pēdējo gadu laikā teksts Lorem Ipsum ieguvis dažādas versijas. Dažreiz tās radušās kļūdu dēļ, dažreiz – apzināti (piemēram, humoristiski un tiem līdzīgi varianti).
      </p>
      </Container>
      <Container textAlign="center" className={classes.buttons}>
        <Button animated color='teal' onClick={() => history.push('/diagram')}>
          <Button.Content visible>Start</Button.Content>
          <Button.Content hidden>
            <Icon name='arrow right' />
          </Button.Content>
        </Button>
      </Container>
    </>
  )
}

export default StartScreen