import { useState } from 'react'

import { Card, StyledBody, StyledAction } from "baseui/card";
import { Button } from "baseui/button";
import { Input } from 'baseui/input';
import axios
    from 'axios';
export const Login = () => {
    const [userName, setUserName] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = () => {
        axios.post(`http://localhost:5001/api/user/login`)
        .then(res => {
            console.log(res.data)

            //  setEntries({ persons });
        })
    }
    

    return (<>
        <Card

            title="Login"
        >
            <StyledBody>

                <Input
                    value={userName}
                    onChange={e => setUserName(e.target.value)}
                    placeholder="JohnDoe"
                    clearOnEscape
                />

                <Input
                    onChange={(event) => setPassword(event.currentTarget.value)}
                    type="password"
                    value={password}
                />
            </StyledBody>
            <StyledAction>
                <Button  onClick={handleLogin} overrides={{ BaseButton: { style: { width: "100%" } } }}>
                    Button Label
                </Button>
            </StyledAction>
        </Card>



    </>);
}