import {
  InputGroup,
  Input,
  Button,
  Image,
  Box,
  Stack,
  Heading,
  Badge,
  Spinner,
  Container,
  Grid,
  Switch,
  FormControl,
  FormLabel,
  Spacer,
} from '@chakra-ui/react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Animal from '../../models/Animal'
import SearchConditions from '../../models/SearchConditions'
import useAnimalNews from '../animals/useAnimalNews'
import SearchModal from './SearchModal'

const AnimalCard = ({ animal }) => (
  <Box borderWidth="1px" borderRadius="lg" overflow="hidden" m="2" cursor="pointer">
    <Image w="100%" src={animal.imageLink} />

    <Box p="6">
      <Box d="flex" alignItems="baseline">
        <Badge borderRadius="full" px="2" colorScheme="teal">
          {animal.animalClass} - {animal.animalBreed}
        </Badge>
      </Box>

      <Box mt="1" fontWeight="semibold" as="h4" lineHeight="tight" isTruncated>
        {animal.name} (Age: {animal.age})
      </Box>

      <Box>
        <Box as="span" color="gray.600" fontSize="sm" />
      </Box>

      <Box d="flex" mt="2" alignItems="center">
        <Box as="span" ml="2" color="gray.600" fontSize="sm">
          <ul>
            {animal.dispositions.map((e) => (
              <li key={e}>{e}</li>
            ))}
          </ul>
        </Box>
      </Box>
      <Box textAlign="right" color="gray.500" fontSize="sm">
        date: {animal.creationDate}
      </Box>
    </Box>
  </Box>
)

const AnimalGrid = ({ animals }) => {
  if (animals.length === 0) {
    return (
      <Box textAlign="center" mt="4" color="red">
        <Heading size="md">Animals not found</Heading>
      </Box>
    )
  }
  return (
    <Grid templateColumns="repeat(auto-fit, minmax(160px, 270px))" justifyContent="center">
      {animals.map((animal) => (
        <Link to={`/animals/${animal.id}`} key={animal.id}>
          <AnimalCard animal={animal} />
        </Link>
      ))}
    </Grid>
  )
}

const NewsItems = () => {
  const { news, fetchAnimalNews } = useAnimalNews()

  useEffect(async () => {
    await fetchAnimalNews()
  }, [])

  return (
    <Stack w="70vw">
      <Box>
        <Heading size="lg" textAlign={{ base: 'center', sm: 'center' }}>
          News
        </Heading>
      </Box>

      {news ? (
        <Grid templateColumns="repeat(auto-fit, minmax(120px, 240px))" justifyContent="center">
          {news.map((e) => (
            <Box
              key={e.id}
              borderWidth="1px"
              borderRadius="lg"
              overflow="hidden"
              m="2"
              p="3"
              cursor="pointer"
              onClick={() => {
                window.location.href = `/#/animals/${e.animal_id}`
              }}
            >
              <Box>
                <Badge borderRadius="full" px="2" colorScheme="orange">
                  {e.date}
                </Badge>
              </Box>
              <Box>{e.text}</Box>
            </Box>
          ))}
        </Grid>
      ) : (
        <div>No news items</div>
      )}
    </Stack>
  )
}

export default function LandingForAdopters() {
  const [animals, setAnimals] = useState(null)

  const fetchAllAnimals = async () => {
    try {
      const { message } = await fetch('/get-animals').then((res) => res.json())
      if (message) {
        setAnimals(JSON.parse(message).map((e) => new Animal(e)))
      }
    } catch (e) {
      setAnimals([])
      console.error(e)
    }
  }

  const fetchMatchingAnimals = async () => {
    try {
      const { message } = await fetch('/get-matching-animals').then((res) => res.json())
      if (message) {
        setAnimals(JSON.parse(message).map((e) => new Animal(e)))
      }
    } catch (e) {
      setAnimals([])
      console.error(e)
    }
  }

  useEffect(async () => {
    fetchAllAnimals()
  }, [])

  const handleSwitch = (event) => {
    if (event.target.checked) {
      fetchMatchingAnimals()
    } else {
      fetchAllAnimals()
    }
  }

  const [searchConditions, setSearchConditions] = useState(new SearchConditions())
  const handleSearchWordChange = (event) => {
    setSearchConditions({
      ...searchConditions,
      keyword: event.target.value.toLowerCase(),
    })
  }

  const applySearchConditions = (animal) => {
    const keywordMatched =
      searchConditions.keyword === '' ||
      animal.name.toLowerCase().includes(searchConditions.keyword)
    const classMatched =
      searchConditions.animalClass === 'all' || animal.animalClass === searchConditions.animalClass
    const breedMatched =
      searchConditions.animalBreed === 'all' || animal.animalBreed === searchConditions.animalBreed

    let hasDispositions = true
    searchConditions.dispositions.forEach((disposition) => {
      hasDispositions = hasDispositions && !!animal.dispositions.find((e) => e === disposition)
    })

    let creationDateMatched = true
    const creationDate = new Date(animal.creationDate)
    creationDate.setHours(0)
    const baseDate = new Date()
    baseDate.setHours(0)
    switch (searchConditions.creationDate) {
      case 'today':
        creationDateMatched = baseDate === creationDate
        break
      case 'week':
        baseDate.setDate(baseDate.getDate() - 7)
        creationDateMatched = baseDate <= creationDate
        break
      case 'month':
        baseDate.setDate(baseDate.getDate() - 30)
        creationDateMatched = baseDate <= creationDate
        break
      default:
        creationDateMatched = true
    }

    return keywordMatched && classMatched && breedMatched && hasDispositions && creationDateMatched
  }

  const checkCreationDate = () => {}

  const filteredAnimals = () => {
    if (!animals) {
      return []
    }
    return animals.filter((e) => applySearchConditions(e))
  }

  if (animals === null) {
    return (
      <Container centerContent p="5">
        <Spinner size="xl" />
      </Container>
    )
  }

  return (
    <Container centerContent>
      <NewsItems />

      <Box mt="5">
        <Heading size="lg" textAlign={{ base: 'center', sm: 'center' }}>
          Animal Profiles
        </Heading>
      </Box>

      <InputGroup m="5" size="md">
        <Input placeholder="Find a pet" rounded="xl" onChange={handleSearchWordChange} />
        <SearchModal
          searchConditions={searchConditions}
          setSearchConditions={setSearchConditions}
        />
      </InputGroup>

      <Stack w="70vw">
        <Box justifyContent="right">
          <FormControl display="flex" alignItems="center">
            <Spacer />
            <FormLabel htmlFor="show-matching-animals" mb="0">
              Show matching animals
            </FormLabel>
            <Switch id="show-matching-animals" onChange={handleSwitch} />
          </FormControl>
        </Box>

        <AnimalGrid animals={filteredAnimals()} />
      </Stack>
    </Container>
  )
}
