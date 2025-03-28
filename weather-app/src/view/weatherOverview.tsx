import * as React from "react";
import { Button } from "baseui/button";
import axios from "axios";
import { WeatherList } from "../modules/weatherList";


export const WeatherOverview = ({isLoggedIn}) => {

    const [entries, setEntries] = React.useState([]);

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
   {isLoggedIn && <Button onClick={() => console.log("Button clicked!")}>Logged-in Action</Button>}
  </>
}