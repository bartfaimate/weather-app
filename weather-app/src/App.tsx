import { useState, useEffect } from 'react'

import './App.css'

import { Login } from './view/Login'
import { Menu, HeaderMenu } from './modules/menu'
import { Register } from './view/register'
import { Block } from "baseui/block";
import { Button } from "baseui/button";
import { Grid, Cell } from 'baseui/layout-grid'

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { WeatherOverview } from './view/weatherOverview'

import { CookiesProvider } from 'react-cookie';

import axios from 'axios'

function App() {

  const [isLoggedIn, setLoggedIn] = useState(false);


  return (
    <>
      <CookiesProvider defaultSetOptions={{ path: '/' }}>

        <Router>

          <Grid>
            <Cell span={12}>
              <HeaderMenu></HeaderMenu>
            </Cell>

            <Cell span={12}>
              <Routes>
                <Route path="/" element={<WeatherOverview  />} />

                <Route path="/login" element={<Login setLoginCb={setLoggedIn} />} />
                <Route path="/register" element={<Register />} />

              </Routes>


            </Cell>

          </Grid>
        </Router>
      </CookiesProvider>

    </>
  );

}

export default App
