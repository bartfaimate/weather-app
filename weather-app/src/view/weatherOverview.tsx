import * as React from "react";
import { Button } from "baseui/button";
import axios from "axios";
import { WeatherList } from "../modules/weatherList";
import { useCookies } from 'react-cookie';

import { NewEntryModal } from "../modules/newEntryModal";

export const WeatherOverview = () => {
    const [isOpen, setIsOpen] = React.useState();

    const [entries, setEntries] = React.useState([]);
    const [cookies, setCookie, removeCookie] = useCookies(['cookie-name']);
    const isLoggedIn = cookies.loggedIn?? false

    React.useEffect(() => {
    
        axios.get(`http://localhost:5001/api/weather/`)
          .then(res => {
            console.log(res.data)
            setEntries(res.data)
            //  setEntries({ persons });
          })
      }, [])
    return <>
    <WeatherList entries={entries} onClickCB={undefined} />
   {isLoggedIn && <Button onClick={() => setIsOpen(true)}>Add new</Button>}
   {isLoggedIn && <NewEntryModal isOpen={isOpen} setOpenCb={setIsOpen}></NewEntryModal>}
  </>
}