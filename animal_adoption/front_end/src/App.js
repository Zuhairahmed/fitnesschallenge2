import { Switch, Route } from 'react-router-dom'
import { Flex, Box } from '@chakra-ui/react'
import { useState } from 'react'
import Landing from './pages/Landing'
import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'
import AdopterSettingsPage from './pages/AdopterSettingsPage'
import Header from './components/Header'
import Footer from './components/Footer'
import UserContext from './components/users/UserContext'
import Animals from './pages/Animals'
import User from './models/User'

function App() {
  /** @type {[User, Function]} */
  const [user, setUser] = useState()

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Flex direction="column" flexFlow="column" minH="100vh">
        <Header />

        <Box as="main" flex="1" bg="gray.50">
          <Switch>
            <Route path="/account">
              <div>Account page</div>
            </Route>

            <Route path="/signup">
              <SignupPage />
            </Route>

            <Route path="/login">
              <LoginPage />
            </Route>

            <Route path="/about">
              <Box as="p" p="5">
                This is a capstone project for OSU CS467.
                <br />
                This is a dating app project that matches shelter animals up with prospective
                owners.
              </Box>
            </Route>

            <Route path="/animals">
              <Animals />
            </Route>

            <Route path="/AdopterSettings">
              <AdopterSettingsPage />
            </Route>

            <Route path="/">
              <Landing />
            </Route>
          </Switch>
        </Box>

        <Footer />
      </Flex>
    </UserContext.Provider>
  )
}

export default App
