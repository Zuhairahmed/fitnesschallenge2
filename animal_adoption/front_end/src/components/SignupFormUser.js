import {
  Input,
  Center,
  Button,
  Checkbox,
  FormControl,
  FormLabel,
  Select,
  Divider,
  Stack,
} from '@chakra-ui/react'
import React, { Component } from 'react'

export default class SignupFormUser extends Component {
  constructor(props) {
    super(props)
    this.state = {
      firstName: '',
      lastName: '',
      username: '',
      password: '',
      userType: 'adopter',
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

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value,
    })
  }

  submitForm(event) {
    // Console.log messages are for developers to see what will be passed
    // To view any field we enter "event.target.{field_name}.value"
    console.log('Adopter Form submitted')
    console.log(event.target.firstName.value)
    console.log(event.target.lastName.value)
    console.log(event.target.username.value)
    console.log(event.target.password.value)
    console.log(event.target.animalPreference.value)
    console.log(event.target.goodWithAnimals.checked)
    console.log(event.target.goodWithChildren.checked)
    console.log(event.target.animalLeashed.checked)
    event.preventDefault()
    fetch('/create-user-with-all-details', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(
        this.state
        // this.state.firstName.value,
        // this.state.lastName.value,
        // this.state.username.value,
        // this.state.password.value,
        // this.state.animalType.value,
        // this.state.goodWithAnimals.value,
        // this.state.goodWithChildren.value,
        // this.state.animalLeashed.value
      ),
    }).then(() => {
      window.location.href = '/#/login'
    })
    console.log(this.state)
    // console.log('STATE STRINGIFIED')
    // console.log(JSON.stringify(this.state))
    // Add code to connect to Flask API
  }

  // Add required later
  render() {
    return (
      <div>
        <FormLabel> Adopter Registration Form</FormLabel>
        <FormControl>
          <form onSubmit={this.submitForm}>
            <FormLabel>First Name</FormLabel>
            <Input
              type="text"
              name="firstName"
              placeholder="First Name"
              value={this.state.firstName}
              onChange={this.handleChange}
              required
            />
            <br />
            <FormLabel>Last Name</FormLabel>
            <Input
              type="text"
              name="lastName"
              placeholder="Last Name"
              value={this.state.lastName}
              onChange={this.handleChange}
              required
            />
            <br />
            <FormLabel>E-Mail Address</FormLabel>
            <Input
              type="email"
              name="username"
              placeholder="Email Address"
              value={this.state.username}
              onChange={this.handleChange}
              required
            />
            <br />
            <FormLabel>Password</FormLabel>
            <Input
              type="password"
              name="password"
              placeholder="Password"
              value={this.state.password}
              onChange={this.handleChange}
              required
            />
            <br />
            <FormLabel>Select Desired Animal Type:</FormLabel>
            <Select
              name="animalPreference"
              value={this.state.animalPreference}
              onChange={this.handleDropDown}
              required
            >
              <option value="">Select Animal</option>
              <option value="dog">Dog</option>
              <option value="cat">Cat</option>
              <option value="other">Other</option>
            </Select>
            <br />
            <Divider />
            <Stack spacing={0} direction="column">
              <FormLabel>Animal Disposition</FormLabel>
              <Checkbox
                input
                type="checkbox"
                name="goodWithAnimals"
                value={this.state.goodWithAnimals}
                onChange={this.handleCheckbox}
              >
                Good with other animals
              </Checkbox>
              <Checkbox
                input
                type="checkbox"
                name="goodWithChildren"
                value={this.state.goodWithChildren}
                onChange={this.handleCheckbox}
              >
                Good with other children
              </Checkbox>
              <Checkbox
                input
                type="checkbox"
                name="animalLeashed"
                value={this.state.animalLeashed}
                onChange={this.handleCheckbox}
              >
                Animal must be leashed at all times
              </Checkbox>
            </Stack>
            <br />
            <Center>
              <Button type="submit" colorScheme="green">
                Register
              </Button>
            </Center>
          </form>
        </FormControl>
      </div>
    )
  }
}
