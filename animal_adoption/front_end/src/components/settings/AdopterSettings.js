import {
  Center,
  Divider,
  Checkbox,
  Button,
  Input,
  FormControl,
  FormLabel,
  Stack,
  Flex,
  Select,
} from '@chakra-ui/react'
import React, { Component } from 'react'

export default class AdopterSettings extends Component {
  constructor(props) {
    super(props)
    this.state = {
      firstName: '',
      lastName: '',
      username: '',
      userRole: 'adopter',
      animalPreference: '',
      goodWithAnimals: false,
      goodWithChildren: false,
      animalLeashed: false,
    }

    this.submitForm = this.submitForm.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleCheckbox = this.handleCheckbox.bind(this)
    this.handleDropDown = this.handleDropDown.bind(this)
  }

  componentDidMount() {
    // API GET Method
    // Make API call to get the user's information
    // setState the user's information
    fetch('/get-user-details', {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-type': 'application/json',
      },
    })
      .then((results) => results.json())
      .then((data) => {
        let parsedData = JSON.stringify(data)
        parsedData = JSON.parse(parsedData)
        console.log(parsedData)

        this.setState({
          firstName: parsedData.message.firstName,
          lastName: parsedData.message.lastName,
          username: parsedData.message.username,
          animalPreference: parsedData.message.animalPreference,
        })
      })
  }

  handleDropDown(event) {
    this.setState({
      [event.target.name]: event.target.value,
    })
  }

  handleCheckbox(event) {
    this.setState({
      [event.target.name]: event.target.checked,
    })
  }

  checkClick(event) {
    const { name, checked } = event.target

    this.setState(() => {
      const animalDisposition = event.disposition_types
      animalDisposition[name] = checked
      return animalDisposition[name]
    })
  }

  handleChange(event) {
    console.log('Handle Change')
    this.setState({
      [event.target.name]: event.target.value,
    })
  }

  submitForm(event) {
    // Console.log messages are for developers to see what will be passed
    // To view any field we enter "event.target.{field_name}.value"
    console.log('Adopter Update Form submitted')
    console.log(event.target.firstName.value)
    console.log(event.target.lastName.value)
    console.log(event.target.username.value)
    console.log(event.target.animalPreference.value)
    console.log(event.target.goodWithAnimals.checked)
    console.log(event.target.goodWithChildren.checked)
    console.log(event.target.animalLeashed.checked)
    // Add code to connect to Flask API
    // event.preventDefault()
    fetch('/update-user-details', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(this.state),
    })

    console.log(this.state)
  }

  render() {
    return (
      <Flex justifyContent="center" mt="5">
        <div>
          <Center>
            <b>User Settings Update</b>
          </Center>
          <FormControl>
            <form onSubmit={this.submitForm}>
              <FormLabel>First Name</FormLabel>
              <Input
                type="text"
                name="firstName"
                placeholder={this.state.firstName}
                defaultValue={this.state.firstName}
                onChange={this.handleChange}
              />
              <br />
              <FormLabel>Last Name</FormLabel>
              <Input
                type="text"
                name="lastName"
                placeholder={this.state.lastName}
                defaultValue={this.state.lastName}
                onChange={this.handleChange}
              />
              <br />
              <FormLabel>Username</FormLabel>
              <Input
                type="email"
                name="username"
                placeholder={this.state.username}
                defaultValue={this.state.username}
                onChange={this.handleChange}
              />
              <br />
              <FormLabel>Desired Animal Type</FormLabel>
              <Select
                name="animalPreference"
                value={this.state.animalPreference}
                onChange={this.handleDropDown}
              >
                <option value=""> Select Animal </option>
                <option value="dog">Dog</option>
                <option value="cat">Cat</option>
                <option value="other">Other</option>
              </Select>
              <br />
              <Divider />
              <Stack spacing={0} direction="column">
                <FormLabel>Animal Disposition</FormLabel>
                <Checkbox type="checkbox" name="goodWithAnimals" onChange={this.handleCheckbox}>
                  Good with other animals
                </Checkbox>
                <Checkbox type="checkbox" name="goodWithChildren" onChange={this.handleCheckbox}>
                  Good with other children
                </Checkbox>
                <Checkbox type="checkbox" name="animalLeashed" onChange={this.handleCheckbox}>
                  Animal must be leashed at all times
                </Checkbox>
              </Stack>
              <br />
              <Center>
                <Button type="submit" colorScheme="green">
                  Update
                </Button>
              </Center>
            </form>
          </FormControl>
        </div>
      </Flex>
    )
  }
}
