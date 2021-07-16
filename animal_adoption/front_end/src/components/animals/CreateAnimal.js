import { Container, Heading, Button } from '@chakra-ui/react'
import { useState } from 'react'
import { useHistory } from 'react-router-dom'
import Animal from '../../models/Animal'
import FormEditAnimal from './FormEditAnimal'

export default function CreateAnimal() {
  const [animal, setAnimal] = useState(new Animal())

  const history = useHistory()

  const submit = async () => {
    const { imageData, ...data } = animal

    const formData = new FormData()
    formData.append('data', JSON.stringify(data))
    formData.append('image', imageData)

    const response = await fetch('/create-animal', {
      method: 'POST',
      body: formData,
    }).then((res) => res.json())

    history.push('/')
  }

  return (
    <Container mt="2" centerContent>
      <Heading mb="2">Create new animal profile</Heading>
      <FormEditAnimal animal={animal} setAnimal={setAnimal} />
      <Button mt="5" colorScheme="teal" onClick={submit}>
        Submit
      </Button>
    </Container>
  )
}
