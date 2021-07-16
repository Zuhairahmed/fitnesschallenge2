import { Box, Flex, Heading } from '@chakra-ui/react'

export default function Footer() {
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="1.5rem"
      bg="gray.500"
      color="white"
    >
      <Box>
        <Heading as="h3" size="sm">
          ©2021 OSU CS467 Team Chinchillas
        </Heading>
      </Box>
    </Flex>
  )
}
