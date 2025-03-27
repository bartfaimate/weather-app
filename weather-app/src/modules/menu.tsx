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
        { icon: Upload, label: "Home" },
        { icon: Upload, label: "Primary B" },


    ]);
    const userItems = [
        { icon: Overflow, label: "Account item1" },
        { icon: Overflow, label: "Account item2" },
        { icon: Overflow, label: "Account item3" },
        { icon: Overflow, label: "Account item4" },
    ];


    function handleMainItemSelect(item: NavItem) {
        setMainItems((prev) => setItemActive(prev, item));
    }

    return (
        <AppNavBar 
            title="Weather-App"
            mainItems={mainItems}
            onMainItemSelect={handleMainItemSelect}
            onUserItemSelect={(item) => console.log("user", item)}
        />
    );
}