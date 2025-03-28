import { useState } from 'react'

import { Card, StyledBody, StyledAction } from "baseui/card";
import { Button } from "baseui/button";
import { Input } from 'baseui/input';
import axios
    from 'axios';
import { FormControl } from "baseui/form-control";
import { Notification, KIND } from "baseui/notification";

import { useNavigate } from 'react-router';

export const Register = () => {
    const navigate = useNavigate();
    const [userName, setUserName] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [error, setError] = useState<string>("")

    const handleRegister = () => {
        axios.post(`http://localhost:5001/api/user/register`)
            .then(res => {
                console.log(res.data)

                //  setEntries({ persons });
            }).catch(error => {
                console.error(error)
                setError(error);
            })
    }

    return (<>
        <Card
            title="Register"
        >
            <StyledBody>
                <FormControl label="User name">
                    <Input
                        value={userName}
                        onChange={e => setUserName(e.target.value)}
                        placeholder="JohnDoe"
                        clearOnEscape
                    />
                </FormControl>
                <FormControl label="Password">

                    <Input
                        onChange={(event) => setPassword(event.currentTarget.value)}
                        type="password"
                        value={password}
                    />
                </FormControl>

            </StyledBody>
            <StyledAction>
                <Button onClick={handleRegister} overrides={{ BaseButton: { style: { width: "100%" } } }}>
                    Register
                </Button>
                <Button onClick={()=>navigate("/login")} overrides={{ BaseButton: { style: { width: "100%" } } }}>
                    Back to login
                </Button>

                 { error && <Notification kind={KIND.negative} closeable>
                    {() => error}
                    </Notification>}
            </StyledAction>
        </Card>
    </>);
}