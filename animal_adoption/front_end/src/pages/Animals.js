import { Switch, Route, useRouteMatch } from 'react-router-dom'
import AnimalDetail from '../components/animals/AnimalDetail'
import CreateAnimal from '../components/animals/CreateAnimal'

export default function Animals() {
  const match = useRouteMatch()

  return (
    <Switch>
      <Route path={`${match.path}/create`}>
        <CreateAnimal />
      </Route>
      <Route path={`${match.path}/:animalId`}>
        <AnimalDetail />
      </Route>
    </Switch>
  )
}
