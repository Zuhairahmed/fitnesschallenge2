import { useContext } from 'react'
import UserContext from '../components/users/UserContext'
import LandingBeforeLogin from '../components/landing/LandingBeforeLogin'
import LandingForAdopters from '../components/landing/LandingForAdopters'
import LandingForShelters from '../components/landing/LandingForShelters'
import LandingForAdmins from '../components/landing/LandingForAdmins'
import User from '../models/User'

export default function Landing() {
  /** @type {{user: User}} */
  const { user } = useContext(UserContext)

  if (user?.isAdopter) {
    return <LandingForAdopters />
  }
  if (user?.isShelterWorker) {
    return <LandingForShelters />
  }
  if (user?.isAdministrator) {
    return <LandingForAdmins />
  }

  return <LandingBeforeLogin />
}
