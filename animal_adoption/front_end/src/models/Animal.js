export const animalBreeds = ['golden retriever', 'border collie', 'tabby', 'bengal', 'other']
export const animalClasses = ['dog', 'cat', 'other']
export const adoptionStatuses = ['Not Available', 'Available', 'Pending', 'Adopted']

/**
 * @param {string|null} imagePath
 * @returns {string}
 */
function getImageLink(imagePath) {
  if (!imagePath) {
    return ''
  }

  if (imagePath.startsWith('animal_adoption/front_end/public')) {
    return imagePath.replace('animal_adoption/front_end/public', '')
  }

  if (imagePath.startsWith('animal_adoption/front_end/build')) {
    return imagePath.replace('animal_adoption/front_end/build', '')
  }

  return ''
}

function setAnimalClass(id) {
  if (!id || id >= animalClasses.length) {
    return animalClasses[0]
  }
  return animalClasses[id - 1]
}

function setAnimalBreed(id) {
  if (!id || id >= animalBreeds.length) {
    return animalBreeds[0]
  }
  return animalBreeds[id - 1]
}

function setAdoptionStatus(id) {
  if (!id || id >= adoptionStatuses.length) {
    return 'Available'
  }
  return adoptionStatuses[id - 1]
}

export default class Animal {
  constructor(data) {
    this.id = data?.id_animal ?? ''
    this.name = data?.name ?? ''
    this.age = data?.age
    this.description = data?.description ?? ''
    this.animalClass = setAnimalClass(data?.animal_class_id)
    this.animalBreed = setAnimalBreed(data?.animal_breed_id)
    this.dispositions = data?.dispositions ?? []
    this.adoptionStatus = setAdoptionStatus(data?.adoption_status_id)
    this.creationDate = data?.creation_date
    this.adopter = data?.adopter

    this.shelter = data?.shelter

    this.imageData = null // for submit an image file
    this.imageLink = getImageLink(data?.image_path)
  }

  get available() {
    return this.adoptionStatus === adoptionStatuses[1]
  }

  afterAdoptionRequestSucceeded() {
    this.adoptionStatus = 'Pending'
  }
}
