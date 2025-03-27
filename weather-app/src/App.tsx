import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

import './App.css'

import { Login } from './view/Login'
import { Menu } from './modules/menu'
import { Block } from "baseui/block";
import { Button } from "baseui/button";
import { Grid, Cell } from 'baseui/layout-grid'



function App() {

  return (
    <>
      
    <Grid>
      <Cell span={12}>
        <Menu></Menu>
      </Cell>

      <Cell span={12}>
        <Grid>
          <Cell>Mon</Cell>
          <Cell>Tue</Cell>
          <Cell>Wed</Cell>
          <Cell>Thu</Cell>


        </Grid>
      </Cell>

    </Grid>
      
    </>
  );

}

export default App
