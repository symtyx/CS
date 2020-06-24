import alertDuck from '../ducks/alerts'
import { combineReducers } from 'redux'
import inventoryDuck from '../ducks/inventory'
import productsDuck from '../ducks/products'
import { reducer as reduxFormReducer } from 'redux-form'

export default combineReducers({
  alerts: alertDuck,
  config: (state = {}, action) => state,
  form: reduxFormReducer,
  inventory: inventoryDuck,
  products: productsDuck
})