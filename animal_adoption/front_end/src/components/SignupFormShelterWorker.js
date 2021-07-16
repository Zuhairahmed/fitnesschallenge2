import { Center, Button, Input, FormControl, FormLabel, Select } from '@chakra-ui/react'
import React, { Component } from 'react'

let shelter_names = []

export default class SignupFormShelterWorker extends Component {
  constructor(props) {
    super(props)
    this.state = {
      firstName: '',
      lastName: '',
      username: '',
      password: '',
      userType: 'shelter worker',
      shelterNames: [],
      shelterName: '',
    }

    this.submitForm = this.submitForm.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleDropDown = this.handleDropDown.bind(this)
  }

  componentDidMount() {
    fetch('/get-shelters', {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-type': 'application/json',
      },
    })
      .then((results) => results.json())
      .then((data) => {
        let parsed_data = JSON.stringify(data)
        parsed_data = JSON.parse(parsed_data)
        const data_length = parsed_data.message.length
        shelter_names = []
        for (let i = 0; i < data_length; i += 1) {
          shelter_names.push(parsed_data.message[i].name)
        }

        this.setState({ shelterNames: shelter_names })
      })
  }

  handleDropDown(event) {
    this.setState({
      [event.target.name]: event.target.value,
    })
  }

  handleChange(event) {
    console.log('Handle Change')
    console.log('Event Target Name')
    console.log(event.target.name)
    this.setState({
      [event.target.name]: event.target.value,
    })
    console.log(event.target.name)
  }

  submitForm(event) {
    console.log('Shelter Worker Form submitted')
    console.log(event.target.firstName.value)
    console.log(event.target.lastName.value)
    console.log(event.target.username.value)
    console.log(event.target.shelterName.value)
    // To view any field we enter "event.target.{field_name}.value"
    // Add code to connect to Flask API
    event.preventDefault()
    fetch('/create-user-with-all-details', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(this.state),
    }).then(() => {
      window.location.href = '/#/login'
    })

    console.log('STATE STRINGIFIED')
    console.log(JSON.stringify(this.state))
  }

  render() {
    return (
      <div>
        <FormLabel>Shelter Worker Signup Form</FormLabel>
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
              placeholder="E-Mail Address"
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
            <FormLabel>Select Shelter:</FormLabel>
            <Select
              name="shelterName"
              value={this.state.shelterName}
              onChange={this.handleDropDown}
              required
            >
              <option value="">Select Shelter</option>
              {this.state.shelterNames.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </Select>
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
