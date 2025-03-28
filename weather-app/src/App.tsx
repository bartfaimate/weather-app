import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

import './App.css'

import { Login } from './view/Login'
import { Menu } from './modules/menu'
import { Register } from './view/register'
import { Block } from "baseui/block";
import { Button } from "baseui/button";
import { Grid, Cell } from 'baseui/layout-grid'

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { WeatherOverview } from './view/weatherOverview'

import { WeatherList } from './modules/weatherList'

import axios from 'axios'

function App() {

  const [isLoggedIn, setLoggedIn] = useState(false);


  return (
    <>
    <Router>

      <Grid>
        <Cell span={12}>
          <Menu></Menu>
        </Cell>

        <Cell span={12}>
          <Routes>
            <Route path="/" element={<WeatherOverview isLoggedIn={isLoggedIn} />} />

            <Route path="/login" element={<Login setLoginCb={setLoggedIn}/>}/>
            <Route path="/register" element={<Register/>}/>
            
          </Routes>


        </Cell>

      </Grid>
    </Router>

    </>
  );

}

export default App
