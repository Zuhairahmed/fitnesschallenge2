import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import {
  Container,
  Stack,
  Box,
  Image,
  Heading,
  Table,
  Thead,
  Th,
  Tr,
  Td,
  Tbody,
  Button,
} from '@chakra-ui/react'
import Animal from '../../models/Animal'
import useAnimalNews from './useAnimalNews'

const SUCCESS = 'SUCCESS'
const FAILURE = 'FAILURE'

export default function AnimalDetail() {
  const { animalId } = useParams()

  const { news, fetchAnimalNews } = useAnimalNews(`/get-animal-news-by-id?animalId=${animalId}`)

  const [animal, setAnimal] = useState()
  const [status, setStatus] = useState()

  const adoptAnimal = async () => {
    try {
      const response = await fetch('/adopt-animal', {
        method: 'POST',
        headers: {
          'Content-type': 'application/json',
        },
        body: JSON.stringify({ animalId }),
      }).then((res) => res.json())

      animal.afterAdoptionRequestSucceeded()
      setAnimal({ ...animal })
    } catch (e) {
      console.error(e)
    }
  }

  useEffect(async () => {
    try {
      const response = await fetch(`/get-animal-details-by-id?animalId=${animalId}`).then((res) =>
        res.json()
      )
      setAnimal(new Animal(response))

      await fetchAnimalNews()

      setStatus(SUCCESS)
    } catch (e) {
      setStatus(FAILURE)
    }
  }, [])

  if (!animal && !status) {
    return <div>loading...</div>
  }

  if (status === FAILURE) {
    return <div>Not Found</div>
  }

  return (
    <Container centerContent p="2">
      <Stack>
        <Box>
          <Heading size="lg">{animal.name}</Heading>
        </Box>
        <Image
          w="80%"
          src={animal.imageLink}
          fallbackSrc="https://via.placeholder.com/300?text=no%20photo"
        />
        <Box>
          <Heading size="md" mb="2">
            Status
          </Heading>
          {animal.adoptionStatus}
          <Button ml="10" disabled={!animal.available} colorScheme="teal" onClick={adoptAnimal}>
            Adopt this animal
          </Button>
        </Box>
        <Box>
          <Heading size="md" mb="2">
            Age
          </Heading>
          {animal.age}
        </Box>
        <Box>
          <Heading size="md" md="2">
            Description
          </Heading>
          {animal.description}
        </Box>
        <Box>
          <Heading size="md" mb="2">
            Dispositions
          </Heading>
          <Box pl="5">
            <ul>
              {animal.dispositions.map((e) => (
                <li key={e}>{e}</li>
              ))}
            </ul>
          </Box>
        </Box>
        <Box>
          <Heading size="md" mb="2">
            Class
          </Heading>
          {animal.animalClass}
        </Box>
        <Box>
          <Heading size="md" mb="2">
            Breed
          </Heading>
          {animal.animalBreed}
        </Box>
        <Box mt="2" mb="3">
          creation date: {animal.creationDate}
        </Box>

        <hr />
        <Box>
          <Heading size="md" mt="5">
            News Items
          </Heading>
          <Table variant="simple" mt="2">
            <Tbody>
              {news.map((e) => (
                <Tr key={e.id}>
                  <Th>{e.date}</Th>
                  <Td>{e.text}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>

        <Box borderWidth="1px" borderRadius="lg" p="5" boxShadow="lg">
          <Heading size="md">Shelter Info</Heading>
          <Table variant="simple" mt="2">
            <Tbody>
              <Tr>
                <Th>Name</Th>
                <Td>{animal.shelter?.name}</Td>
              </Tr>
              <Tr>
                <Th>Physical Address</Th>
                <Td>{animal.shelter?.physical_address}</Td>
              </Tr>
              <Tr>
                <Th>Phone Number</Th>
                <Td>{animal.shelter?.phone_number}</Td>
              </Tr>
              <Tr>
                <Th>Email Address</Th>
                <Td>{animal.shelter?.email_address}</Td>
              </Tr>
            </Tbody>
          </Table>
        </Box>
      </Stack>
    </Container>
  )
}
