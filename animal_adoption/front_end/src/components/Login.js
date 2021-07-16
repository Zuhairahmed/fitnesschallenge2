import React, { useState } from 'react'
import {
  Input,
  FormControl,
  FormLabel,
  Button,
  Heading,
  Container,
  Box,
  Text,
} from '@chakra-ui/react'

export default function Login() {
  const [formState, setFormState] = useState({
    username: '',
    password: '',
  })

  const [error, setError] = useState('')

  const redirectToHome = () => {
    window.location.href = '/'
  }

  const submitForm = async (event) => {
    event.preventDefault()

    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...formState }),
      })

      if (response.status < 200 || response.status >= 300) {
        const { msg } = await response.json()
        setError(msg)
        return
      }

      redirectToHome()
    } catch (e) {
      setError('Login Failed.')
    }
  }

  const handleChange = (event) => {
    setFormState({
      ...formState,
      [event.target.name]: event.target.value,
    })
  }

  return (
    <Container>
      <Heading size="md" mt="5">
        Login
      </Heading>
      {error && (
        <Box>
          <Text color="red">{error}</Text>
        </Box>
      )}
      <FormControl as="form" onSubmit={submitForm}>
        <Input mt="2" type="text" name="username" placeholder="Username" onChange={handleChange} />
        <Input
          mt="2"
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
        />
        <Button type="submit" mt="2" colorScheme="teal">
          Login
        </Button>
      </FormControl>
    </Container>
  )
}
