import {
  Input,
  Textarea,
  FormControl,
  FormLabel,
  Image,
  Select,
  Checkbox,
  Stack,
} from '@chakra-ui/react'

import { animalClasses, animalBreeds, adoptionStatuses } from '../../models/Animal'

function PreviewImage({ animal }) {
  if (animal?.imageLink) {
    return <Image src={animal.imageLink} />
  }
  return <div>Preview: No data</div>
}

export default function FormEditAnimal({ animal, setAnimal }) {
  const handleImageFile = (event) => {
    const file = event.target.files[0]
    setAnimal({
      ...animal,
      imageData: file,
      imageLink: URL.createObjectURL(file),
    })
  }

  const handleChange = (event) => {
    setAnimal({
      ...animal,
      [event.target.name]: event.target.value,
    })
  }

  const handleCheckbox = (event) => {
    let { dispositions } = animal
    if (event.target.checked) {
      dispositions = dispositions.concat([event.target.name])
    } else {
      dispositions = dispositions.filter((e) => e !== event.target.name)
    }
    setAnimal({
      ...animal,
      dispositions: [...new Set(dispositions)],
    })
  }

  const isDispositionChecked = (disposition) => !!animal.dispositions.find((e) => e === disposition)

  return (
    <FormControl>
      <FormLabel>Name</FormLabel>
      <Input type="text" name="name" defaultValue={animal?.name} onChange={handleChange} />

      <FormLabel>Age</FormLabel>
      <Input type="number" name="age" defaultValue={animal?.age} onChange={handleChange} />

      <FormLabel>Description</FormLabel>
      <Textarea
        type="text"
        name="description"
        defaultValue={animal?.description}
        onChange={handleChange}
      />

      <FormLabel>Animal Class</FormLabel>
      <Select name="animalClass" onChange={handleChange} defaultValue={animal.animalClass}>
        {animalClasses.map((e) => (
          <option key={`class-${e}`} value={e}>
            {e}
          </option>
        ))}
      </Select>

      <FormLabel>Animal Breed</FormLabel>
      <Select name="animalBreed" onChange={handleChange} defaultValue={animal.animalBreed}>
        {animalBreeds.map((e) => (
          <option key={`breed-${e}`} value={e}>
            {e}
          </option>
        ))}
      </Select>

      <FormLabel>Animal Disposition</FormLabel>
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

      <FormLabel>Image</FormLabel>
      <Input type="file" name="image" mb="1" onChange={handleImageFile} />
      <PreviewImage animal={animal} />

      <FormLabel mt="5">Adoption Status</FormLabel>
      <Select name="adoptionStatus" onChange={handleChange} defaultValue={animal.adoptionStatus}>
        {adoptionStatuses.map((e) => (
          <option key={`adoption-${e}`} value={e}>
            {e}
          </option>
        ))}
      </Select>
    </FormControl>
  )
}
