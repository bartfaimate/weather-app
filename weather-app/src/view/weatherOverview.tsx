import * as React from "react";
import { Button } from "baseui/button";
import axios from "axios";
import { WeatherList } from "../modules/weatherList";
import { useCookies } from 'react-cookie';

import { NewEntryModal } from "../modules/newEntryModal";
import { ModifyEntryModal } from "../modules/modifyEntryModal";

export const WeatherOverview = () => {
    const [isOpen, setOpen] = React.useState(false);
    const [isModifyOpen, setModifyOpen] = React.useState(false)

    const [entries, setEntries] = React.useState([]);
    const [cookies, setCookie, removeCookie] = useCookies();
    const isLoggedIn = cookies.loggedIn ?? false
    const [entryId, setEntryId] = React.useState<string>()

    React.useEffect(() => {
    
        axios.get(`http://localhost:5001/api/weather/`)
          .then(res => {
            console.log(res.data)
            let sorted = res.data.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
            setEntries(sorted)
            //  setEntries({ persons });
          })
      }, [isOpen, isModifyOpen])
    return <>
    <WeatherList entries={entries} onClickCB={[setEntryId, setModifyOpen]} />
   {isLoggedIn && <Button onClick={() => setOpen(true)}>Add new</Button>}
   {isLoggedIn && <NewEntryModal isOpen={isOpen} setOpenCb={setOpen}></NewEntryModal>}
   <ModifyEntryModal isOpen={isModifyOpen} setOpenCb={setModifyOpen} entryId={entryId}></ModifyEntryModal>
  </>
}