import {
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Input,
  Textarea,
  FormControl,
  FormLabel,
  Image,
  Select,
  Checkbox,
  Stack,
} from '@chakra-ui/react'
import { useState } from 'react'

import { animalClasses, animalBreeds } from '../../models/Animal'
import SearchConditions from '../../models/SearchConditions'

export default function SearchModal({ searchConditions: state, setSearchConditions: setState }) {
  const { isOpen, onOpen, onClose } = useDisclosure()

  const handleChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.value,
    })
  }

  const handleCheckbox = (event) => {
    let { dispositions } = state
    if (event.target.checked) {
      dispositions = dispositions.concat([event.target.name])
    } else {
      dispositions = dispositions.filter((e) => e !== event.target.name)
    }
    setState({
      ...state,
      dispositions: [...new Set(dispositions)],
    })
  }

  const isDispositionChecked = (disposition) =>
    !!state?.dispositions?.find((e) => e === disposition)

  const resetState = () => {
    const { keyword } = state
    setState({
      ...new SearchConditions(),
      keyword,
    })
  }

  return (
    <>
      <Button ml="2" colorScheme="teal" onClick={onOpen}>
        Advanced
      </Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Advanced Search</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <FormControl>
              <FormLabel>Animal Class</FormLabel>
              <Select name="animalClass" onChange={handleChange} defaultValue={state.animalClass}>
                <option value="all">all</option>
                {animalClasses.map((e) => (
                  <option key={`class-${e}`} value={e}>
                    {e}
                  </option>
                ))}
              </Select>

              <FormLabel>Animal Breed</FormLabel>
              <Select name="animalBreed" onChange={handleChange} defaultValue={state.animalBreed}>
                <option value="all">all</option>
                {animalBreeds.map((e) => (
                  <option key={`breed-${e}`} value={e}>
                    {e}
                  </option>
                ))}
              </Select>

              <FormLabel mt="2">Animal Disposition</FormLabel>
              <Stack spacing={2} direction="column">
                <Checkbox
                  type="checkbox"
                  name="Good with other animals"
                  isChecked={isDispositionChecked('Good with other animals')}
                  onChange={handleCheckbox}
                >
                  Good with other animals
                </Checkbox>
                <Checkbox
                  type="checkbox"
                  name="Good with children"
                  isChecked={isDispositionChecked('Good with children')}
                  onChange={handleCheckbox}
                >
                  Good with other children
                </Checkbox>
                <Checkbox
                  type="checkbox"
                  name="Animal must be leashed at all times"
                  isChecked={isDispositionChecked('Animal must be leashed at all times')}
                  onChange={handleCheckbox}
                >
                  Animal must be leashed at all times
                </Checkbox>
              </Stack>

              <FormLabel mt="2">Creation Date</FormLabel>
              <Select name="creationDate" onChange={handleChange}>
                <option>All</option>
                <option value="today">Today</option>
                <option value="week">Last 7 days</option>
                <option value="month">Last 30 days</option>
              </Select>
            </FormControl>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={onClose}>
              OK
            </Button>
            <Button color="gray.800" onClick={resetState}>
              Reset
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}
