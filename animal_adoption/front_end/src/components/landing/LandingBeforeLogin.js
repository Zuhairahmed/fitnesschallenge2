import { Button, Image, Box, Stack, Heading, Text, Flex } from '@chakra-ui/react'
import { Link } from 'react-router-dom'

export default function LandingBeforeLogin() {
  return (
    <Flex
      align="center"
      justify={{ base: 'center', md: 'space-around', xl: 'space-between' }}
      direction={{ base: 'column-reverse', md: 'row' }}
      wrap="no-wrap"
      minH="80vh"
      px={8}
      py={8}
    >
      <Stack
        spacing={4}
        w={{ base: '80%', md: '50%' }}
        align={['center', 'center', 'flex-start', 'flex-start', 'center']}
      >
        <Heading
          as="h1"
          size="xl"
          fontWeight="bold"
          color="primary.800"
          textAlign={['center', 'center', 'left', 'left']}
        >
          <Text as="span" position="relative" color="gray.800">
            Dating App for
            <Text color="green.500">Animal Adoption</Text>
          </Text>
        </Heading>
        <Heading
          as="h2"
          size="md"
          color="primary.800"
          opacity="0.8"
          fontWeight="normal"
          lineHeight={1.5}
          textAlign={['center', 'center', 'left', 'left']}
        >
          Capstone project OSU CS467
          <Text as="p" size="sm">
            some description here
          </Text>
        </Heading>
        <Link to="/signup">
          <Button colorScheme="green">Get started</Button>
        </Link>
      </Stack>

      <Box w={{ base: '80%', sm: '70%', md: '50%' }} mb={{ base: 12, md: 0 }}>
        <Image src="/img/lp.jpeg" size="100%" rounded="1rem" shadow="dark-lg" />
      </Box>
    </Flex>
  )
}
