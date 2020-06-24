import { makeStyles } from '@material-ui/core/styles'
import MuiTextField from '@material-ui/core/TextField'
import React from 'react'

const useStyles = makeStyles(theme => ({
  warnText: {
    color: `${theme.palette.warning.dark}`
  }
}))

export const TextField = (props) => {
  const classes = useStyles()
  const { meta: { touched, error, warning } } = props
  return (
    <MuiTextField
      id={props.id}
      error={touched && error !== undefined}
      helperText={error !== undefined ? touched && error : warning !== undefined ? warning : null}
      FormHelperTextProps={{
        classes: {
          root: warning ? classes.warnText : undefined
        }
      }}
      placeholder={props.placeholder}
      label={props.label}
      required={props.required}
      InputProps={{
        inputProps: {
          tabIndex: props.tabIndex, min: props.min, max: props.max
        },
      }}
      {...props.input}
      {...props.custom}
    />
  )
}

TextField.defaultProps = {
  tabIndex: 0
}
