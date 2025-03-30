import { useState } from 'react';
import React from 'react';
import { useStyletron } from "baseui";
import { Button } from "baseui/button";
import { Layer } from "baseui/layer";
import { ChevronDown, Delete, Overflow, Upload } from "baseui/icon";
import { AppNavBar, setItemActive, NavItem } from "baseui/app-nav-bar";


export const Menu = () => {
    const [css] = useStyletron();
    const [mainItems, setMainItems] = React.useState<NavItem[]>([
        { label: "Home", },
        {  label: "Login" },
        {  label: "Register" },
    ]);



    function handleMainItemSelect(item: NavItem) {
        setMainItems((prev) => setItemActive(prev, item));
    }

    return (
        <AppNavBar 
            title="Weather-App"
            mainItems={mainItems}
            onMainItemSelect={handleMainItemSelect}
        />
    );
}