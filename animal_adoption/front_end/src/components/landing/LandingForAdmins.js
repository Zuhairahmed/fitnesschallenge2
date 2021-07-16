import {
  Button,
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
} from '@chakra-ui/react'
import { useEffect, useState } from 'react'
import User from '../../models/User'

export default function LandingForAdmins() {
  const [users, setUsers] = useState(null)

  const fetchUsers = async () => {
    try {
      const { message } = await fetch('/users').then((res) => res.json())
      if (message) {
        setUsers(JSON.parse(message).map((e) => new User(e)))
      }
    } catch (e) {
      setUsers([])
      console.error(e)
    }
  }

  /**
   * Delete user
   *
   * @param {number} userId
   */
  const deleteUser = async (userId) => {
    const ans = window.confirm('Are you sure to delete this user?')
    if (ans) {
      try {
        const response = await fetch(`/users/${userId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        })

        if (response.status < 200 || response.status >= 300) {
          const { msg } = await response.json()
          console.log(msg)
          return
        }

        setUsers(users.filter((e) => e.id !== userId))
      } catch (err) {
        console.error(err)
      }
    }
  }

  useEffect(async () => {
    await fetchUsers()
  }, [])

  if (users === null) {
    return (
      <Container centerContent p="5">
        <Spinner size="xl" />
      </Container>
    )
  }

  return (
    <Flex justifyContent="center" mt="5">
      <Stack w="60vw">
        <Heading alignSelf="center" size="lg" mb="2">
          User lists
        </Heading>
        {(users?.length ?? 0) !== 0 ? (
          <Table border="1px">
            <Thead>
              <Tr bgColor="green.100">
                <Th border="1px">Username</Th>
                <Th border="1px">First Name</Th>
                <Th border="1px">Last Name</Th>
                <Th border="1px">Email</Th>
                <Th border="1px">User Type</Th>
                <Th border="1px">Action</Th>
              </Tr>
            </Thead>
            <Tbody>
              {users.map((user) => (
                <Tr key={user.username}>
                  <Td border="1px"> {user.username} </Td>
                  <Td border="1px"> {user.firstName} </Td>
                  <Td border="1px"> {user.lastName} </Td>
                  <Td border="1px"> {user.emailAddress} </Td>
                  <Td border="1px"> {user.userType} </Td>
                  <Td border="1px">
                    <Button colorScheme="red" onClick={() => deleteUser(user.id)}>
                      Delete
                    </Button>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        ) : (
          <Box bg="orange.100" p="5">
            No profiles found
          </Box>
        )}
      </Stack>
    </Flex>
  )
}
