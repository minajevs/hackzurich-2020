import { makeStyles } from '@material-ui/core';
import React, { useCallback, useEffect, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button, Header, Icon, Modal, Progress, Transition, TransitionablePortal } from 'semantic-ui-react'

export type Props = {
  open: boolean,
  onClose: () => void,
  onFinish: () => void,
  onOpen: () => void,
}

const useStyles = makeStyles({
  dropzone: {
    marginTop: '1em',
    padding: '3em',
    border: '3px dashed black',
    borderRadius: '10px',
    '&:focus': {
      outline: 'none'
    }
  },
  processing: {
    textAlign: 'center'
  }
});

type States = 'upload' | 'loading' | 'processing'

export const RecognitionModal: React.FC<Props> = ({ open, onClose, onOpen, onFinish }) => {
  const classes = useStyles()

  const [progress, setProgress] = useState(0)
  const [uploadVisible, setUploadVisible] = useState(true)
  const [loadingVisible, setLoadingVisible] = useState(false)
  const [processingVisible, setProcessingVisible] = useState(false)

  useEffect(
    () => {
      document.addEventListener('keydown', onFinish);
      return () => {
        document.removeEventListener('keydown', onFinish);
      };
    }, []
  );

  const onDrop = useCallback(acceptedFiles => {
    setUploadVisible(false)

    setTimeout(() => {
      setLoadingVisible(true)
      const int = setInterval(() => setProgress(prev => (prev + Math.random() * 20)), 100)
      setTimeout(() => {
        clearInterval(int)
        setLoadingVisible(false)
        setTimeout(() => setProcessingVisible(true), 500)
      }, 1500)
    }, 500)
  }, [])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })
  return (
    <>
      <style>{`
          .ui.dimmer {
            transition: background-color 0.5s ease;
            background-color: transparent;
          }

          .modal-fade-in .ui.dimmer {
            background-color: rgba(0, 0, 0, 0.84);
          }
        `}</style>
      <TransitionablePortal
        open={open}
        onOpen={() => setTimeout(() => document.body.classList.add('modal-fade-in'), 0)}
        transition={{ animation: 'fade down', duration: 500 }}
      >
        <Modal
          onClose={() => {
            document.body.classList.remove('modal-fade-in')
            onClose()
          }}
          open={true}

        >
          <Header icon>
            <Icon name='computer' />
            Apply home automation circuit
          </Header>
          <Modal.Content>
            <div>
              Upload a picture of a home automation circuit to automatically parse it into editable scheme. You will be able to review it before import.
            </div>
            <Transition visible={uploadVisible} unmountOnHide>
              <div {...getRootProps({
                className: classes.dropzone
              })}>
                <input {...getInputProps()} />
                {
                  isDragActive ?
                    <p>Drop the file here ...</p> :
                    <p>Drag 'n' drop file here, or click to select a file</p>
                }
              </div>
            </Transition>
            <Transition visible={loadingVisible} animation='scale' unmountOnHide>
              <Progress percent={progress} indicating />
            </Transition>
            <Transition visible={processingVisible} animation='scale'>
              <div className={classes.processing}>
                <Header as="h4">Processing</Header>
              </div>
            </Transition>
          </Modal.Content>
          <Modal.Actions>
            <Button basic onClick={onClose}>
              <Icon name='cancel' /> Cancel
        </Button>
          </Modal.Actions>
        </Modal>
      </TransitionablePortal>
    </>
  )
}

export default RecognitionModal