import { useState } from "react";
import React from "react";

import {
  HeaderNavigation,
  ALIGN,
  StyledNavigationItem as NavigationItem,
  StyledNavigationList as NavigationList,
} from "baseui/header-navigation";
import { StyledLink as Link } from "baseui/link";

interface NavLink {
    label: string
    route: string
}

export const HeaderMenu = () => {
  const [mainItems, setMainItems] = React.useState<NavLink[]>([
    { label: "Home", route: "/" },
    { label: "Login", route: "/login" },
    { label: "Register", route: "/register" },
  ]);

  return (
    <HeaderNavigation>
      <NavigationList $align={ALIGN.left}>
        <NavigationItem>Weather-App</NavigationItem>
      </NavigationList>

      <NavigationList $align={ALIGN.center} />

      <NavigationList $align={ALIGN.right}>
        {mainItems.map((navItem) => {
          return (
            <>
              <NavigationItem>
                <Link href={navItem.route}>{navItem.label}</Link>
              </NavigationItem>
            </>
          );
        })}
       
      </NavigationList>
    </HeaderNavigation>
  );
};
