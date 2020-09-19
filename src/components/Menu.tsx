import React, { useCallback, useState } from 'react'
import { Label, Menu as SemanticMenu } from 'semantic-ui-react'

type Props = {
  start: () => void,
  reset: () => void
}

export const Menu: React.FC<Props> = ({ start, reset }) => {
  return (
    <SemanticMenu vertical>
      <SemanticMenu.Item
        active={false}
        onClick={start}
      >
        Upload automation scheme
      </SemanticMenu.Item>

      <SemanticMenu.Item
        active={false}
        onClick={reset}
      >
        Reset
      </SemanticMenu.Item>
    </SemanticMenu>
  )
}

export default Menu