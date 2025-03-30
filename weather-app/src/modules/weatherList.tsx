import * as React from "react";

import {
  ListItem,
  ListItemLabel,
  SHAPE
} from "baseui/list";

import { Check } from "baseui/icon";

export const WeatherList = ({
  entries, onClickCB
}) => {
  return (
    <>
      <ul>
        {
          entries.map((entry) => {
            return (
              <ListItem
              onClick={ () => {onClickCB[0](entry.id) , onClickCB[1](true)}}
                artwork={props => <Check {...props} />}
                shape={SHAPE.ROUND}
                endEnhancer={() => (
                  <ListItemLabel>{`${entry.temperature}°C, ${entry.humidity}%`}</ListItemLabel>
                )}
              >
                <ListItemLabel description={`${entry.location}`}> {entry.timestamp}</ListItemLabel>
              </ListItem>
            )
          })
        }
      </ul>


    </>
  );
}