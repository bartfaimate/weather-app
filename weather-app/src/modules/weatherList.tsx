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
                                artwork={props => <Check {...props} />}
                                shape={SHAPE.ROUND}
                                endEnhancer={() => (
                                    <ListItemLabel>{`${entry.temperature}°C ${entry.sky_overcast}`}</ListItemLabel>
                                )}
                            >
                                <ListItemLabel description={`${entry.temperature}°C ${entry.sky_overcast}`}> {entry.timestamp}</ListItemLabel>
                            </ListItem>
                        )
                    })
                }
            </ul>


        </>
    );
}