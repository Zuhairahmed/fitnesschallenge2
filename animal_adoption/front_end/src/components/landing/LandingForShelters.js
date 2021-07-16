import {
  Button,
  Image,
  Box,
  Stack,
  Heading,
  Flex,
  Spinner,
  Container,
  Table,
  Thead,
  Th,
  Tr,
  Td,
  Tbody,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  Text,
} from '@chakra-ui/react'
import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Animal from '../../models/Animal'
import Drawer from '../common/Drawer'
import FormEditAnimal from '../animals/FormEditAnimal'
import useAnimalNews from '../animals/useAnimalNews'

function NewsItemModal({ animal }) {
  const { onOpen: _onOpen, isOpen, onClose } = useDisclosure()

  const { news, fetchAnimalNews } = useAnimalNews(`/get-animal-news-by-id?animalId=${animal.id}`)

  const [newsText, setNewsText] = useState('')

  function handleChange(event) {
    setNewsText(event.target.value)
  }

  async function postNewsItem() {
    try {
      await fetch('/create-animal-news-item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ animalId: animal.id, newsText }),
      })

      setNewsText('')

      await fetchAnimalNews()
    } catch (e) {
      console.error(e)
    }
  }

  async function onOpen() {
    await fetchAnimalNews()
    _onOpen()
  }

  return (
    <>
      <Button mt="1" colorScheme="gray" onClick={onOpen}>
        + Add news item
      </Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>News Items: {animal.name}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box ml="5">
              <ul>
                {news.map((e) => (
                  <li key={`${e.id}`}>
                    {e.text} - {e.date}
                  </li>
                ))}
              </ul>
            </Box>
            <FormControl mt="5">
              <FormLabel>Add news item</FormLabel>
              <InputGroup>
                <Input onChange={handleChange} placeholder="news item" value={newsText} />
                <Button disabled={newsText === ''} ml="1" colorScheme="blue" onClick={postNewsItem}>
                  Add
                </Button>
              </InputGroup>
            </FormControl>
          </ModalBody>

          <ModalFooter>
            <Button color="gray.800" onClick={onClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default function LandingForShelters() {
  const [animals, setAnimals] = useState(null)
  const [selectedAnimal, setSelectedAnimal] = useState()
  const { isOpen, onOpen, onClose: _onClose } = useDisclosure()

  useEffect(async () => {
    try {
      const { message } = await fetch('/get-animals-of-shelter').then((res) => res.json())
      if (message) {
        setAnimals(JSON.parse(message).map((e) => new Animal(e)))
      }
    } catch (e) {
      setAnimals([])
      console.error(e)
    }
  }, [])

  const editAnimal = (animal) => {
    setSelectedAnimal({ ...animal })
    onOpen()
  }

  const onClose = () => {
    setSelectedAnimal()
    _onClose()
  }

  const onSave = async () => {
    const { imageData, ...data } = selectedAnimal

    const formData = new FormData()
    formData.append('data', JSON.stringify(data))
    formData.append('image', imageData)

    const response = await fetch(`/animals/${selectedAnimal.id}`, {
      method: 'PUT',
      body: formData,
    }).then((res) => res.json())

    setAnimals(animals.map((e) => (e.id === selectedAnimal.id ? selectedAnimal : e)))

    _onClose()
  }

  /**
   * Delete animal from animals
   *
   * @param {Animal} animal
   */
  const deleteAnimal = async (animal) => {
    const ans = window.confirm('Are you sure to delete this animal from your profiles?')
    if (ans) {
      try {
        const response = await fetch(`/animals/${animal.id}`, { method: 'DELETE' })

        if (response.status < 200 || response.status >= 300) {
          const { msg } = await response.json()
          console.log(msg)
          return
        }

        setAnimals(animals.filter((e) => e.id !== animal.id))
      } catch (err) {
        console.error(err)
      }
    }
  }

  if (!animals) {
    return (
      <Container centerContent p="5">
        <Spinner size="xl" />
      </Container>
    )
  }

  return (
    <Flex justifyContent="center" mt="5">
      <Stack w="90vw">
        <Heading alignSelf="center" size="lg">
          Animal Profiles
        </Heading>
        <Box height="80px" textAlign="right">
          <Link to="/animals/create">
            <Button colorScheme="blue">Create new profile</Button>
          </Link>
        </Box>

        <Table border="1px">
          <Thead>
            <Tr bgColor="green.100">
              <Th border="1px">Photo</Th>
              <Th border="1px">Name</Th>
              <Th border="1px">Age</Th>
              <Th border="1px">Description</Th>
              <Th border="1px">class</Th>
              <Th border="1px">breed</Th>
              <Th border="1px">Status</Th>
              <Th border="1px">Adopter</Th>
              <Th border="1px">Action</Th>
            </Tr>
          </Thead>
          <Tbody>
            {animals.map((animal) => (
              <Tr key={animal.id}>
                <Td border="1px">
                  <Link to={`animals/${animal.id}`}>
                    <Image src={animal.imageLink} />
                  </Link>
                </Td>
                <Td border="1px"> {animal.name} </Td>
                <Td border="1px"> {animal.age} </Td>
                <Td border="1px"> {animal.description} </Td>
                <Td border="1px"> {animal.animalClass} </Td>
                <Td border="1px"> {animal.animalBreed} </Td>
                <Td border="1px"> {animal.adoptionStatus} </Td>
                <Td border="1px">
                  {animal.available
                    ? null
                    : `${animal.adopter?.firstName} ${animal.adopter?.lastName}`}
                </Td>
                <Td border="1px">
                  <NewsItemModal animal={animal} />
                  <Button mt="1" mr="2" colorScheme="teal" onClick={() => editAnimal(animal)}>
                    Edit
                  </Button>
                  <Button mt="1" colorScheme="red" onClick={() => deleteAnimal(animal)}>
                    Delete
                  </Button>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>

        {/* Edit animal profile */}
        <Drawer isOpen={isOpen} onClose={onClose} onSave={onSave} header="Edit animal profile">
          <FormEditAnimal animal={selectedAnimal} setAnimal={setSelectedAnimal} />
        </Drawer>
      </Stack>
    </Flex>
  )
}
