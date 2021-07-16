import { Flex, Center, Button, Divider } from '@chakra-ui/react'
import React from 'react'
import SignupFormUser from '../components/SignupFormUser'
import SignupFormShelterWorker from '../components/SignupFormShelterWorker'

function SignupPage() {
  const [showAdopter, setAdopterState] = React.useState(false)
  const [showShelterWorker, setShelterWorkerState] = React.useState(false)

  return (
    <Flex justifyContent="center" mt="5">
      <div>
        <Center>
          <b> Sign up Page </b>
        </Center>
        <br />
        <Center>
          <Button
            colorScheme="green"
            type="button"
            onClick={() => {
              setAdopterState(true)
              setShelterWorkerState(false)
            }}
          >
            Register as Adopter
          </Button>
        </Center>
        <br />
        <Center>
          <Button
            colorScheme="green"
            type="button"
            onClick={() => {
              setShelterWorkerState(true)
              setAdopterState(false)
            }}
          >
            Register as Shelter Worker
          </Button>
        </Center>
        <br />

        {showAdopter ? <SignupFormUser /> : null}

        {showShelterWorker ? <SignupFormShelterWorker /> : null}
      </div>
    </Flex>
  )
}

export default SignupPage
